import asyncio
import os
import sys
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Gemini クライアントの初期化 (環境変数 GEMINI_API_KEY を使用)
gemini_client = genai.Client()


async def main():
    # 同一ディレクトリの server.py を起動する設定
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[os.path.join(os.path.dirname(__file__), "server.py")],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. MCP サーバーの初期化
            await session.initialize()

            # 2. サーバーから利用可能なツール一覧を取得
            mcp_tools = await session.list_tools()
            print(
                f"[MCP Client] Discovered tools: {[t.name for t in mcp_tools.tools]}"
            )

            # 3. Prompt の定義
            user_prompt = "直角三角形の底辺が3、高さが4のとき、斜辺の長さはいくらですか？"
            print(f"\nUser: {user_prompt}")

            # 4. MCP の Tool 定義を Gemini 側の関数呼び出し形式に変換して渡す
            # (※ここでは概念理解のため、直接ツール実行を呼び出すフローを記述)
            tool_to_call = "calculate_hypotenuse"
            tool_args = {"a": 3.0, "b": 4.0}

            # 5. MCP サーバー上のツールを実行 (Call Tool)
            print(
                f"[MCP Client] Executing tool '{tool_to_call}' with args: {tool_args}"
            )
            result = await session.call_tool(tool_to_call, arguments=tool_args)

            # 6. 結果の出力
            mcp_output = result.content[0].text
            print(f"[MCP Server Response]: {mcp_output}")

            # 7. ツール結果を組み込んで Gemini で最終回答を作成
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"ユーザーの質問: {user_prompt}\nツール実行結果: {mcp_output}\n上記の結果を踏まえて回答を作成してください。",
            )

            print(f"\nGemini Response:\n{response.text}")


if __name__ == "__main__":
    asyncio.run(main())