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
        self.isFunc     = False
        self.canReturn  = False
        self.funcName   = ""
    
    def saveFunctionContext(self, canReturn, funcName) -> dict:
        # Save previous states
        prevContext = {
            'isFunc': self.isFunc,
            'canReturn': self.canReturn,
            'funcName': self.funcName
        }
        
        # Set new states
        self.canReturn = canReturn
        self.funcName  = funcName
        self.isFunc    = True

        return prevContext

    def isFuncCurrently(self) -> bool:
        return self.isFunc

    def getFunctionContext(self) -> tuple[bool, str]:
        return (self.canReturn, self.funcName)

    def resetFunctionContext(self, context) -> None:
        self.canReturn  = context['canReturn']
        self.funcName   = context['funcName']
        self.isFunc     = context['isFunc']
