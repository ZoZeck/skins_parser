import requests
from lxml import etree
import lxml.html
import csv
import argparse
from bs4 import BeautifulSoup as BS

class parse:
    def __init__(self, url_tm, url_money):
        self.url_tm = url_tm
        self.url_money = url_money

    def tm(self):
        try:
            num = 1
            page = 1
            print(self.url_tm + str(page))
            while (num < 57) and (page < 250):
                while page < 250:
                    api_tm = requests.get(self.url_tm)
                    tree_tm = lxml.html.document_fromstring(api_tm.text)
                    name_tm = tree_tm.xpath('//*[@id="applications"]/a['+str(num)+']/div[2]/text()')
                    print(f'[{num}] {name_tm}')
                    num = num + 1
                    print(num, '==== num')
                    if num >= 56:
                        num = 1
                        page += 1
                        print(page, '==== page')
                        self.url_tm + str(page)
                        print(self.url_tm + str(page))
        finally:
            pass

#    def money(self):
#        name = 'Paw'
#        a = '&sort=price&order=asc'
#        while True:
#            r = requests.get('https://cs.money/ru/csgo/trade/?search=' + str(name) + str(a))
#            html = BS(r.content, 'html.parser')
#            item = html.select('.actioncard_wrapper__3jY0N > .BaseCard_footer__2trfe')
#            if (len(item)):
#                for el in item:
#                    title = el.select('list_wrapper__2zFtP > .list_list__2q3CF list_large__1xvME')
#                    price = el.select('.styles_price__1m7op price_currency__1RmBq')
#                    print(f'{title[0].text} {price[0].text} rubles')
#            else:
#                break

def main():
    parse('https://market.csgo.com/?t=all&p=', 'https://cs.money/ru/csgo/trade/?search=').tm()
    parse('https://market.csgo.com/?t=all&p=', 'https://cs.money/ru/csgo/trade/?search=').money()

if __name__ == "__main__":
    main()
