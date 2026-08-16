# 01_gemini

Gemini APIをPythonから利用する基本的な実験。

## Purpose

Gemini APIの基本的な利用方法とレスポンス構造を理解する。
サードパーティのフレームワークに依存せず、公式SDK (`google-genai`) を直接操作してモデル呼出の原点を確認する。

## Environment

- Python 3.10+
- `google-genai`

### Installation

```bash
py -m pip install google-genai
```

### Environment Variables

1. [Google AI Studio](https://aistudio.google.com/) にアクセスし、Google アカウントでログインします。
2. 「Get API key」 > 「Create API key」 から本物の API キーを発行します。
3. ターミナルで発行された API キーを環境変数に設定します。

macOS/Linux の場合
```bash
export GEMINI_API_KEY="XXXXXXXXXXXXXXXXXXXXX"
```

Windows (PowerShell) の場合
```
$env:GEMINI_API_KEY="XXXXXXXXXXXXXXXXXXXXX"
```

以下のコードでAPIを確認
```
echo $env:GEMINI_API_KEY
```

## Experiments

| File | Description |
|---|---|
| `01_basic_api.py` | `gemini-3.5-flash` を用いた最小限のテキスト生成 |

## Execution

```bash
py 01_basic_api.py
```

## Key Learnings / Notes

- **SDK**: `google-genai`（統合された新しい公式SDK）を使用。
- **認証**: `genai.Client()` はデフォルトで環境変数 `GEMINI_API_KEY` を参照する。
- **モデル選択**: 軽量・高速な検証には `gemini-2.5-flash` を基本として利用する。