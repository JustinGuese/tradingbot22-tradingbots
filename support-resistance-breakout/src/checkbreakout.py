from datetime import datetime, timedelta
from os import environ

import numpy as np
import pandas as pd
from basebot22.basebot import BaseBot
from tqdm import tqdm

bot = BaseBot("breakout-bot-v1", backendurl = environ.get("BACKENDURL", "http://localhost:8000"))

ALLOWED_STOCKS = [
    "AAPL", "MSFT", "GOOG", "TSLA", 'AMD', 'AMZN', 'DG', 'KDP', 'LLY', 'NOC', 'NVDA', 'PGR', 'TEAM', 'UNH', 'WM',  # stocks
    # etfs
    "URTH", # iShares world
    "IWDA.AS", # world
    "EEM", # emerging markets
    # adding megatrends etfs
    "XAIX.DE", # Xtrackers Artificial Intelligence & Big Data UCITS ET
    "BTEC.L", # iShares Nasdaq US Biotechnology UCITS ETF USD (Acc) (BTEC.L)
    "L0CK.DE", # iShares Digital Security UCITS ETF (L0CK.DE)
    "2B76.DE", # iShares Automation & Robotics UCITS ETF (2B76.DE)
    "W1TA.DE", # WisdomTree Battery Solutions UCITS ETF (W1TA.DE)
    "RENW.DE", # L&G Clean Energy UCITS ETF (RENW.DE)
    "BNXG.DE", # Invesco CoinShares Global Blockchain UCITS ETF (BNXG.DE)
    # crypto
    "BTC-USD", "ETH-USD", "AVAX-USD" # crypto
]

def fix_stock_price(df: pd.DataFrame):
  df['Date'] = pd.to_datetime(df.index)
  df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
  return df

#method 1: fractal candlestick pattern
# determine bullish fractal 
def is_support(df,i):  
  cond1 = df['Low'][i] < df['Low'][i-1]   
  cond2 = df['Low'][i] < df['Low'][i+1]   
  cond3 = df['Low'][i+1] < df['Low'][i+2]   
  cond4 = df['Low'][i-1] < df['Low'][i-2]  
  return (cond1 and cond2 and cond3 and cond4) 
# determine bearish fractal
def is_resistance(df,i):  
  cond1 = df['High'][i] > df['High'][i-1]   
  cond2 = df['High'][i] > df['High'][i+1]   
  cond3 = df['High'][i+1] > df['High'][i+2]   
  cond4 = df['High'][i-1] > df['High'][i-2]  
  return (cond1 and cond2 and cond3 and cond4)
# to make sure the new level area does not exist already
def is_far_from_level(value, levels, df):    
  ave =  np.mean(df['High'] - df['Low'])    
  return np.sum([abs(value-level)<ave for _,level in levels])==0

#method 1: fractal candlestick pattern
def detect_level_method_1(df):
  levels = []
  for i in range(2,df.shape[0]-2):
    if is_support(df,i):
      l = df['Low'][i]
      if is_far_from_level(l, levels, df):
        levels.append((i,l))
    elif is_resistance(df,i):
      l = df['High'][i]
      if is_far_from_level(l, levels, df):
        levels.append((i,l))
  return levels

#method 2: window shifting method
def detect_level_method_2(df):
  levels = []
  max_list = []
  min_list = []
  for i in range(5, len(df)-5):
      high_range = df['High'][i-5:i+4]
      current_max = high_range.max()
      if current_max not in max_list:
          max_list = []
      max_list.append(current_max)
      if len(max_list) == 5 and is_far_from_level(current_max, levels, df):
          levels.append((high_range.idxmax(), current_max))
      
      low_range = df['Low'][i-5:i+5]
      current_min = low_range.min()
      if current_min not in min_list:
          min_list = []
      min_list.append(current_min)
      if len(min_list) == 5 and is_far_from_level(current_min, levels, df):
          levels.append((low_range.idxmin(), current_min))
  return levels

# to detect breakout
def has_breakout(levels, previous, last):
  for _, level in levels:
    cond1 = (previous['Open'] < level) 
    cond2 = (last['Open'] > level) and (last['Low'] > level)
  return (cond1 and cond2)

buy = dict()

for ticker in tqdm(ALLOWED_STOCKS):
    df = bot.getData(ticker, start_date = datetime.utcnow() - timedelta(days = 60)) # 2 months
    df = df[["open", "high", "low", "close", "volume"]]
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df = fix_stock_price(df)
    
    # get levels using the first method
    
    breakout = False
    levels_1 = detect_level_method_1(df)
    if (has_breakout(levels_1[-5:], df.iloc[-2], df.iloc[-1])):
        print(ticker, "has breakout method 1")
        breakout = True

    # get levels using the second method
    levels_2 = detect_level_method_2(df)
    if (has_breakout(levels_2[-5:], df.iloc[-2], df.iloc[-1])):
        print(ticker, "has breakout method 2")
        breakout = True
        
    if breakout:
        buy.update({ticker :  df.iloc[-1]['Close'] })
        
if len(buy) > 0:
    # we have to buy some
    portfolio = bot.getPortfolio()
    usd = portfolio['USD']
    
    usdPerBuy = usd / len(buy)
    
    
    # buy with stop loss take profit
    for ticker, crntPrice in buy.items():
        # TODO: find fitting values
        stopLoss = crntPrice * 1.02 # + 2 pct
        takeProfit = crntPrice * 1.05 # + 5 pct
        
        bot.buy(ticker, amount = usdPerBuy, amountInUSD = True, 
                close_if_below = stopLoss, close_if_above = takeProfit)
        print("buying ", ticker, "with stop loss ", stopLoss, "and take profit ", takeProfit)
        
        