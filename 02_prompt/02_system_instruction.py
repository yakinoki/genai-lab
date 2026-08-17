import os
from google import genai
from google.genai import types

client = genai.Client()
MODEL_NAME = "gemini-2.5-flash"


def run_with_system_instruction():
    print("\n=== System Instruction による振る舞い制御 ===")

    # システムプロンプトによる制約とペルソナ定義
    system_instruction = """
あなたはコードレビューを担当するシニアデータエンジニアです。
回答を作成する際は以下の制約条件を厳格に守ってください：

1. 結論から述べること。
2. 箇条書きで簡潔に指摘すること。
3. 専門用語（例: 冪等性, パーティショニング）を適切に用いて技術的な厳密性を保つこと。
4. コードの修正例を必ず提示すること。
"""

    user_prompt = """
以下のSQLクエリのレビューをお願いします。

SELECT *
FROM `project.dataset.events`
WHERE TIMESTAMP_TRUNC(event_timestamp, DAY) = "2026-08-01"
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,  # 一貫性を高めるため低めに設定
        ),
    )
    print(response.text)


if __name__ == "__main__":
    run_with_system_instruction()