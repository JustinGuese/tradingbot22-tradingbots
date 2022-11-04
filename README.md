individual bot needs to overwrite 
getDecision function

```
class TrendBot(BaseBot):

    def __init__(self, name: str, stock, backendurl: str = "http://127.0.0.1:8000"):
        super().__init__(name, backendurl)
        self.stock = stock
```

ALLOWED_STOCKS = [
    "AAPL", "MSFT", "GOOG", "TSLA", 'AMD', 'AMZN', 'DG', 'KDP', 'LLY', 'NOC', 'NVDA', 'PGR', 'TEAM', 'UNH', 'WM',  # stocks
    "CWEG.L", "IWDA.AS", "EEM", # etfs
    "BTC-USD", "ETH-USD", "AVAX-USD" # crypto
]