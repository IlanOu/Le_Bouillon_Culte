"""
How to use this gist ?
Debug :
Debug.Log("Hello World !")
Debug.LogError("Hello World !")
Debug.LogWarning("Hello World !")
Debug.LogSuccess("Hello World !")
Debug.LogWhisper("Hello World !")
Colors :
print(Colors.WARNING + "Hello" + Colors.ENDC)
print(Colors.BLUE + "Hello" + Colors.ENDC)
print(Colors.HEADER + "Hello" + Colors.ENDC)
print(Colors.UNDERLINE + "Hello" + Colors.ENDC)
"""


import datetime
import inspect
import sys

class Style:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'

    RED = '\033[31m'
    BLACK = '\033[30m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GREY = '\033[37m'
    DARK_GRAY = '\033[90m'

    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

    RESET = '\033[0m'
    SEPARATOR = '- ' * 40 + '\n'


class Debug:
    verbose = True
    prefixActive = True
    blocking = True
    emojisActive = True

    @staticmethod
    def _get_log_prefix(level, class_name, func_name, line_number):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        class_name_str = str(class_name)
        func_name_str = str(func_name)

        if class_name_str == "__main__" or class_name_str == "str":
            class_name_str = ""
        else:
            class_name_str += " : "

        if func_name_str == "<module>":
            func_name_str = ""
        else:
            func_name_str += "() "

        prefix = f"{Style.DIM}{Style.SEPARATOR}{level}[{current_time}] \n{Style.BOLD}{class_name_str}{func_name_str}{Style.RESET}{level}{Style.DIM}Line {line_number}:{Style.RESET} \n"
        return prefix

    @staticmethod
    def _log(message, level=Style.DARK_GRAY):
        frame = inspect.currentframe().f_back.f_back
        line_number = frame.f_lineno
        class_name = frame.f_locals.get('self', '__main__').__class__.__name__
        func_name = frame.f_code.co_name
        prefix = ""

        if Debug.prefixActive:
            prefix = Debug._get_log_prefix(level, class_name, func_name,
                                        line_number)

        print(f"{level}{prefix}{level}{message}{Style.RESET}")

    @staticmethod
    def Log(message):
        Debug._log(message)

    @staticmethod
    def LogWhisper(message):
        if Debug.verbose:
            Debug._log(message, Style.DARK_GRAY + Style.DIM + Style.ITALIC)

    @staticmethod
    def LogSuccess(message):
        if Debug.emojisActive:
            message = "✅ - " + message
        Debug._log(message, Style.OK_GREEN)

    @staticmethod
    def LogWarning(message):
        if Debug.emojisActive:
            message = "❕ - " + message
        Debug._log(message, Style.WARNING)

    @staticmethod
    def LogError(message):
        Debug.prefixActive = True
        Debug._log("❌ - " + message, Style.FAIL + Style.BOLD)
        if Debug.blocking == True:
            sys.exit()
        Debug.prefixActive = False
        
    

    @staticmethod
    def LogColor(message, style=Style.RESET):
        if isinstance(style, list):
            style = "".join(style)
        Debug._log(style + message, Style.WARNING)
