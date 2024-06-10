'''
Saves the current context / details of file, along with function context as well
'''
class Context:
    currentLine = 1
    currentCol  = 1

def updateContext(line, col) -> None:
    Context.currentLine = line
    Context.currentCol  = col

def getContext() -> tuple[int, int]:
    return Context.currentLine, Context.currentCol

#Very simple function context
class FunctionContext:
    def __init__(self) -> None:
        self.isFunc      = False
        self.canReturn   = False
        self.funcName    = ""
        self.mangledName = ""
    
    def saveFunctionContext(self, canReturn, funcName, mangledName) -> dict:
        # Save previous states
        prevContext = {
            'isFunc': self.isFunc,
            'canReturn': self.canReturn,
            'funcName': self.funcName,
            'mangledName': mangledName
        }
        
        # Set new states
        self.canReturn   = canReturn
        self.funcName    = funcName
        self.mangledName = mangledName
        self.isFunc      = True

        return prevContext

    def isFuncCurrently(self) -> bool:
        return self.isFunc

    def getFunctionContext(self) -> tuple[bool, str, str]:
        return (self.canReturn, self.funcName, self.mangledName)

    def resetFunctionContext(self, context) -> None:
        self.canReturn  = context['canReturn']
        self.funcName   = context['funcName']
        self.isFunc     = context['isFunc']
