from enum import Enum, auto

class WordCode(Enum):
    ACCEPT = auto()
    DUPLICATE = auto()
    REJECT = auto()

class WordListCode(Enum):
    SUCCESS = auto()
    FAIL = auto()
    