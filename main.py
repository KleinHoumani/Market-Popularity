import praw
import json
import requests
import time
import os
from flask import Flask, jsonify, make_response

client_id = os.environ.get('REDDIT_CLIENT')
client_secret = os.environ.get('REDDIT_SECRET')
password = os.environ.get('REDDIT_PASSWORD')


reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     username='thederpytroller', password=password, user_agent='test1')


subredditlist = ['wallstreetbets', 'stocks']
time_list = ["day", 'week', 'month', 'year']

reddit_wallstreetbets_list = []
reddit_stocks_list = []

for sub_name in subredditlist:
    times_combined = []
    for timeframe in time_list:
        stocklist = []
        symbolcount = []
        x = 0
        subreddit = reddit.subreddit(sub_name)
        hot_python = list(subreddit.top(timeframe, limit=50))
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
                if x >= 1:
                    symbolcount.append('{\n' + '"stock": ' + '"' + str(finalsymbol1) + '",\n' + '"postcount": ' +
                                       '"' + str(x) + '"\n},')
                x -= x

        symbolcountnew = symbolcount[:-1]
        symbolcountnew.append(symbolcount[-1][:-1])

        if timeframe != "year":
            times_combined.append('"' + timeframe + '": [' + "".join(symbolcountnew) + '],')
        else:
            times_combined.append('"' + timeframe + '": [' + "".join(symbolcountnew) + ']')

    print(times_combined)
    if sub_name == "wallstreetbets":
        reddit_wallstreetbets_list.append("".join(times_combined))
    if sub_name == "stocks":
        reddit_stocks_list.append("".join(times_combined))


app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    my_resp = make_response('test')
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
