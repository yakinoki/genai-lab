import os
import sys
from typing import Any

from google import genai
from google.genai import types


MODEL_NAME = "gemini-2.5-flash"
MAX_STEPS = 5


def calculate(expression: str) -> str:
    """Calculate a simple arithmetic expression.

    Args:
        expression: Arithmetic expression such as "120 * 1.1".
    """
    # This is intentionally a very small demo tool.
    # Do not use eval() for arbitrary user input in production.
    allowed_chars = set("0123456789+-*/(). ")

    if not expression or not set(expression) <= allowed_chars:
        return "Error: unsupported expression."

    try:
        # The expression is restricted to arithmetic characters only.
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as exc:
        return f"Error: {exc}"


def lookup_product_price(product_name: str) -> str:
    """Look up a product price from a small demo database.

    Args:
        product_name: Product name to look up.
    """
    products = {
        "laptop": 150000,
        "monitor": 50000,
        "keyboard": 12000,
        "mouse": 8000,
    }

    price = products.get(product_name.lower())

    if price is None:
        return f"Product '{product_name}' was not found."

    return f"{product_name}: JPY {price:,}"


TOOLS = {
    "calculate": calculate,
    "lookup_product_price": lookup_product_price,
}


def execute_tool(function_name: str, args: dict[str, Any]) -> str:
    """Execute a tool selected by the model."""
    function = TOOLS.get(function_name)

    if function is None:
        return f"Error: unknown tool '{function_name}'."

    try:
        result = function(**args)
        return str(result)
    except Exception as exc:
        return f"Error while executing '{function_name}': {exc}"


def run_agent(client: genai.Client, user_input: str) -> str:
    """Run a simple agent loop."""

    contents: list[types.Content] = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
        )
    ]

    for step in range(1, MAX_STEPS + 1):
        print(f"\n[Agent step {step}]")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a simple AI agent. "
                    "Use tools when they are useful. "
                    "You may call multiple tools when necessary. "
                    "When you have enough information, provide the final answer."
                ),
                tools=list(TOOLS.values()),
                temperature=0,
            ),
        )

        if not response.candidates:
            return "Error: no response candidates."

        candidate = response.candidates[0]
        model_content = candidate.content

        if model_content is None:
            return "Error: model returned no content."

        contents.append(model_content)

        function_calls = []

        for part in model_content.parts or []:
            if part.function_call is not None:
                function_calls.append(part.function_call)

        if not function_calls:
            return response.text or "No response."

        for function_call in function_calls:
            function_name = function_call.name
            args = dict(function_call.args or {})

            print(f"Tool: {function_name}")
            print(f"Args: {args}")

            tool_result = execute_tool(function_name, args)

            print(f"Result: {tool_result}")

            contents.append(
                types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={
                                "result": tool_result,
                            },
                        )
                    ],
                )
            )

    return f"Error: agent exceeded maximum steps ({MAX_STEPS})."


def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print(
            "Error: GEMINI_API_KEY environment variable is not set.",
            file=sys.stderr,
        )
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    print("GenAI Lab - 06 Agent")
    print("Type 'exit' to quit.")

    while True:
        try:
            user_input = input("\nUser> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        answer = run_agent(client, user_input)

        print(f"\nAgent> {answer}")


if __name__ == "__main__":
    main()