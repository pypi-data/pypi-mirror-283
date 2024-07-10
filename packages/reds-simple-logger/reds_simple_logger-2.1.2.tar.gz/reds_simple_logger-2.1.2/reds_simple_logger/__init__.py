from termcolor import colored
from datetime import datetime

class Logger:
    def info(self, msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("INFO",  "light_blue")}]\t\t: {msg}')
    
    def success(self, msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("SUCCESS",  "green")}]\t\t: {msg}')

    def error(self, msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("ERROR",  "red")}]\t\t: {msg}')

    def warn(self, msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("WARN",  "yellow")}]\t\t: {msg}')

    def working(self, msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("WORKING",  "cyan")}]\t\t: {msg}')

    def waiting(self, msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("WAITING",  "light_grey")}]\t\t: {msg}')