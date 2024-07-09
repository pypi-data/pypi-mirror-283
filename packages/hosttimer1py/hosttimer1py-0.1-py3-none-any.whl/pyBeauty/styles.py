# pyBeauty/styles.py
from colorama import init, Fore, Style

# Inicializa o colorama
init(autoreset=True)

def print_bold(text):
    """Imprime texto em negrito"""
    print(Style.BRIGHT + text)

def print_italic(text):
    """Imprime texto em itálico"""
    print('\033[3m' + text + '\033[0m')

def print_colored(text, color):
    """Imprime texto com a cor especificada"""
    colors = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE
    }
    print(colors.get(color, Fore.WHITE) + text)
