from game_shared import GAME_LEVELS, GAME_MODES, GAME_STATUS
from enum import EnumType

class CurrDataSingle():
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(CurrDataSingle, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return

        self.__matched_words= []
        self.__level = None
        self.__mode = None
        self.__status = GAME_STATUS.HALTED
        self.__initialized = True

    @property
    def matched_words(self):
        return self.__matched_words
    def clear_wordlist(self):
        self.__matched_words = []
    def append_matched_word(self, word: dict):
        self.__matched_words.append(word)

    def __setproperty(self, val: str, prop_name: str, enum_options: EnumType, is_allow_none: bool = True) -> True:
        res = False
        print(is_allow_none, val, [a.name for a in enum_options], (is_allow_none and not val), val in [a.value for a in enum_options])
        if (is_allow_none and not val) or val in [a.name for a in enum_options]: res = True
        else: print(f"invalid {prop_name}: {val}")
        return res

    @property
    def level(self):
        return self.__level
    @level.setter
    def level(self, lev: str):
        if self.__setproperty(lev, "level", GAME_LEVELS):
            self.__level = lev

    @property
    def mode(self):
        return self.__mode
    @mode.setter
    def mode(self, mod: str):
        if self.__setproperty(mod, "mode", GAME_MODES):
            self.__mode = mod

    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, stat: str):
        if self.__setproperty(stat, "status", GAME_STATUS, False):
            self.__status = stat
