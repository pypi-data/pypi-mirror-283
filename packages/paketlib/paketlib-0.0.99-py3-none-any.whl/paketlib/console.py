from pystyle import Colors
import os

uColors = {
    '~red~': Colors.red,
    '~yellow~': Colors.yellow,
    '~cyan~': Colors.cyan,
    '~blue~': Colors.blue,
    '~green~': Colors.green,
    '~pink~': Colors.pink,
    '~orange~': Colors.orange,
    '~gray~': Colors.gray,
    '~purple~': Colors.purple,
    '~bold~': '\033[1m',
    '~reset~': Colors.reset 
}

class Console:
    def __init__(self) -> None:
        self.format = '[~path~] ~green~$~reset~ '
        self.path = '~'
        self.inputstr = ''
        if os.system('cls') != 0:
            os.system('clear')

    def __format__(self, nfpath: str) -> str:
        final = nfpath
        for signature, color in uColors.items():
            final = final.replace(signature, color)
        return final.replace('~path~', self.path)

    def print(self, txt: str) -> None:
        print('\r', txt, '\n', self.__format__(self.format), '\n', sep='', end='')

    def input(self):
        self.inputstr = input(self.__format__(self.format))
