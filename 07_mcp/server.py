import math
from mcp.server.fastmcp import FastMCP

# MCPサーバーの初期化
mcp = FastMCP("GenAI-Lab-MCP-Server")


@mcp.tool()
def calculate_hypotenuse(a: float, b: float) -> float:
    """直角三角形の2辺の長さ (a, b) から斜辺の長さを計算します。"""
    return math.sqrt(a**2 + b**2)


@mcp.tool()
def get_system_status() -> str:
    """現在のシステムステータスを取得します。"""
    return "All systems operational. BigQuery connection: ACTIVE."


if __name__ == "__main__":
    # stdio トランスポートでサーバーを実行
    mcp.run(transport="stdio")