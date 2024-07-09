from termcolor import colored
from datetime import datetime

class Logger:
    def info(msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("INFO",  "light_blue")}]      : {msg}')
    
    def success(msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("SUCCESS",  "light_green")}]  : {msg}')

    def error(msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("ERROR",  "light_red")}]      : {msg}')

    def warn(msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("WARN",  "yellow")}]          : {msg}')