from matplotlib.font_manager import json_dump
import requests
import json
from bs4 import BeautifulSoup as BS
from urllib.parse import unquote
from collections import OrderedDict
import lxml.html
import time
import json
from json_excel_converter import Converter 
from json_excel_converter.xlsx import Writer


class MarketCSGOObject(dict):
    def __init__(self, name, wrapped_name, link, best_price, iterations):
        dict.__init__(self, name=name, link=f'https://market.csgo.com{link}', best_price=best_price, wrapped_name=wrapped_name)
        self.name = name
        self.link = link
        self.best_price = best_price
        self.iterations = iterations
        self.wrapped_name = wrapped_name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.name}, {self.best_price}, https://market.csgo.com{self.link}'


def gen_cfg():
    page = 0
    skins_list = dict()
    max_pages = 170 
    while page < max_pages:
        time.sleep(0.2)
        r = requests.get(f'https://market.csgo.com/?t=all&p={page}&sd=desc')
        html = BS(r.content, 'html.parser')
        item = html.select('.market-items > .item')[:56]
        tree_tm = lxml.html.document_fromstring(r.text)
        if (len(item)):
            for el in item:
                link = el.get('href')
                wrapped_name = link.split("-", 2)[2][:-1]
                skin_name = unquote(wrapped_name)
                skin_price = float(el.select('.price')[0].text.replace(u'\xa0', u' ').replace(" ", ""))
                if skin_name not in skins_list or skins_list[skin_name].best_price > skin_price:
                    skins_list[skin_name] = MarketCSGOObject(
                        skin_name,
                        wrapped_name,
                        link,
                        skin_price,
                        skins_list[skin_name].iterations + 1 if skin_name in skins_list else 0
                    )
            page += 1
        else:
            break
    return skins_list


# 0.92 cs_market 1 / 1.4 cs.money

def money(object: MarketCSGOObject):
    json_object = None
    retry = 0

    is_start_trak = object.name.startswith("StatTrak")
    is_souvenir = object.name.startswith("Souvenir")

    while json_object is None and retry < 10:
        try:
            url = f'https://cs.money/ru/csgo/trade/?search={object.wrapped_name}&sort=price&order=asc&isMarket=false&hasTradeLock=false&'
            page = requests.get(url).text
            search_1, search_2 = page.find('{"props"'), page.find('</script>')
            page_json = page[search_1:search_2]
            json_object = json.loads(page_json)
        except json.JSONDecodeError:
            retry += 1

    if retry > 10 or json_object is None:
        return None

    if len(json_object["props"]["pageProps"]["botInitData"]["skinsInfo"]["skins"]) > 0 \
        and json_object["props"]["pageProps"]["botInitData"]["skinsInfo"]["skins"][0]["fullName"] in object.name:
        value = json_object["props"]["initialReduxState"]["listCurrencies"]["RUB"]["value"]
        price = float(json_object["props"]["pageProps"]["botInitData"]["skinsInfo"]["skins"][0]["price"])
        rub = price * value
        if object.best_price * 0.92 > rub / 1.3:
            return {
                "object" : json_object["props"]["pageProps"]["botInitData"]["skinsInfo"]["skins"][0]["fullName"],
                "rub_price" : round(rub, 2),
                "url" : url
            }
        return None
    return None


def main():
    result_skins = []

    try:
        skin_list = gen_cfg()
        print(len(skin_list.values()))
        for market_skin in skin_list.values():
            if market_skin.best_price < 3000:
                money_skin = money(market_skin)
                if money_skin:
                    result_skins.append({ 
                        "csmoney_skin" : money_skin,
                        "market_csgo_skin" : market_skin,
                        "profit" : market_skin.best_price * 0.92 - money_skin["rub_price"] / 1.3
                    })
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        with open("cfg.json", 'a', encoding='utf-8') as f:
            f.write(json.dumps(result_skins, indent=4))
        Converter().convert(result_skins, Writer(file='cfg.xlsx'))


if __name__ == "__main__":
    main()
