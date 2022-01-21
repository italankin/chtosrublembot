from messengers.messenger import Messenger


class NoOpMessenger(Messenger):
    def caption(self, symbol: str) -> str:
        return ''
