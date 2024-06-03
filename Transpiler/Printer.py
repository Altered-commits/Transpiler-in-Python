'''
File containing functions which neatly print error/warning/success messages and if error, exit the Transpiler.\n
Coloring may not work on all terminals.\n
For windows refer to "https://learn.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences"
'''
from Context import getContext

#Define color codes (taken from blender build scripts)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printError(section, message) -> None:
    line, col = getContext()
    print(f"{bcolors.FAIL}[{section}]: {message}{bcolors.ENDC}")
    print(f"{bcolors.WARNING}[ErrorDetails] -> Line: {line}, Column: {col}{bcolors.ENDC}")
    exit(1)

def printPreprocessorError(message) -> None:
    print(f"{bcolors.FAIL}[PreprocessorError]: {message}{bcolors.ENDC}")
    exit(1)

def printWarning(section, message) -> None:
    print(f"{bcolors.WARNING}[{section}]: {message}{bcolors.ENDC}")

def printSuccess(message) -> None:
    print(f"{bcolors.OKGREEN}[TranspilationSuccess]: {message}{bcolors.ENDC}")