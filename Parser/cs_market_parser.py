import requests
import json
from bs4 import BeautifulSoup as BS
from urllib.parse import unquote
from collections import OrderedDict


class MarketCSGOObject:
    def __init__(self, name, link, best_price, iterations):
        self.name = name
        self.link= link
        self.best_price = best_price
        self.iterations = iterations

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.name}, {self.best_price}, https://market.csgo.com{self.link}'


def main():
    page = 0
    skins_list = dict()
    while page < 10:
        r = requests.get(f'https://market.csgo.com/?t=all&p={page}&sd=desc')
        html = BS(r.content, 'html.parser')
        item = html.select('.market-items > .item')[:56]
        if (len(item)):
            for el in item:
                link = el.get('href')
                skin_name = unquote(link.split("-", 2)[2][:-1])
                skin_price = float(el.select('.price')[0].text.replace(u'\xa0', u' ').replace(" ", ""))
                if skin_name not in skins_list or skins_list[skin_name].best_price > skin_price:
                    skins_list[skin_name] = MarketCSGOObject(
                        skin_name,
                        link,
                        skin_price,
                        skins_list[skin_name].iterations + 1 if skin_name in skins_list else 0
                    )
            page += 1
        else:
            break
    return skins_list


if __name__ == "__main__":
    print(main())