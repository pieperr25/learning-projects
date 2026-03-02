import yfinance as yf
import json
print('Type "done" when finished or "remove" to remove a ticker')
try:
    with open('portfolio.json','r') as f:
        portfolio = json.load(f)
except FileNotFoundError:
    portfolio = {}
while True:
    ticker = input('Ticker:')
    if ticker == 'done':
        break
    if ticker == 'remove':
        removed = input('Which ticker would you like to remove:')
        try:
            del portfolio[removed]
        except KeyError:
            print('That ticker does not exist in your portfolio')
    else:
        while True:
            try:
                shares = int(input('Shares:'))
                break
            except ValueError:
                print('Must be a valid integer')
        try:
            (yf.Ticker(ticker)).info['quoteType']
            portfolio[ticker] = shares
        except (KeyError, Exception):
            print('That ticker does not exist')

total_value = 0
print(f"{'Stock':<16}{'Price':>10}{'Shares':>13}{'Value':>15}")
print('-' * 54)
for stock in portfolio:
    ticker = yf.Ticker(stock)
    info = ticker.info
    price = info.get('currentPrice') or info.get('regularMarketPrice')
    shares = portfolio[stock]
    price_fmt = f'${price:.2f}'
    value_fmt = f'${(price * shares):.2f}'
    print(f'{stock.upper():<16}{price_fmt:>10}{str(shares):>13}{value_fmt:>15}')
    total_value += price * shares

print('-' * 54)
formatted = f"${total_value:.2f}"
print(f"{'Total':<39}{formatted:>15}")
with open('portfolio.json', 'w') as f:
    json.dump(portfolio, f)
