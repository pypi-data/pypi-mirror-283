import sys
import traceback
from termcolor import colored
from datetime import datetime

class Logger:
    def info(self, msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("INFO",  "light_blue")}]\t\t\t: {msg}')
    
    def success(self, msg: str):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored("SUCCESS",  "light_green")}]\t\t\t: {msg}')

    def error(self, msg: str):
        self._log_with_caller_info("ERROR", "light_red", msg)

    def warn(self, msg: str):
        self._log_with_caller_info("WARN", "yellow", msg)

    def _log_with_caller_info(self, level, color, msg):
        caller_frame = sys._getframe(1)
        caller_module = caller_frame.f_globals.get("__name__")
        caller_lineno = caller_frame.f_lineno
        caller_filename = caller_frame.f_code.co_filename
        caller_funcname = caller_frame.f_code.co_name

        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{colored(level, color)}] IN {caller_filename}:{caller_lineno} ({caller_funcname})\t\t\t: {msg}')