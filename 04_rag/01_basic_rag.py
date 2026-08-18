```python
import os
import sys

from google import genai
from google.genai import types


MODEL_NAME = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"


def load_documents() -> list[str]:
    """RAGで検索対象とするドキュメントを返す。"""
    return [
        """
        BigQueryはGoogle Cloudが提供するフルマネージドな
        データウェアハウスです。SQLを使って大規模なデータを
        分析できます。インフラストラクチャの管理は基本的に
        Google Cloud側で行われます。
        """,
        """
        BigQueryではテーブルをパーティション分割できます。
        日付やタイムスタンプなどをパーティションキーとして
        利用することで、クエリ時に不要なデータの読み取りを
        削減できます。これをパーティションプルーニングと呼びます。
        """,
        """
        BigQueryの料金は、代表的にはクエリで処理したデータ量に
        基づいて計算されます。そのため、SELECT *を避けたり、
        パーティションプルーニングを利用したりすることが
        コスト削減につながります。
        """,
        """
        dbtはSQLを中心としてデータ変換処理を管理するための
        ツールです。モデル、テスト、ドキュメントなどをコードとして
        管理できます。データパイプラインの再現性や保守性を
        高めるために利用されます。
        """,
    ]


def create_embeddings(
    client: genai.Client,
    documents: list[str],
) -> list[list[float]]:
    """ドキュメントをEmbeddingに変換する。"""
    embeddings = []

    for document in documents:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=document,
        )

        embeddings.append(response.embeddings[0].values)

    return embeddings


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """2つのベクトルのコサイン類似度を計算する。"""
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    norm_a = sum(a * a for a in vector_a) ** 0.5
    norm_b = sum(b * b for b in vector_b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def retrieve(
    client: genai.Client,
    documents: list[str],
    embeddings: list[list[float]],
    query: str,
    top_k: int = 2,
) -> list[str]:
    """クエリとドキュメントのEmbeddingを比較して上位文書を取得する。"""
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
    )

    query_embedding = response.embeddings[0].values

    scores = []

    for document, embedding in zip(documents, embeddings):
        score = cosine_similarity(query_embedding, embedding)
        scores.append((score, document))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [document for _, document in scores[:top_k]]


def generate_answer(
    client: genai.Client,
    query: str,
    retrieved_documents: list[str],
) -> str:
    """検索結果をコンテキストとしてGeminiに回答を生成させる。"""
    context = "\n\n".join(retrieved_documents)

    prompt = f"""
以下のContextだけを根拠として質問に回答してください。
Contextに答えが存在しない場合は、「Contextからは判断できません」と回答してください。

## Context

{context}

## Question

{query}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
        ),
    )

    return response.text


def main() -> None:
    if "GEMINI_API_KEY" not in os.environ:
        print(
            "Error: GEMINI_API_KEY environment variable is not set.",
            file=sys.stderr,
        )
        sys.exit(1)

    client = genai.Client()

    documents = load_documents()

    print("=== Creating embeddings ===")
    embeddings = create_embeddings(client, documents)

    query = "BigQueryのクエリ料金を削減するにはどうすればよいですか？"

    print("\n=== Query ===")
    print(query)

    retrieved_documents = retrieve(
        client=client,
        documents=documents,
        embeddings=embeddings,
        query=query,
        top_k=2,
    )

    print("\n=== Retrieved Documents ===")

    for index, document in enumerate(retrieved_documents, start=1):
        print(f"\n--- Document {index} ---")
        print(document.strip())

    answer = generate_answer(
        client=client,
        query=query,
        retrieved_documents=retrieved_documents,
    )

    print("\n=== Answer ===")
    print(answer)


if __name__ == "__main__":
    main()
```
