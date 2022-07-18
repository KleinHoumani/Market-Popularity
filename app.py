import praw
import json
import requests
import time
import os
from flask import Flask, jsonify, make_response
from threading import Thread

client_id = os.environ.get('REDDIT_CLIENT')
client_secret = os.environ.get('REDDIT_SECRET')
password = os.environ.get('REDDIT_PASSWORD')


reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     username='thederpytroller', password=password, user_agent='test1')

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Mobile Safari/537.36"
}

subredditlist = ['wallstreetbets', 'stocks']
time_list = ["day", 'week', 'month', 'year']

reddit_wallstreetbets_list_setup = ["setting up"]
reddit_stocks_list_setup = ["setting up"]

reddit_wallstreetbets_list = ["setting up"]
reddit_stocks_list = ["setting up"]

app = Flask(__name__)
def main_api():
    @app.route("/", methods=['GET'])
    def home():
        my_resp = make_response('Hello :)')
        my_resp.headers['Access-Control-Allow-Origin'] = '*'
        return my_resp

    @app.route("/reddit_wallstreetbets", methods=['GET'])
    def reddit_wallstreetbets():
        my_resp = make_response('{\n' + reddit_wallstreetbets_list[0] + '\n}')
        my_resp.headers['Access-Control-Allow-Origin'] = '*'
        return my_resp

    @app.route("/reddit_stocks", methods=['GET'])
    def reddit_stocks():
        my_resp = make_response('{\n' + reddit_stocks_list[0] + '\n}')
        my_resp.headers['Access-Control-Allow-Origin'] = '*'
        return my_resp

    if __name__ == "__main__":
        app.run()

def set_data():
    while True:
        for sub_name in subredditlist:
            times_combined = []
            for timeframe in time_list:
                stocklist = []
                symbolcount = []
                x = 0
                subreddit = reddit.subreddit(sub_name)
                hot_python = list(subreddit.top(timeframe, limit=30))
                with open('stocksymbols.txt', 'r') as symbolcheck:
                    for line in symbolcheck:
                        finalsymbol1 = str(line.rstrip('\n'))
                        finalsymbol2 = "$" + finalsymbol1
                        for submission in hot_python:
                            posttitle = submission.title.upper()
                            titlesplit = posttitle.split()
                            if finalsymbol1 in titlesplit:
                                x += 1
                            if finalsymbol2 in titlesplit:
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

                                time.sleep(0.5)

                                symbolcount.append('{\n' + '"stock": ' + '"' + str(finalsymbol1) + '",\n' + '"postcount": ' +
                                               '"' + str(x) + '",\n' + '"price": ' + '"' + str(most_recent_close) +
                                               '",\n' + '"percentchange": ' + '"' + str(round(percent_change, 2)) + '"' + '\n},')
                            except:
                                print('error', finalsymbol1)

                            # symbolcount.append('{\n' + '"stock": ' + '"' + str(finalsymbol1) + '",\n' + '"postcount": ' +
                            #                    '"' + str(x) + '"\n},')
                        x -= x

                symbolcountnew = symbolcount[:-1]
                symbolcountnew.append(symbolcount[-1][:-1])

                if timeframe != "year":
                    times_combined.append('"' + timeframe + '": [' + "".join(symbolcountnew) + '],')
                else:
                    times_combined.append('"' + timeframe + '": [' + "".join(symbolcountnew) + ']')

            if sub_name == "wallstreetbets":
                reddit_wallstreetbets_list.clear()
                reddit_wallstreetbets_list.append("".join(times_combined))
            if sub_name == "stocks":
                reddit_stocks_list.clear()
                reddit_stocks_list.append("".join(times_combined))
        time.sleep(20)

Thread(target=main_api).start()
Thread(target=set_data).start()
