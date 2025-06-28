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

![通知例](https://github.com/sinnichi/stock-alert-notifier/blob/3b7017d196cb59431f2f5e1837bf68d50480bb61/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202025-06-28%20225351.png)


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
