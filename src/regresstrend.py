from basebot import BaseBot


class TrendBot(BaseBot):

    def __init__(self, name: str, stock, backendurl: str = "http://127.0.0.1:8000"):
        super().__init__(name, backendurl)
        self.stock = stock
        