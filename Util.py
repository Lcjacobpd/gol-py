import time
from os import system

class Util:
    @staticmethod
    def Red():
        print('\u001b[31m', end='')

    @staticmethod
    def Cyan():
        print('\u001b[36m', end='')

    @staticmethod
    def White():
        print('\u001b[0m', end='')

    @staticmethod
    def Yellow():
        print('\u001b[33m', end='')

    @staticmethod
    def clear() -> None:
        '''
        reset terminal screen space
        '''
        _ = system('clear')
