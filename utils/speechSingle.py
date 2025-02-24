import os
import json
import threading
import pyttsx3

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
        self.__espeak_engine = pyttsx3.init(driverName='espeak') if os.getenv("ENV") == "pi" else pyttsx3.init()
        self.__espeak_engine.setProperty('rate', 150) # Speed of speech (default is 200)

        self.__is_speaking = False
        self.__queue = []
        self.__initialized = True

    def __proccess_queue(self):
        if not len(self.__queue):
            self.__is_speaking = False
            return
        
        self.__is_speaking = True
        txt = self.__queue.pop(0)
        self.__espeak_engine.say(f'{txt} .')
        self.__espeak_engine.runAndWait()

        self.__proccess_queue()
        
    def speak(self,txt):
        if not txt: return

        self.__queue.append(txt)
        if not self.__is_speaking:
            self.__proccess_queue()

    def clear_queue(self):
        self.__is_speaking = False
        self.__queue = []