from typing import Pattern, Optional


class MessageTrigger:
    fullmatch: Pattern
    substring: Optional[Pattern]
    symbol: str

    def __init__(self, fullmatch: Pattern, substring: Optional[Pattern], symbol: str):
        self.fullmatch = fullmatch
        self.substring = substring
        self.symbol = symbol
