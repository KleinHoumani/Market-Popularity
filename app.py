import praw
import json
import requests
import time
import os
from flask import Flask, make_response, jsonify
from threading import Thread
from operator import itemgetter

client_id = os.environ.get('REDDIT_CLIENT')
client_secret = os.environ.get('REDDIT_SECRET')
username = os.environ.get('REDDIT_USERNAME')
password = os.environ.get('REDDIT_PASSWORD')


reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     username=username, password=password, user_agent='test1')

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Mobile Safari/537.36"
}

subreddit_list = ['wallstreetbets', 'stocks', 'shortsqueeze', 'investing', 'options', 'stockmarket', 'daytrading']
time_list = ["day", 'week', 'month', 'year']
sub_data = {}


class sub:
    def __init__(self, sub_name):
        self.sub_name = sub_name
        self.data = {"day": [], "week": [], "month": [], "year": []}

    def set_data(self):
        for timeframe in time_list:
            symbol_count = []
            subreddit = reddit.subreddit(self.sub_name)
            hot_python = list(subreddit.top(timeframe, limit=100))
            time.sleep(0.5)
            with open('stock_symbols.txt', 'r') as symbolcheck:
                for line in symbolcheck:
                    x = 0
                    final_symbol1 = str(line.rstrip('\n'))
                    final_symbol2 = "$" + final_symbol1
                    for submission in hot_python:
                        post_title = submission.title
                        title_split = post_title.split()
                        if final_symbol1 in title_split or final_symbol2 in title_split:
                            x += 1

                    if timeframe == "day":
                        stock_range = "1d"
                    if timeframe == "week":
                        stock_range = "5d"
                    if timeframe == "month":
                        stock_range = "1mo"
                    if timeframe == "year":
                        stock_range = "1y"

                    if x >= 1:
                        try:
                            yahoo_url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + final_symbol1 + '?formatted=true&crumb=jEkX0k2sA5R&lang=en-US&region=US&events=div%7Csplit&includeAdjustedClose=true&interval=1d&range=' + stock_range + '&useYfid=true&corsDomain=finance.yahoo.com'
                            data = requests.get(yahoo_url, headers=headers).json()
                            most_recent_close = data['chart']['result'][0]['meta']['regularMarketPrice']
                            old_close = data['chart']['result'][0]['meta']['chartPreviousClose']
                            percent_change = (100 * most_recent_close / old_close) - 100
                            data = {"stock": final_symbol1, "postcount": str(x), "price": str(most_recent_close), "percentchange": str(round(percent_change, 2))}
                            time.sleep(1)

                            symbol_count.append(data)
                        except:
                            print('error ', final_symbol1)
            self.data[timeframe] = sorted(symbol_count, key=lambda d: int(d["postcount"]), reverse=True)

def update_data():
    while True:
        for subreddit in subreddit_list:
            sub_data[subreddit] = sub(subreddit)
            sub_data[subreddit].set_data()
        time.sleep(1800)


app = Flask(__name__)

def main_api():
    @app.route("/", methods=['GET'])
    def home():
        my_resp = make_response('Hello :)')
        my_resp.headers['Access-Control-Allow-Origin'] = '*'
        return my_resp

    @app.route("/reddit_<name>", methods=['GET'])
    def subreddit_data(name):
        if name in subreddit_list:
            resp = make_response(sub_data[name].data)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        return "No data found"

    if __name__ == "__main__":
        app.run()


Thread(target=main_api).start()
Thread(target=update_data).start()
