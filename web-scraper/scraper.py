import requests
import csv
from bs4 import BeautifulSoup


final_price_title = []
for i in range(1,51):
    url = f'https://books.toscrape.com/catalogue/page-{i}.html'
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser',from_encoding='utf-8')
    titles = soup.find_all('h3')
    prices = soup.find_all('p',class_='price_color')
    new_prices = [i.text[2:] for i in prices]
    new_titles = [h3.find('a')['title'] for h3 in titles]
    price_title = list(zip(new_titles,new_prices))
    final_price_title.extend(price_title)



with open('books.csv','w') as new:
    csvwriter = csv.writer(new)
    csvwriter.writerow(['Title','Price'])
    csvwriter.writerows(final_price_title)