# 02_prompt: Prompt Engineering Experiments

Gemini API を用いたプロンプトエンジニアリングの各種手法および制御メカニズムの検証実験。

## Overview

プロンプトの設計手法によってモデルの出力精度・フォーマット・一貫性がどのように変化するかを評価・比較する。

## Content

- `01_prompt_techniques.py`: 代表的なプロンプト手法の比較
  - Zero-Shot Prompting
  - Few-Shot Prompting
  - Chain-of-Thought (CoT) Prompting
  - Structured Prompting (XMLタグを活用した構造化)
- `02_system_instruction.py`: System Instruction (システム指示) とパラメータ調整による挙動制御

## Setup & Run

```bash
# 依存ライブラリのインストール
pip install -r requirements.txt

# APIキーの設定
export GEMINI_API_KEY="your-api-key"

# スクリプトの実行
python 01_prompt_techniques.py
python 02_system_instruction.py