import os
import threading
import subprocess
import time

from dotenv import load_dotenv

class SpeechSingle:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(SpeechSingle, cls).__new__(cls)
                cls.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return

        load_dotenv(verbose=True, override=True)
        self.__ispi = os.getenv("ENV") == "pi"

        self.__is_speaking = False
        self.__queue = []
        self.__initialized = True

    def __subprocess_speak(self, txt):
        is_english = txt.isalpha()
        sleep_len = int(len(txt)/(5 if is_english else 2))
        subprocess.run(["espeak-ng",
                        "-v", 'en-gb' if is_english else 'cmn-latn-pinyin',
                        "-s", str(150),
                        txt])
        time.sleep(sleep_len)

    def __proccess_queue(self):
        self.__is_speaking = True

        while len(self.__queue):
            txt = self.__queue.pop(0)
            if self.__ispi: self.__subprocess_speak(txt)

        self.__is_speaking = False
        
    def speak(self,txt):
        if not txt: return

        self.__queue.append(txt)
        if not self.__is_speaking:
            self.__proccess_queue()

    def clear_queue(self):
        self.__is_speaking = False
        self.__queue = []