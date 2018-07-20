import requests
import json

convert = 'USD'

listing_url = 'https://api.coinmarketcap.com/v2/listings/'
url_end = '?structure=array&convert=' + convert

request = requests.get(listing_url)
results_dict = request.json()

data_list = results_dict['data']  # data is a list containing many dict
ticker_url_pairs = {}

'''this loop is able to find all symbol and id pair, and store in a dict'''
# the first currency item is
# {'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'website_slug': 'bitcoin'}
for currency in data_list:
    symbol = currency['symbol']  # 'BTC'
    url = currency['id']  # 1
    ticker_url_pairs[symbol] = url  # 'BTC': 1

# print(ticker_url_pairs)

while True:
    print()
    choice = input("Enter the ticker symbol of a crypto-currency: ")
    choice = choice.upper()

    ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[choice]) + '/' + url_end

    request = requests.get(ticker_url)
    results = request.json()

    #print(json.dumps(results, sort_keys=True, indent=4))

    currency = results['data'][0]  # currency is dict
    rank = currency['rank']
    name = currency['name']
    symbol = currency['symbol']

    circulating_supply = int(currency['circulating_supply'])
    total_supply = int(currency['total_supply'])

    quotes = currency['quotes'][convert]  # in this case, convert is USD
    market_cap = quotes['market_cap']
    hour_change = quotes['percent_change_1h']
    day_change = quotes['percent_change_24h']
    week_change = quotes['percent_change_7d']
    price = quotes['price']
    volume = quotes['volume_24h']

    volume_string = '{:,}'.format(volume)
    market_cap_string = '{:,}'.format(market_cap)
    circulating_supply_string = '{:,}'.format(circulating_supply)
    total_supply_string = '{:,}'.format(total_supply)

    print(str(rank) + ': ' + name + ' (' + symbol + ')')
    print('Market cap: \t\t$' + market_cap_string)
    print('Price: \t\t\t\t$' + str(price))
    print('24h Volume: \t\t$' + volume_string)
    print('Hour change: \t\t' + str(hour_change) + '%')
    print('Day change: \t\t' + str(day_change) + '%')
    print('Week change: \t\t' + str(week_change) + '%')
    print('Total supply: \t\t' + total_supply_string)
    print('Circulating supply: ' + circulating_supply_string)
    print('Percentage of coins in circulation: ' + str(int(circulating_supply / total_supply * 100)))
    print()

    choice = input('Again? (y/n): ')

    if choice == "n":
        break


