import praw
import json
import requests
import time
import os
from flask import Flask, make_response
from threading import Thread

client_id = os.environ.get('REDDIT_CLIENT')
client_secret = os.environ.get('REDDIT_SECRET')
username = os.environ.get('REDDIT_USERNAME')
password = os.environ.get('REDDIT_PASSWORD')


reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     username=username, password=password, user_agent='test1')

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Mobile Safari/537.36"
}

subredditlist = ['wallstreetbets', 'stocks', 'shortsqueeze', 'investing', 'options', 'stockmarket', 'daytrading']
time_list = ["day", 'week', 'month', 'year']
sub_data = {}


class sub:
    def __init__(self, sub_name):
        self.sub_name = sub_name
        self.data = ["setting up"]

    def set_data(self):
        times_combined = []
        for timeframe in time_list:
            symbolcount = []
            subreddit = reddit.subreddit(self.sub_name)
            hot_python = list(subreddit.top(timeframe, limit=100))
            time.sleep(0.5)
            with open('stocksymbols.txt', 'r') as symbolcheck:
                for line in symbolcheck:
                    x = 0
                    finalsymbol1 = str(line.rstrip('\n'))
                    finalsymbol2 = "$" + finalsymbol1
                    for submission in hot_python:
                        posttitle = submission.title
                        titlesplit = posttitle.split()
                        if finalsymbol1 in titlesplit or finalsymbol2 in titlesplit:
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
                            yahoo_url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + finalsymbol1 + '?formatted=true&crumb=jEkX0k2sA5R&lang=en-US&region=US&events=div%7Csplit&includeAdjustedClose=true&interval=1d&range=' + stock_range + '&useYfid=true&corsDomain=finance.yahoo.com'
                            data = requests.get(yahoo_url, headers=headers).json()
                            most_recent_close = data['chart']['result'][0]['meta']['regularMarketPrice']
                            old_close = data['chart']['result'][0]['meta']['chartPreviousClose']
                            percent_change = (100 * most_recent_close / old_close) - 100
                            data = {"stock": finalsymbol1, "postcount": str(x), "price": str(most_recent_close), "percentchange": str(round(percent_change, 2))}
                            time.sleep(1)

                            symbolcount.append(json.dumps(data) + ",")
                        except:
                            print('error ', finalsymbol1)
            if len(symbolcount) >= 1:
                symbolcountnew = symbolcount[:-1]
                symbolcountnew.append(symbolcount[-1][:-1])

                if timeframe != "year":
                    times_combined.append('"' + timeframe + '": [' + "".join(symbolcountnew) + '],')
                else:
                    times_combined.append('"' + timeframe + '": [' + "".join(symbolcountnew) + ']')

            self.data.clear()
            self.data.append("{" + "".join(times_combined) + "}")


def update_data():
    for subreddit in subredditlist:
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
        for subreddit in subredditlist:
            if name == subreddit:
                resp = make_response(sub_data[subreddit].data[0])
                resp.headers['Access-Control-Allow-Origin'] = '*'
                return resp
        return "No data found"

    if __name__ == "__main__":
        app.run()


Thread(target=main_api).start()
Thread(target=update_data).start()
