import logging
from datetime import date

import requests

from rates.get_rate import GetRate, Candle

HISTORY_URL = 'https://fcsapi.com/api-v3/forex/history'

logger = logging.getLogger(__name__)


class FcsApi(GetRate):
    def __init__(self, access_key: str):
        self._access_key = access_key

    def candles(self, symbol: str) -> list['Candle']:
        try:
            params = {
                'symbol': symbol,
                'period': '15m',
                'level': 1,  # latest 300 candles
                'access_key': self._access_key
            }
            response = requests.get(HISTORY_URL, params=params)
            if response.status_code != 200:
                logger.error(f"Received status_code={response.status_code}: {response.text}")
                return []
            json = response.json()
            if json['code'] != 200:
                logger.error(f"Received status_code={json['code']}: {json['msg']}")
                return []
            candles = []
            for timestamp, candle in json['response'].items():
                d = date.fromtimestamp(int(timestamp))
                candles.append(Candle(float(candle['o']), float(candle['c']), d))
            return candles
        except Exception as e:
            logger.error(f"Failed to fetch candles: {e}", exc_info=e)
            return []
