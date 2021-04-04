import logging
from datetime import datetime

import dateutil
import requests

from rates.usd_rub_rate import UsdRubRate, Candle

logger = logging.getLogger(__name__)


class TinkoffInvest(UsdRubRate):
    _figi = 'BBG0013HGFT4'  # USD000UTSTOM

    def __init__(self, token: str, base_url: str):
        self._token = token
        self._url_market_candles = f"{base_url}/market/candles"

    def candles(self, date_from: datetime, date_to: datetime) -> list[Candle]:
        try:
            params = {
                'figi': self._figi,
                'from': self._as_date_param(date_from),
                'to': self._as_date_param(date_to),
                'interval': 'hour'
            }
            headers = {'authorization': f"Bearer {self._token}"}
            response = requests.get(self._url_market_candles, params=params, headers=headers)
            if response.status_code != 200:
                logger.error(f"Received status_code={response.status_code}: {response.text}")
                return []
            print(response.text)
            json = response.json()
            json_candles = json['payload']['candles']
            candles = []
            for jc in json_candles:
                date = dateutil.parser.parse(jc['time']).date()
                candles.append(Candle(o=jc['o'], c=jc['c'], date=date))
            return candles
        except Exception as e:
            logger.error(f"Failed to fetch candles for interval=[{date_from}, {date_to}]: {e}", exc_info=e)
            return []

    @staticmethod
    def _as_date_param(date: datetime) -> str:
        return date.astimezone().isoformat(timespec='microseconds')
