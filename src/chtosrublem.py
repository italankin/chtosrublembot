import io
import logging
from datetime import timezone, datetime, timedelta
from typing import Optional

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from rates.get_rate import GetRate, Candle

logger = logging.getLogger(__name__)

MAX_STEPS_BACK = 7
RESULTS_THRESHOLD = 10
DAYS_DELTA = 3
VALUE_THRESHOLD = 0.05


class ChtoSRublem:
    _get_rate: GetRate

    def __init__(self, get_rate: GetRate):
        self._get_rate = get_rate

    def status(self, symbol: str) -> 'Status':
        candles = self._candles(symbol)
        if len(candles) == 0:
            raise ValueError('No data available')
        plot = self._make_plot(symbol, candles)
        return Status(text='', plot=plot)

    def _candles(self, symbol: str) -> list[Candle]:
        start = datetime.now(timezone.utc)
        result: list[Candle] = []
        step = 0
        while True:
            step = step + 1
            end = start - timedelta(days=DAYS_DELTA)
            candles = self._get_rate.candles(symbol, date_from=end, date_to=start)
            for c in reversed(candles):
                result.insert(0, c)
            if len(result) > RESULTS_THRESHOLD:
                return result
            if step >= MAX_STEPS_BACK:
                break
            start = start - timedelta(days=DAYS_DELTA)
        return result

    def _make_plot(self, symbol: str, candles: list[Candle]) -> Optional[io.BytesIO]:
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
            ax.set_title(f"{symbol} ({date_text})")
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
