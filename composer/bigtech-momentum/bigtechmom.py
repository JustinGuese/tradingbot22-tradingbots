from datetime import datetime, timedelta

from basebot22.basebot import BaseBot

STOCKS = ["META", "AMZN", "AAPL", "MSFT", "GOOG", "PYPL", "ADBE", "NVDA"]
# get 20d cumulative return
bot = BaseBot("composer-bigtechmomentum-v1", backendurl = "http://tradingbot-baseimage-service:8000")
cumret = dict()
for ticker in STOCKS:
    df = bot.getData(ticker, start_date = datetime.now() - timedelta(days=35))
    # calculate the cumulative return 20d
    df["20d_cumulative_return"] = (df["close"] / df["close"].shift(20)) - 1
    cumret[ticker] = df["20d_cumulative_return"].iloc[-1]

# sort by cumulative return descending
cumret = {k: v for k, v in sorted(cumret.items(), key=lambda item: item[1], reverse=True)}
print("cumret: ", cumret)
biggestTwo = list(cumret.keys())[:2]
portfolio = bot.getPortfolio()
usd = bot.getPortfolioWorth()
if biggestTwo[0] not in portfolio:
    portfolio[biggestTwo[0]] = 0
if biggestTwo[1] not in portfolio:
    portfolio[biggestTwo[1]] = 0

for ticker, amount in portfolio.items():
    if ticker != "USD":
        if ticker not in biggestTwo:
            print("selling all shares of ", ticker)
            bot.sell(ticker)
        else:
            # ticker is in the top 2 and we have some already
            targetUSD = usd / 2
            crntPrice = bot.getCurrentPrice(ticker)
            holdingUSD = crntPrice * amount
            diff = targetUSD - holdingUSD
            if abs(diff) > 100:
                # only act if the difference is more than 100 dollatz
                if diff > 0:
                    cash = bot.getPortfolio()["USD"]
                    if cash >= diff:
                        # buy
                        print("buying", ticker, "for", diff, "USD")
                        bot.buy(ticker, amount = diff, amountInUSD = True)
                    else:
                        # maybe error?
                        print("not enough cash to execute buy. cash: ", cash, "diff: ", diff)
                else:
                    # sell
                    bot.sell(ticker, amount = abs(diff), amountInUSD = True)