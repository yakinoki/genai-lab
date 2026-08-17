import os
from google import genai
from google.genai import types

# クライアントの初期化 (環境変数 GEMINI_API_KEY を使用)
client = genai.Client()

MODEL_NAME = "gemini-2.5-flash"

def run_zero_shot():
    print("\n=== 1. Zero-Shot Prompting ===")
    prompt = """
以下のテキスト感情を「Positive」「Negative」「Neutral」のいずれかで分類してください。

テキスト: 今回の新機能リリースは、パフォーマンスが向上した一方で設定画面がやや複雑になりました。
感情:
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    print(response.text)


def run_few_shot():
    print("\n=== 2. Few-Shot Prompting ===")
    prompt = """
テキストの感情を分類してください。

テキスト: 画面のレスポンスが非常に早くて快適です。
感情: Positive

テキスト: エラーが頻発して使いものになりません。
感情: Negative

テキスト: 仕様通りに動作しています。
感情: Neutral

テキスト: 今回の新機能リリースは、パフォーマンスが向上した一方で設定画面がやや複雑になりました。
感情:
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    print(response.text)


def run_chain_of_thought():
    print("\n=== 3. Chain-of-Thought (CoT) Prompting ===")
    prompt = """
以下の思考プロセスに従って、最終的な判断を導出してください。

【タスク】
ユーザーの意図を分析し、SQLクエリの最適化が必要か判断してください。

【入力】
「毎日夜間実行しているダッシュボード用のデータ更新クエリが最近30分以上かかるようになった。スキャン量が10TBを超えている。」

【ステップ】
1. 課題の特定
2. 提案される解決策の洗い出し
3. 最適化が必要かどうかの結論（YES / NO）と理由

思考プロセスと結論:
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    print(response.text)


def run_structured_prompt():
    print("\n=== 4. Structured Prompting (XML / Markdown Structuring) ===")
    prompt = """
<context>
あなたは高度なデータアナリストです。非技術者からの依頼を技術仕様に落とし込む役割を担っています。
</context>

<task>
依頼文から「分析目的」「必要なデータソース」「アウトプット形式」を抽出してください。
</task>

<input_text>
先月のマーケティングキャンペーンの効果を知りたいです。特にメール配信からのCV率と、SNS広告経由のCV率を比較して、どちらの費用対効果が高いか可視化したレポートを作成してください。
</input_text>

<output_format>
- 分析目的:
- 必要なデータソース:
- アウトプット形式:
</output_format>
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    print(response.text)


if __name__ == "__main__":
    run_zero_shot()
    run_few_shot()
    run_chain_of_thought()
    run_structured_prompt()