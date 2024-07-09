import inspect
from termcolor import colored
from datetime import datetime

class Logger:
    def info(self, msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("INFO",  "light_blue")}]      : {msg}')
    
    def success(self, msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("SUCCESS",  "light_green")}]   : {msg}')

    def error(self, msg: str):
        caller_frame = inspect.getframe(1)
        caller_class = caller_frame.f_locals["self"].__class__.__name__ if "self" in caller_frame.f_locals else ""
        caller_method = caller_frame.f_code.co_name
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("ERROR",  "light_red")}]      : IN {caller_class}.{caller_method} {msg}')

    def warn(self, msg: str):
        caller_frame = inspect.getframe(1)
        caller_class = caller_frame.f_locals["self"].__class__.__name__ if "self" in caller_frame.f_locals else ""
        caller_method = caller_frame.f_code.co_name
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("WARN",  "yellow")}]          : IN {caller_class}.{caller_method} {msg}')