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

##実行例
![image](https://github.com/user-attachments/assets/63bf7530-5eb9-4211-b079-1700eca7ac22)

![image](https://github.com/user-attachments/assets/2455ac13-0b55-4ac0-b73b-3687a8d3966b)


##ファイル構成
├ month_mail2_safe.py
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
