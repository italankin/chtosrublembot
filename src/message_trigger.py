from typing import Pattern, Optional


class MessageTrigger:
    fullmatch: Pattern
    substring: Optional[Pattern]
    symbol: str
    source: str
    captions: list[str]

    def __init__(self, fullmatch: Pattern, substring: Optional[Pattern], source: str, symbol: str, captions: list[str]):
        self.fullmatch = fullmatch
        self.substring = substring
        self.source = source
        self.symbol = symbol
        self.captions = captions
