# 株価変動＆IPO情報自動通知スクリプト（Python）

## 概要
このスクリプトは、Pythonで構成された自動通知ツールです。

- 株式インデックスやETFの価格変動を監視
- 日本取引所グループ（JPX）から新規上場企業情報を取得
- 条件を満たす場合、Gmailから自動で通知メールを送信

## 必要ライブラリ

```bash
pip install pandas yfinance requests python-dotenv
```

## 実行前の準備

1. `.env` ファイルを用意して、以下のように記入してください：

```
FROM_EMAIL=your_email@gmail.com
TO_EMAIL=recipient_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

2. `.gitignore` に `.env` を追加し、GitHubに公開しないようにしてください。

## 実行方法

```bash
python month_mail2_safe.py
```

## ⛔ スクレイピングに関する注意
- 本スクリプトはJPX公式サイトの公開情報を対象としたスクレイピングです。
- robots.txtを遵守し、過剰なアクセスは行っていません。


## ライセンス

MIT
