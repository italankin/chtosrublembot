import io
import logging
from datetime import datetime
from typing import Optional

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from messengers.messenger import Messenger
from rates.get_rate import GetRate, Candle

logger = logging.getLogger(__name__)


class ChtoSRublem:
    _get_rate: GetRate
    _messenger: Messenger

    def __init__(self, get_rate: GetRate, messenger: Messenger):
        self._get_rate = get_rate
        self._messenger = messenger

    def status(self, source: str, symbol: str) -> Optional['Status']:
        candles = self._candles(source, symbol)
        if len(candles) == 0:
            raise None
        plot = self._make_plot(symbol, candles)
        return Status(text=self._messenger.caption(symbol), plot=plot)

    def _candles(self, source: str, symbol: str) -> list[Candle]:
        return self._get_rate.candles(source, symbol)

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

            fig = Figure(figsize=(5, 3))
            ax: Axes = fig.add_subplot(111)
            ax.set_title(f"{symbol} ({date_text})")
            ax.margins(0)
            ax.yaxis.grid(True, linestyle=':')
            ax.set_xticklabels([])
            ax.xaxis.set_tick_params(which='both', length=0)
            ax.plot(values)
            ax.text(x=len(values) - 1, y=values[-1], s=str(values[-1]))
            fig.tight_layout(pad=1.04)

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
