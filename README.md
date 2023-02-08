# stock_aip

random project that calculate the aip benefit with:
- stock price history csv
- exchange rate csv

formula:

assume stock price in USD, purchase 100 EUR share every 7 days:
- giving time spam
- giving you are going to purchase 100 EUR every 7 days
- giving purchase every 7 days
- saying your next purchase day is 2023/02/9, tell the program this date
- giving stock price history csv
- giving exchange rate history csv
- (100 EUR -> USD)/share price = share purchase
- sum(above calculation in the time spam) = total share
- calculate average price per share you purchased
- (current price - avg price) * total share you have

No support of external stock price api or exchange rate api

writing this whole thing for personal memorization purpose

GH was asking me for the license so sure.

I don't know if attaching my csv will cause any problem, so I won't do that