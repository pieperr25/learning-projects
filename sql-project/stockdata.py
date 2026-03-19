#psql -U postgres stockdata


import psycopg2
import yfinance as yf

conn = psycopg2.connect(
    dbname="stockdata",
    user="postgres",
    password="92312",
    host="localhost",
    port="5432"
)

tickers = []
print('Type a valid ticker or QUIT to see portfolio or REMOVE')
while True:
    ticker = input('Ticker:')
    if ticker == 'QUIT':
        break
    if ticker == 'REMOVE':
        ticker_remove = input('Which ticker would you like removed:')
        curs = conn.cursor()
        curs.execute("DELETE FROM stockdata WHERE ticker = %s",
                     (ticker_remove,))
        conn.commit()
        continue
    try:
        (yf.Ticker(ticker)).info['quoteType']
        tickers.append(ticker)
    except (KeyError, Exception):
        print('Invalid ticker')


for i in tickers:
    data = (yf.Ticker(i)).info
    open = data['open']
    market = data.get('currentPrice') or data.get('regularMarketPrice')
    history = (yf.Ticker(i)).history('ytd')
    close = history['Close']
    first_price = close.iloc[0]
    ytd = ((market - first_price) / first_price) * 100
    day = ((market - open) / open) * 100

    curs = conn.cursor()
    curs.execute(
        "INSERT INTO stockdata (ticker,market_open,market_price,day_change,ytd_change)" 
        "Values (%s,%s,%s,%s,%s)", 
        (i,open,market,round(float(day),2),round(float(ytd),2))
    )
    conn.commit()
    
curs = conn.cursor()
curs.execute(
    "SELECT * FROM stockdata"
)
final_data  = curs.fetchall()
print(final_data)
print(f"{'Stock':<16}{'Open':>10}{'Market':>13}{'Day Change':>15}{'YTD Change':>13}")
print('-' * 67)
for i in final_data:
    ticker = i[0]
    open = i[1]
    market = i[2]
    day = i[3]
    ytd = i[4]
    print(f'{ticker:<16}{open:>10}{market:>13}{day:>15}{ytd:>15}')
