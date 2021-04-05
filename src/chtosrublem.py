import io
import logging
from datetime import timezone, datetime, timedelta
from typing import Optional

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from messenger import Messenger
from rates.usd_rub_rate import Candle, UsdRubRate

logger = logging.getLogger(__name__)

MAX_STEPS_BACK = 7
RESULTS_THRESHOLD = 20
DAYS_DELTA = 3
VALUE_THRESHOLD = 0.8


class ChtoSRublem:
    _usd_rub_rate: UsdRubRate
    _messenger: Messenger

    def __init__(self, usd_rub_rate: UsdRubRate, messenger: Messenger):
        self._usd_rub_rate = usd_rub_rate
        self._messenger = messenger

    def status(self) -> 'Status':
        candles = self._candles()
        if len(candles) == 0:
            raise ValueError('No data available')
        msg = self._get_msg(candles)
        plot = self._make_plot(candles)
        return Status(text=msg, plot=plot)

    def _candles(self) -> list[Candle]:
        start = datetime.now(timezone.utc)
        result: list[Candle] = []
        step = 0
        while True:
            step = step + 1
            end = start - timedelta(days=DAYS_DELTA)
            candles = self._usd_rub_rate.candles(date_from=end, date_to=start)
            for c in reversed(candles):
                result.insert(0, c)
            if len(result) > RESULTS_THRESHOLD:
                return result
            if step >= MAX_STEPS_BACK:
                break
            start = start - timedelta(days=DAYS_DELTA)
        return result

    def _get_msg(self, candles: list[Candle]) -> str:
        last = candles[-1].c
        diff = last - candles[0].o
        if diff > VALUE_THRESHOLD:
            return self._messenger.rub_down(last)
        if diff < -VALUE_THRESHOLD:
            return self._messenger.usd_down(last)
        return self._messenger.neutral()

    def _make_plot(self, candles: list[Candle]) -> Optional[io.BytesIO]:
        try:
            values = []
            date_start: datetime.date = datetime.max.date()
            date_end: datetime.date = datetime.min.date()
            for candle in candles:
                if date_start > candle.date:
                    date_start = candle.date
                if date_end < candle.date:
                    date_end = candle.date
                values.append(candle.o)
                values.append(candle.c)
            if date_start == date_end:
                date_text = date_start.strftime('%d %b')
            else:
                date_text = f"{date_start.strftime('%d %b')} - {date_end.strftime('%d %b')}"

            fig = Figure(figsize=(4, 3))
            ax: Axes = fig.add_subplot(111)
            ax.set_title(f"USDRUB ({date_text})")
            ax.margins(0)
            ax.yaxis.grid(True, linestyle=':')
            ax.set_xticklabels([])
            ax.xaxis.set_tick_params(which='both', length=0)
            ax.plot(values)

            buf = io.BytesIO()
            fig.savefig(buf, dpi=120)
            buf.seek(0)

            return buf
        except Exception as e:
            logger.error(f"Failed to make a plot: {e}", exc_info=e)
            return None


class Status:
    text: str
    plot: Optional[bytes]

    def __init__(self, text: str, plot: Optional[io.BytesIO]):
        self.text = text
        self.plot = plot
