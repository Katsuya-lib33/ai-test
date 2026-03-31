# YouTube台本生成AIエージェント

YouTube動画の台本作成を支援する、**日本語向けの台本生成AIエージェント**です。

## 機能
- 入力（テーマ・ターゲット・尺・トーン）から台本を生成
- 4段階ワークフロー
  1. リサーチ観点整理
  2. 構成案（フック・本編・CTA）作成
  3. 完成台本生成
  4. 品質チェック（冗長性・一貫性・CTA妥当性）
- JSON出力とMarkdown出力の両対応

## セットアップ
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

環境変数を設定:
```bash
export OPENAI_API_KEY="your_api_key"
```

## 使い方
```bash
python youtube_script_agent.py \
  --topic "初心者向けNISAの始め方" \
  --audience "20-30代の会社員" \
  --duration-minutes 8 \
  --tone "親しみやすく、信頼感" \
  --format markdown
```

JSON形式で保存:
```bash
python youtube_script_agent.py \
  --topic "生成AI副業の始め方" \
  --audience "副業初心者" \
  --duration-minutes 10 \
  --tone "実践重視" \
  --format json > output.json
```

## ファイル構成
- `youtube_script_agent.py`: 実行スクリプト
- `prompts.py`: エージェント用プロンプト定義
- `requirements.txt`: 依存パッケージ

## 注意
- 生成内容は公開前に必ずファクトチェックしてください。
- 医療・法律・投資など高リスク領域では専門家監修を推奨します。
