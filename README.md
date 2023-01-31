# Reddit Stock Tracker - MarketPopularity.com

A web application that uses the Reddit API to gather post titles from different subreddits and analyzes if each title contains any stock symbols.

## Features
- Collects post titles from specified subreddits
- Analyzes the titles and counts the number of times each stock symbol is mentioned
- Displays results on the website in a table format for each subreddit
- Retrieves price data from the Yahoo Finance API for each stock that is found

## Notes
- Data may be incorrect at times due to some stock symbols also being words. For example, the stock symbol for Costco is "COST". If a post title says: "THE COST OF AAPL IS $150," COST would be added as a found symbol even though the post title wasn't referencing the stock symbol.
- Some stock symbols for very small companies that are also common words have been removed. The symbols removed can be seen in removed_stocks.txt
- Stocks recently listed won't be searched for until they are added to stock_symbols.txt

