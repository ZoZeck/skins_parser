import requests
from bs4 import BeautifulSoup as BS

page = 1

while True:
    r = requests.get('https://market.csgo.com/?t=all&p=' + str(page))
    html = BS(r.content, 'html.parser')
    item = html.select('.market-items > .item')
    if (len(item)):
        for el in item:
            title = el.select('.name')
            price = el.select('.price')
            mas = print(f'{page} page{title[0].text}{price[0].text} rubles')
        page += 1
    else:
        break
