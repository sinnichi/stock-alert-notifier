#個人情報をここで分ける
import os
from dotenv import load_dotenv
load_dotenv()

#入っていないものがあれば入れてから実行すること
import yfinance as yf
import pandas as pd
import time
import random
import datetime
import requests
import sys

# --- メール送信関連のインポート ---
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
# --- メール送信関連のインポート 終わり ---

print("--- 株価変動モニタリングプログラムを開始します ---")

# --- 設定項目 ---
ticker_symbols = [

 # 海外の主要インデックス、一例なので好きなものを登録してください
    "^GSPC",   # S&P 500 (米国)
    "^IXIC",   # NASDAQ 総合指数 (米国)
    "^GDAXI",  # ドイツDAX指数
    "^FTSE",   # FTSE 100 (英国)
    "000001.SS", # 上海総合指数 (中国)
    "399001.SZ", # 深圳成分指数 (中国)
    "^N225",     # 日経平均株価 (日本)
    "GLD",       # SPDR ゴールド・シェア (金ETF)
    "IAU"        # iシェアーズ ゴールドトラスト (金ETF)
]

# 株価変動の閾値（%）、インデックスなので1％でも大きいはず、、、
decrease_threshold_percent = -1.0
increase_threshold_percent = 1.0

# 過去何日間のデータを取得するか (直近2営業日を比較するために少し余裕を持たせる)
fetch_days = 10

# リクエスト間の最小・最大待機時間（秒）、これがないとサイト側から拒否されます
min_sleep_time = 3
max_sleep_time = 7

# --- User-Agent の設定 ---
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    # ※ Chromeのバージョンは適宜最新のものを調べて設定してください
}

# --- メール設定 ---詳しくは.env.exampleを
from_addr = os.getenv("FROM_EMAIL")
to_addr = os.getenv("TO_EMAIL")
password = os.getenv("EMAIL_PASSWORD")
smtp_host = 'smtp.gmail.com'
smtp_port = 587


# --- データ取得期間の計算 ---インデックスが大きく動いたときに連絡できるようにします
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=fetch_days)

print(f"\n監視対象ティッカー: {ticker_symbols}")
print(f"取得期間: {start_date} から {end_date}")
print(f"減少報告閾値: {decrease_threshold_percent:.1f}%")
print(f"増加報告閾値: {increase_threshold_percent:.1f}%")

found_fluctuations = [] # 減少・増加があった銘柄と情報を格納するリスト

for ticker in ticker_symbols:
    print(f"\n--- {ticker} の株価データを取得中... ---")
    
    sleep_duration = random.uniform(min_sleep_time, max_sleep_time)
    print(f"  次のリクエストまで {sleep_duration:.2f} 秒待機します...")
    time.sleep(sleep_duration)

    try:
        stock_data = yf.download(
            ticker, 
            start=start_date, 
            end=end_date, 
            progress=False, 
            actions=False, 
        )

        if not stock_data.empty:
            close_prices = stock_data['Close']
            
            # データが十分にあるか確認 (少なくとも2営業日分)
            if len(close_prices) < 2:
                print(f"  {ticker}: 比較するための十分なデータがありません（少なくとも2営業日必要です）。")
                continue

            daily_returns = close_prices.pct_change() * 100

            latest_date = daily_returns.index[-1]
            latest_change = daily_returns.iloc[-1].item()

            yesterday_close_value = close_prices.iloc[-2].item()
            today_close_value = close_prices.iloc[-1].item()

            print(f"  {ticker} の最新営業日 ({latest_date.strftime('%Y-%m-%d')}) の株価変化率: {latest_change:.2f}%")

            if latest_change <= decrease_threshold_percent:
                message_type = "暴落"
                message_body = (
                    f"【アラート！】 {ticker} が {latest_date.strftime('%Y-%m-%d')} に{message_type}しました。\n"
                    f"  終値変化率: {latest_change:.2f}%\n"
                    f"  昨日の終値: {yesterday_close_value:.2f} USD\n"
                    f"  今日の終値: {today_close_value:.2f} USD"
                )
                print(message_body)
                found_fluctuations.append(message_body)
            elif latest_change >= increase_threshold_percent:
                message_type = "急騰"
                message_body = (
                    f"【アラート！】 {ticker} が {latest_date.strftime('%Y-%m-%d')} に{message_type}しました。\n"
                    f"  終値変化率: {latest_change:.2f}%\n"
                    f"  昨日の終値: {yesterday_close_value:.2f} USD\n"
                    f"  今日の終値: {today_close_value:.2f} USD"
                )
                print(message_body)
                found_fluctuations.append(message_body)
            else:
                print(f"  {ticker}: 報告閾値（±{abs(decrease_threshold_percent):.1f}%）を超える変動はありません。")

        else:
            print(f"  {ticker}: データが見つからないか、取得できませんでした。")

    except Exception as e:
        print(f"  {ticker} の取得または処理中にエラーが発生しました: {e}")
        print(f"  詳細: {e}")

print("\n--- 株価変動モニタリングプログラムを終了します ---")


print("--- 日本の新規上場企業情報取得プログラムを開始します ---")

# --- 設定項目 ---来月の予定を送ります
url_ipo = "https://www.jpx.co.jp/listing/stocks/new/index.html"
min_sleep_time = 2
max_sleep_time = 5
headers_req = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

