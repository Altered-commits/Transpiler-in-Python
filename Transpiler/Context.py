'''
Saves the current context / details of file
For now it saves line no. and col no.
'''
class Context:
    currentLine = 1
    currentCol  = 1

def updateContext(line, col):
    Context.currentLine = line
    Context.currentCol  = col

def getContext():
    return Context.currentLine, Context.currentCol