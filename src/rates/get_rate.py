from datetime import datetime


class GetRate:
    def candles(self, source: str, symbol: str) -> list['Candle']:
        pass


class Candle:
    o: float
    c: float
    date: datetime.date

    def __init__(self, o: float, c: float, date: datetime.date):
        self.o = o
        self.c = c
        self.date = date
