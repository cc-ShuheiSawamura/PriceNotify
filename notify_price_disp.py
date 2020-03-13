# _*_coding: utf-8 _*_

import requests
import traceback
import json

class Notificator():

    def __init__(self, slack_url):
        self.exchanges = {"cc", "zaif", "bf", "gmo", "liquid"}
        self.urls = {
            "cc": "https://coincheck.com/api/ticker",
            "zaif": "https://api.zaif.jp/api/1/last_price/btc_jpy",
            "bf": "https://api.bitflyer.com/v1/ticker",
            "gmo": "https://api.coin.z.com//public/v1/ticker?symbol=BTC",
            "liquid": "https://api.liquid.com/products/5"
        }
        self.prices = {}
        self.slack_url = slack_url

    def get_price(self, exchange):
        if exchange == "cc":
            try:
                self.prices["cc"] = float(requests.get(self.urls["cc"]).json()["last"])
            except:
                traceback.print_exc()
        elif exchange == "zaif":
            try:
                self.prices["zaif"] = float(requests.get(self.urls["zaif"]).json()["last_price"])
            except:
                traceback.print_exc()
        elif exchange == "bf":
            try:
                self.prices["bf"] = float(requests.get(self.urls["bf"]).json()["ltp"])
            except:
                traceback.print_exc()
        elif exchange == "gmo":
            try:
                self.prices["gmo"] = float(requests.get(self.urls["gmo"]).json()["data"][0]["last"])
            except:
                traceback.print_exc()
        elif exchange == "liquid":
            try:
                self.prices["liquid"] = float(requests.get(self.urls["liquid"]).json()["last_traded_price"])
            except:
                traceback.print_exc()
        else:
            print(f"Exchange {exchange} is not implemented")

    def disp(self, self_price, external_price):  # % of disp
        return external_price - self_price, round(external_price / self_price * 100 - 100, 3)

    def update_info(self):
        for e in self.exchanges:
            self.get_price(e)

    def notify(self):
        message = ""
        for e in self.exchanges:
            disp, disp_percent = self.disp(self.prices["cc"], self.prices[e])
            message = message + e + f": {disp}円, {disp_percent}%, "
        data = json.dumps({
            'text': message,  #通知内容
            'username': u'Price disp notificator',  #ユーザー名
            'icon_emoji': u':smile_cat:',  #アイコン
            'link_names': 1,  #名前をリンク化
        })
        try:
            print(message)
            requests.post(self.slack_url, data)
        except:
            traceback.print_exc()


if __name__ == "__main__":
    from time import sleep
    import config
    url = config.slack_url
    bot = Notificator(url)
    while True:
        bot.update_info()
        bot.notify()
        sleep(30)