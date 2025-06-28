# stock-alert-notifier

[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📌 Table of Contents
- [概要](#概要)
- [特徴](#特徴)
- [使い方](#使い方)
- [依存関係](#依存関係)
- [実行例](#実行例)
- [ファイル構成](#ファイル構成)
- [注意事項](#注意事項)
- [ライセンス](#ライセンス)

## 概要
株価の変動やIPO情報を監視して、条件に応じてGmailで通知するPythonスクリプト。

## 特徴
- ✅ yfinanceで主要インデックス監視  
- ✅ JPXサイトからIPO情報をスクレイピング  
- ✅ 一定以上の変動があれば通知  
- ✅ Gmailの自動送信付き

## 使い方
1. リポジトリをクローン  
2. `.env` を配置（`FROM_EMAIL`などを記入）  
3. ライブラリをインストール  
4. `python month_mail2_safe.py` を実行

## 依存関係
```bash
pip install pandas yfinance requests python-dotenv

## 📸 実行結果イメージ

以下は株価急変時のメール通知例です：

![通知例](![スクリーンショット 2025-06-28 225323](https://github.com/user-attachments/assets/b70c9fdf-cf83-440b-af47-4717f6ab4e7b)
)

##ファイル構成
├ stock-ipo-monitor.py
├ .env.example
├ README.md
└ .gitignore

##注意
.env ファイルは 公開しないでください

## ⛔ スクレイピングに関する注意
- 本スクリプトはJPX公式サイトの公開情報を対象としたスクレイピングです。
- robots.txtを遵守し、過剰なアクセスは行っていません。


## ライセンス

MIT