# --- 重複列名を一意に変換する関数 ---
def deduplicate_columns(columns):
    seen = {}
    new_cols = []
    for col in columns:
        if col not in seen:
            seen[col] = 0
            new_cols.append(col)
        else:
            seen[col] += 1
            new_cols.append(f"{col}.{seen[col]}")
    return new_cols

try:
    sleep_duration_ipo = random.uniform(min_sleep_time, max_sleep_time)
    print(f"URL: {url_ipo} にアクセス中... ({sleep_duration_ipo:.2f} 秒待機)")
    time.sleep(sleep_duration_ipo)

    response_ipo = requests.get(url_ipo, headers=headers_req)
    response_ipo.raise_for_status()
    response_ipo.encoding = response_ipo.apparent_encoding

    print("HTMLコンテンツの取得に成功しました。解析中...")

    dfs_from_html_ipo = pd.read_html(response_ipo.text)

    if dfs_from_html_ipo:
        df_ipo_raw = dfs_from_html_ipo[0]

        print("\n--- 新規上場企業情報（rawデータ、最初の5行） ---")
        print(df_ipo_raw.head().to_string())
        print(f"rawデータの列数: {len(df_ipo_raw.columns)}")

        # MultiIndex対応と前処理
        if isinstance(df_ipo_raw.columns, pd.MultiIndex):
            df_ipo_raw.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df_ipo_raw.columns.values]
        df_ipo_raw.columns = df_ipo_raw.columns.str.replace(r'\s+', ' ', regex=True).str.strip()
        df_ipo_raw.columns = df_ipo_raw.columns.str.replace('\n', ' ', regex=False).str.strip()
        df_ipo_raw.columns = deduplicate_columns(df_ipo_raw.columns)

        print("\n--- 整形後のdf_ipo_raw列名 ---")
        print(df_ipo_raw.columns.tolist())

        # --- 上場月を文字列で検索する方式 ---
        current_date_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()

        # 来月の日付を計算
        if current_date_jst.month == 12:
            next_month_date = current_date_jst.replace(year=current_date_jst.year + 1, month=1, day=1)
        else:
            next_month_date = current_date_jst.replace(month=current_date_jst.month + 1, day=1)

        next_month_str = str(next_month_date.month).zfill(2)
        next_year = next_month_date.year

        target_month_str = f"{next_year}/{next_month_str}" # ここが新しい来月の文字列になります！

        print(f"\n>>> 全データから '{target_month_str}' を検索してフィルタします...")

        # すべての列を文字列型にして対象文字列を含む行を抽出
        df_all_str = df_ipo_raw.astype(str)
        mask = df_all_str.apply(lambda row: target_month_str in ' '.join(row), axis=1)
        july_ipos = df_ipo_raw[mask].copy()

        if not july_ipos.empty:
            print(f"\n--- {current_date_jst.year}年 '{target_month_str}' 月に上場予定の企業情報（{len(july_ipos)}件） ---")
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            pd.set_option('display.max_rows', None)
            print(july_ipos.to_string(index=False))
        else:
            print(f"\n{current_date_jst.year}年 '{target_month_str}' 月に上場予定の企業は見つかりませんでした。")

    else:
        print("新規上場企業情報のあるテーブルが見つかりませんでした。")

except requests.exceptions.RequestException as e:
    print(f"Webページへのアクセス中にエラーが発生しました: {e}")
except Exception as e:
    print(f"データの解析中にエラーが発生しました: {e}")

print("\n--- プログラム実行を終了します ---")
print("\n--- 総合報告 ---")
print("新規上場企業情報の取得と表示が完了しました。")


# --- 最終的な報告メールの送信 ---
email_subject = f"株価変動アラート報告 ({datetime.date.today().strftime('%Y-%m-%d')})"
email_body_list = []

if found_fluctuations:
    email_body_list.append("--- 総合報告：変動があった銘柄 ---")
    for msg in found_fluctuations:
        email_body_list.append(msg)
else:
    email_body_list.append(f"--- 総合報告：直近1週間で報告すべき大きな（±{abs(decrease_threshold_percent):.1f}%）変動は見つかりませんでした ---")

if 'july_ipos' in locals() and not july_ipos.empty: # july_iposが存在し、かつデータがあるか確認
    email_body_list.append("\n\n--- 新規上場企業情報 ---")
    email_body_list.append(july_ipos.to_string(index=False)) # DataFrameを文字列に変換して追加
else:
    email_body_list.append("\n\n--- 新規上場企業情報 ---")
    email_body_list.append(f"{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().year}年7月に上場予定の企業は見つかりませんでした。")
# --- 新規上場企業情報のメール本文への追加 終わり ---

email_body = "\n\n".join(email_body_list) # 各アラートメッセージを改行で結合

try:
    msg = MIMEText(email_body, 'plain', 'utf-8') # 日本語対応のために'utf-8'を指定
    msg['Subject'] = email_subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.starttls() # TLS暗号化を開始
        smtp.login(from_addr, password) # ログイン
        smtp.send_message(msg) # メール送信
    print(f"\nメールを送信しました: '{email_subject}' to {to_addr}")

except Exception as e:
    print(f"\nメールの送信中にエラーが発生しました: {e}")
    print("メールの送信設定（送信元アドレス、パスワード、SMTPサーバーなど）を確認してください。")
    print("特にGmailの場合、アプリパスワードの設定が必要です。")

sys.exit() # プログラムを明示的に終了させる