'''
Project utilities collection
'''

from os import system


class Util:
    '''
    Basic display and printing utilities
    '''
    @staticmethod
    def red():
        '''
        Change color to red
        '''
        print('\u001b[31m', end='')

    @staticmethod
    def cyan():
        '''
        Change color to cyan
        '''
        print('\u001b[36m', end='')

    @staticmethod
    def white():
        '''
        Change color to white
        '''
        print('\u001b[0m', end='')

    @staticmethod
    def yellow():
        '''
        Change color to yellow
        '''
        print('\u001b[33m', end='')

    @staticmethod
    def clear() -> None:
        '''
        reset terminal screen space
        '''
        _ = system('clear')
