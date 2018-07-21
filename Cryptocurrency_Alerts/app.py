import os
import json
import time
import requests
from datetime import datetime


convert = 'USD'
listings_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
url_end = '?structure=array&convert=' + convert

request = requests.get(listings_url)
results = request.json()
data_list = results['data']  # data_list is a list containing many dict

ticker_url_pairs = {}  # store symbol and id later, { 'BTC': 1, .... }

'''this loop is able to find all symbol and id pair, and store in a dict'''
# the first currency item is
# {'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'website_slug': 'bitcoin'}
for currency in data_list:
    symbol = currency['symbol']  # 'BTC'
    url = currency['id']  # 1
    ticker_url_pairs[symbol] = url  # 'BTC': 1


print()
print("Alerts Tracking...")
print()

already_hit_symbols = []

while True:
    with open("alerts.txt") as inp:
        for line in inp:
            ticker, amount = line.split()
            ticker = ticker.upper()
            ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end

            request = requests.get(ticker_url)
            results = request.json()

            currency = results['data'][0]
            name = currency['name']
            last_updated = currency['last_updated']
            symbol = currency['symbol']
            quotes = currency['quotes'][convert]
            price = quotes['price'] 

            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                os.system('say ' + name + 'hit' + amount)
                last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')
                print(name + ' hit ' + amount + ' on ' + last_updated_string)
                already_hit_symbols.append(symbol)

    print("...")
    time.sleep(300)  # 5m
