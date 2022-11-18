from os import environ

import finnhub

from basebot import BaseBot

TRADEABLE = [
  "AAPL",
  "MSFT",
  "GOOG",
  "TSLA",
  "AMD",
  "AMZN",
  "DG",
  "KDP",
  "LLY",
  "NOC",
  "NVDA",
  "PGR",
  "TEAM",
  "UNH",
  "WM",
  "CWEG.L",
  "IWDA.AS",
  "EEM",
  "BTC-USD",
  "ETH-USD",
  "AVAX-USD"
]

finnhub_client = finnhub.Client(api_key=environ["API_KEY"])

def numberRating(rating: dict):
    rate = 0
    rate += rating["strongBuy"] * 2
    rate += rating["buy"] * 1
    rate += rating["sell"] * -1
    rate += rating["strongSell"] * -2
    return rate

recs = dict()
for ticker in TRADEABLE:
    try:
        recs[ticker] = numberRating(finnhub_client.recommendation_trends(ticker)[0])
    except Exception as e:
        print("problem with: ", ticker)
        print(e)
    
recs = dict(sorted(recs.items(), key=lambda item: item[1], reverse=True))
# convert the number to a full rating that equals 1. total
total = sum(recs.values())
for key in recs:
    recs[key] = recs[key] / total
assert sum(recs.values()) == 1

print("my targets are: ", recs)

bot = BaseBot(f"finnhub-recommendations", backendurl = environ.get("BACKENDURL", "http://localhost:8000"))
portfolio = bot.getPortfolio()
usd = portfolio["USD"]

# first check sells
for ticker, target in recs.items():
    if ticker in portfolio and target < 0:
        print("selling ", ticker)
        bot.sell(ticker, -1)
    
portfolio = bot.getPortfolio()
usd = portfolio["USD"]
# then check buys	
for ticker, target in recs.items():
    if ticker not in portfolio and target > 0:
        print("buying ", ticker)
        bot.buy(ticker, usd * target, amountInUSD=True)
    elif ticker in portfolio and target > 0:
        diff = (target*usd) - (portfolio[ticker] * bot.getCurrentPrice(ticker))
        if diff > 0:
            print("rebalancing buy ", ticker)
            bot.buy(ticker, diff, amountInUSD=True)