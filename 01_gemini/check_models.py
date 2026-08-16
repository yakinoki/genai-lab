import os
import sys
from google import genai


def main() -> None:
    if "GEMINI_API_KEY" not in os.environ:
        print("Error: GEMINI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client()

    print("=== Available Models ===")

    try:
        for model in client.models.list():
            if "generateContent" in getattr(model, "supported_actions", []):
                print(model.name)

    except Exception as e:
        print(f"Failed to list models: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()