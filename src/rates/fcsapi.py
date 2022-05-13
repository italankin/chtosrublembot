import logging
from datetime import date
from typing import Optional, Tuple

import requests

from rates.get_rate import GetRate, Candle

HISTORY_URL = 'https://fcsapi.com/api-v3/%s/history'
LIST_URL = 'https://fcsapi.com/api-v3/forex/list'

logger = logging.getLogger(__name__)


class FcsApi(GetRate):
    def __init__(self, access_key: str, symbols: list[str]):
        self._access_key = access_key
        self._symbols = symbols
        self._symbol_ids = None

    def candles(self, source: str, symbol: str) -> list['Candle']:
        if not self._symbol_ids:
            self._symbol_ids = self.symbol_ids()
        if self._symbol_ids:
            symbol_id = self._symbol_ids.get(symbol, None)
        else:
            symbol_id = None
        try:
            params = {
                'period': '15m',
                'level': 1,  # latest 300 candles
                'access_key': self._access_key
            }
            if symbol_id:
                params['id'] = symbol_id
            else:
                params['symbol'] = symbol
            url = HISTORY_URL % source
            response = requests.get(url, params=params)
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

    def symbol_ids(self) -> Optional[dict[str, str]]:
        try:
            params = {
                'access_key': self._access_key
            }
            response = requests.get(LIST_URL, params=params)
            if response.status_code != 200:
                logger.error(f"Received status_code={response.status_code}: {response.text}")
                return None
            json = response.json()
            if json['code'] != 200:
                logger.error(f"Received status_code={json['code']}: {json['msg']}")
                return None
            ids = {}
            for item in json['response']:
                symbol = item['symbol']
                if symbol in self._symbols:
                    ids[symbol] = item['id']
            logger.debug(f"Fetched symbol ids: {ids}")
            return ids
        except Exception as e:
            logger.error(f"Failed to fetch candles: {e}", exc_info=e)
            return None
