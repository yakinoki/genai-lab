import os
import sys

from google import genai
from google.genai.errors import APIError


def main() -> None:
    # GEMINI_API_KEY が未設定の場合の早期チェック
    if "GEMINI_API_KEY" not in os.environ:
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    # クライアントの初期化（GEMINI_API_KEY は自動的に読み込まれます）
    client = genai.Client()

    prompt = "Explain what a Forward Deployed Engineer does in three sentences."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        print("=== Model Response ===")
        print(response.text)

    except APIError as e:
        print(f"API Error occurred: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()