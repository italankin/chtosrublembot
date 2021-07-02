from datetime import datetime


class GetRate:
    def candles(self, symbol: str, date_from: datetime, date_to: datetime) -> list['Candle']:
        pass


class Candle:
    o: float
    c: float
    date: datetime.date

    def __init__(self, o: float, c: float, date: datetime.date):
        self.o = o
        self.c = c
        self.date = date