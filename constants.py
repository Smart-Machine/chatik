""" 
    Constants for chatik.
"""

import colorama

HOST, PORT = 'localhost', 65432
BUFSIZE = 1024

RESET = colorama.Style.RESET_ALL
USER  = colorama.Fore.LIGHTMAGENTA_EX

INFO  = f'{colorama.Fore.GREEN}[INFO]{RESET} '
ERROR = f'{colorama.Fore.RED}[ERROR]{RESET} '
LOG   = f'{colorama.Fore.BLUE}[LOG]{RESET} '

