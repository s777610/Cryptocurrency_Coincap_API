import os
import json
import requests
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style


convert = 'USD'
listings_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
url_end = '?structure=array&convert=' + convert

request = requests.get(listings_url)
results = request.json()
data_list = results['data']  # data_list is a list containing many dict

ticker_url_pairs = {}  # store symbol and id later

'''this loop is able to find all symbol and id pair, and store in a dict'''
# the first currency item is
# {'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'website_slug': 'bitcoin'}
for currency in data_list:
    symbol = currency['symbol']  # 'BTC'
    url = currency['id']  # 1
    ticker_url_pairs[symbol] = url  # 'BTC': 1


print()
print("My Portfolio")
print()

portfolio_value = 0.00
last_updated = 0

table = PrettyTable(['Asset', 'Amount Owned', convert + 'Value', 'Price', '1h', '24h', '7d'])
with open("portfolio.txt") as inp:
    for line in inp:
        ticker, amount = line.split()
        ticker = ticker.upper()

        ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end

        request = requests.get(ticker_url)
        results = request.json()

        currency = results['data'][0]
        rank = currency['rank']
        name = currency['name']
        last_updated = currency['last_updated']
        symbol = currency['symbol']
        quote = currency['quotes'][convert]
        hour_change = quote['percent_change_1h']
        day_change = quote['percent_change_24h']
        week_change = quote['percent_change_7d']
        price = quote['price']

        value = float(price) * float(amount)

        if hour_change > 0:
            hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
        else:
            hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL
        if day_change > 0:
            day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
        else:
            day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL
        if week_change > 0:
            week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
        else:
            week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

        portfolio_value += value
        value_string = '{:,}'.format(round(value, 2))

        table.add_row([name + ' (' + symbol + ')',
                       amount,
                       '$' + value_string,
                       '$' + str(price),
                       str(hour_change),
                       str(day_change),
                       str(week_change)])


print(table)
print()

portfolio_value_string = '{:,}'.format(round(portfolio_value, 2))
last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')

print("Total Portfolio Value: " + Back.GREEN + "$" + portfolio_value_string + Style.RESET_ALL)
print()
print("API Results Last Updated on " + last_updated_string)
print()
