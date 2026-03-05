import yfinance as yf
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt


def user_input():
    while True:
        ticker = input('Input a ticker:')
        if ticker == 'QUIT':
            return 'QUIT'
        if ticker == 'CLEAR':
            return 'CLEAR'
        if ticker == 'COMPARE':
            while True:
                ticker1 = input('Ticker1:')
                try:
                    data1 = yf.Ticker(ticker1).info
                    break
                except Exception:
                    print('Invalid Ticker')
            while True:
                ticker2 = input('Ticker2:')
                try:
                    data2 = yf.Ticker(ticker2).info
                    break
                except Exception:
                    print('Invalid Ticker')
            return(ticker1,data1,ticker2,data2)
        try:
            data = yf.Ticker(ticker).info
            break
        except Exception:
            print('Invalid Ticker')
    return (ticker,data)

def ticker_request(ticker:str,ticker_data):
    current_price = ticker_data.get('currentPrice') or ticker_data.get('regularMarketPrice')
    open_price = ticker_data.get('open')
    change = ((current_price-open_price)/open_price) *100
    name = ticker_data.get('shortName')
    return (name,ticker,current_price,change)

def save(file:str,data:tuple,news):
    text = f'{data[0]} ({(data[1].upper())}): Market Price: {data[2]}, Day Change: {data[3]:.2f}%\n'
    with open(file,'a') as new:
        new.write(text)
        new.write('-'*len(text))
        new.write('\nLatest News:\n')
        for i in news:
            new.write(f'{i}\n')
        new.write(f'\nSee Chart: {data[1]}.png\n')
    print('Data saved')

def web_scraper(ticker:str):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f'https://finance.yahoo.com/quote/{ticker}/'
    data = requests.get(url, headers=headers).text
    soup = BeautifulSoup(data, 'html.parser')
    titles = soup.find_all('h3', class_='clamp')
    titles = [i.text for i in titles]
    return titles

def clear_file(file:str):
    with open(file,'w') as new:
        print('Data Cleared')

def price_chart(ticker):
    ticker1 = yf.Ticker(ticker)
    two_year_history = ticker1.history(period='2y')
    two_year = two_year_history['Close']
    thundred_ma = two_year.rolling(window=200).mean()
    fifty_ma = two_year.rolling(window=50).mean()
    plt.plot(two_year_history.index,two_year,label = ticker)
    plt.plot(two_year_history.index,thundred_ma,label = f'{ticker.upper()} 200 day MA')
    plt.plot(two_year_history.index,fifty_ma,label = f'{ticker.upper()} 50 day MA')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{ticker.upper()} Price History')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{ticker}.png')

def comparison_chart(ticker1:str,ticker2:str):
    ticker1_info = yf.Ticker(ticker1)
    ticker2_info = yf.Ticker(ticker2)
    two_year_history1 = ticker1_info.history(period='2y')
    two_year_history2 = ticker2_info.history(period='2y')
    two_year_close1 = two_year_history1['Close']
    two_year_close2 = two_year_history2['Close']
    one_ma = two_year_close1.rolling(window=50).mean()
    two_ma = two_year_close2.rolling(window=50).mean()
    plt.plot(two_year_history1.index,one_ma,label=f'{ticker1.upper()} 50 day MA')
    plt.plot(two_year_history2.index,two_ma,label=f'{ticker2.upper()} 50 day MA')
    plt.plot(two_year_history1.index,two_year_close1,label=f'{ticker1.upper()} Close')
    plt.plot(two_year_history2.index,two_year_close2,label=f'{ticker2.upper()} Close')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{ticker1.upper()} and {ticker2.upper()} Price History')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(ticker1 + '_' + ticker2 + '.png')
    print('Chart Generated')


print('Generate Stock Reports')
print('Type QUIT to exit or CLEAR to clear file or COMPARE to compare stocks')
while True:
    ticker = user_input()
    if ticker == 'QUIT':
        break
    elif ticker == 'CLEAR':
        clear_file('research_data.txt')
    elif len(ticker) > 3:
        comparison_chart(ticker[0],ticker[2])
    else:
        data = ticker_request(ticker[0],ticker[1])
        news = web_scraper(ticker[0])
        price_chart(ticker[0])
        save('research_data.txt',data,news)
print('You may view your summary at research_data.txt')