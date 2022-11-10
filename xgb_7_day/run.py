from datetime import date
from os import environ
from pathlib import Path

import numpy as np
from tqdm import tqdm
from train import loadLatest, prepareData, train

from basebot import BaseBot

# check if f"persistent/{ticker}_best_settings.json" exists
tickers = environ["TICKERS"].split(",")
for ticker in tqdm(tickers):
    print("#", ticker)
    my_file = Path(f"persistent/{ticker}_best_settings.json")
    if my_file.is_file():
        needsTraining = False
    else:
        needsTraining = True
        
    if date.today().day == 1 or needsTraining: # every monday retraining
        print("i need to re-train")
        data = prepareData(ticker, train=True)
        lastX, model = train(ticker, data)
    else:
        data = prepareData(ticker, train=False)
        # load model and best lookback
        lastX, model = loadLatest(ticker)
    # predict current
    pred = np.median(model.predict(lastX))
    pred_trans = {
        1: "buy",
        0: "sell"
    }
    print("i predict: ", pred_trans[pred])
    ## check if we should buy or sell
    bot = BaseBot(f"xgb_7_day_{ticker}", backendurl = environ.get("BACKENDURL", "http://tradingbot-baseimage-service:8000"))
    portfolio = bot.getPortfolio()
    usd = portfolio["USD"]

    if pred == 1 and usd > 10 and portfolio.get(ticker, 0) == 0:
        # buy
        bot.buy(ticker, amount = -1) # -1 means all we can
        print(f"bought {usd}$ of {ticker}")
    elif pred == 0 and portfolio.get(ticker, 0) > 0:
        # sell
        bot.sell(ticker, amount = -1) # -1 means all we can
        print(f"sold all {ticker}")
    else:
        print("nothing to do")