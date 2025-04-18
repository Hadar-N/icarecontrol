import os
import threading
import subprocess
import time
import queue
import re
from dotenv import load_dotenv

from static.consts import FIND_SYLLABLES_PATTERN, SYLLABLES_PER_SECOND_WAIT

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

        self.__queue = queue.Queue()
        self.__stop_event = threading.Event()

        self.__thread = threading.Thread(target=self.__process_queue_loop, daemon=True)
        self.__thread.start()

        self.__initialized = True

    def __count_syllables(self, txt:str) -> int:
        matches = re.findall(FIND_SYLLABLES_PATTERN, txt, re.IGNORECASE)
        return len(matches)

    def __subprocess_speak(self, txt):
        is_english = txt.isascii()
        sleep_len = (self.__count_syllables(txt) if is_english else len(txt))/SYLLABLES_PER_SECOND_WAIT

        subprocess.run(["espeak-ng",
                        "-v", 'en-gb' if is_english else 'cmn-latn-pinyin',
                        "-s", str(150),
                        txt])
        time.sleep(sleep_len)

    def __process_queue_loop(self):
        while not self.__stop_event.is_set():
            try:
                txt = self.__queue.get(timeout=0.1)
                if self.__ispi:
                    self.__subprocess_speak(txt)
                self.__queue.task_done()
            except queue.Empty:
                continue

    def speak(self, txt):
        if txt:
            self.__queue.put(txt)

    def clear_queue(self):
        while not self.__queue.empty():
            try:
                self.__queue.get_nowait()
                self.__queue.task_done()
            except queue.Empty:
                break

    @classmethod
    def stop(cls):
        if hasattr(cls._instance, "_SpeechSingle__stop_event"):
            cls._instance.__stop_event.set()
            cls._instance.__thread.join()