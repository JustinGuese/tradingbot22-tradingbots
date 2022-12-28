import numpy as np
from basebot22.basebot import BaseBot

# mostly based on results of: jupyternotebooks/signalsmoothing.ipynb
bot = BaseBot("decision-tree-v2", backendurl = "http://tradingbot-baseimage-service:8000")

INDICATORS = ["volatility_dcp", "trend_aroon_ind", "momentum_rsi", "volatility_bbp", "volatility_ui", "trend_cci", "momentum_rsi"]
WEIGHTS = {'LLY': 0.012199172778563128, '2B76.DE': 0.012533468332734988, 'W1TA.DE': 0.015220246059009717, 'AAPL': 0.027340483003709472, 'NVDA': 0.027403739071673507, 'AVAX-USD': 0.14061380248945116, 'BTC-USD': 0.16483306536765613, 'TSLA': 0.24052328630924424, 'ETH-USD': 0.3593327365879577}

def getDecision(dfrow):
    # the output of the tree_to_code function, -1 indicating sell signal, 1 indicating buy signal
    if dfrow['volatility_dcp'] <= 0.48:
        if dfrow['trend_aroon_ind'] <= 30.0:
            if dfrow['momentum_rsi'] <= 44.07:
                return -1
            else:  # if dfrow['momentum_rsi'] > 44.07
                return -1
        else:  # if dfrow['trend_aroon_ind'] > 30.0
            if dfrow['volatility_bbp'] <= 0.31:
                return -1
            else:  # if dfrow['volatility_bbp'] > 0.31
                return 1
    else:  # if dfrow['volatility_dcp'] > 0.48
        if dfrow['trend_aroon_ind'] <= 10.0:
            if dfrow['volatility_bbp'] <= 0.82:
                if dfrow['volatility_ui'] <= 13.4:
                    if dfrow['trend_cci'] <= 23.59:
                        return -1
                    else:  # if dfrow['trend_cci'] > 23.59
                        return 1
                else:  # if dfrow['volatility_ui'] > 13.4
                    return -1
            else:  # if dfrow['volatility_bbp'] > 0.82
                return 1
        else:  # if dfrow['trend_aroon_ind'] > 10.0
            if dfrow['momentum_rsi'] <= 55.04:
                return 1
            else:  # if dfrow['momentum_rsi'] > 55.04
                return 1

## trade logic

portfolio = bot.getPortfolio()
print("current portfolio: ", portfolio)
usd = portfolio["USD"]

toBuy = []
for ticker in WEIGHTS.keys():
    df = bot.getData(ticker, technical_indicators=INDICATORS)
    df.drop(["ticker"], axis=1, inplace=True)
    # analyze last three rows to get some kind of stability
    res = np.median([getDecision(df.iloc[-i]) for i in range(1, 4)])
    # debug
    # if ticker == "LLY":
    #     res = 1
    if res == -1 and portfolio.get(ticker, 0) > 0:
        # sell
        print("selling ", ticker)
        bot.sell(ticker)
    elif res == 1 and usd > 0 and portfolio.get(ticker, 0) == 0:
        toBuy.append(ticker)
if len(toBuy) > 0:
    portfolio = bot.getPortfolio()
    usd = portfolio["USD"]
    for ticker in toBuy:
        print("buying ", ticker, " with ", usd * WEIGHTS[ticker], " USD")
        bot.buy(ticker, amount = usd * WEIGHTS[ticker], amountInUSD = True)

