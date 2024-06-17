'''
Some functions for formatting builtins like printf, scanf, etc.
'''
from Printer   import printError
from EvalTypes import evalTypeToString, EVAL_FLOAT32, EVAL_FLOAT64, EVAL_INT8, EVAL_INT16, EVAL_INT32, EVAL_INT64,\
                                        EVAL_UINT8, EVAL_UINT16, EVAL_UINT32, EVAL_UINT64, EVAL_STRING, EVAL_VOID
from Node      import VariableAccessNode

INLINE_PRINTF = 0
INLINE_SCANF  = 1
INLINE_FGETS  = 2

def builtinCFunc(func, args): #func -> FuncDeclNode, args -> Any valid AST node
    funcType = func.isBuiltinInlineC

    if(funcType == INLINE_PRINTF):
        return builtinPrintFormatting(func, args)
    elif(funcType == INLINE_SCANF):
        return builtinScanFormatting(args)
    elif(funcType == INLINE_FGETS):
        return builtinFGetsFormatting(args)

    printError("BuiltinError", f"Invalid builtin type specified for function '{func.funcName}'")

def builtinPrintFormatting(func, args):
    #Check if first arg matches the type (string) or not
    funcParams = func.funcParams
    userArgs   = args

    firstParamType = funcParams[0][1]
    firstArgType   = userArgs[0].evaluateExprType()
    
    if(firstArgType != firstParamType):
        printError("BuiltinError", f"First argument of 'print' needs to be a string type, got '{evalTypeToString(firstArgType)}'")
    
    #Initial function name
    funcName = f"printf({userArgs[0]}"
    hasVargs = len(userArgs) > 1
    vargs = []

    if(hasVargs):
        for i in userArgs[1:]:
            vargs.append(i.__repr__())

        #If only one varg, join wont add ',' by default
        funcName += ", " + ", ".join(vargs)

    funcName += ')'

    return funcName

def builtinScanFormatting(args):
    #Formats such as %d, %c, etc.
    formatMap = {
        EVAL_FLOAT32: "%f",          #float
        EVAL_FLOAT64: "%lf",         #double
        EVAL_INT8:    "%hhd",        #signed char
        EVAL_INT16:   "%hd",         #short
        EVAL_INT32:   "%d",          #int
        EVAL_INT64:   "%lld",        #long long
        EVAL_UINT8:   "%hhu",        #unsigned char
        EVAL_UINT16:  "%hu",         #unsigned short
        EVAL_UINT32:  "%u",          #unsigned int
        EVAL_UINT64:  "%llu",        #unsigned long long
        EVAL_STRING:  "%s"           #string (char array)
    }

    #Few things for scanf, we need to generate formatted string on our own
    #Second, we only want variables to be present (VariableAccessNode specifically), for address
    if(args == []):
        printError("BuiltinError", f"Expected minimum 1 argument for 'input' function, got 0")

    formatString = ""
    params = []

    for identifier in args:
        if(not isinstance(identifier, VariableAccessNode)):
            printError("BuiltinError", f"Invalid argument '{identifier}', 'input' expects pure variable arguments")
        
        idType = identifier.evaluateExprType()
        if(idType == EVAL_VOID):
            printError("BuiltinError", f"Argument '{identifier}' is a 'void' type, it is not a valid type for 'input' function")

        formatString += formatMap[idType]
        params.append(identifier.__repr__())

    #We join '&' for every variable for their address
    params = ', &'.join(params)
    return f"scanf(\"{formatString}\", &{params})"

def builtinFGetsFormatting(args):
    argsLen = len(args)
    if(argsLen != 1):
        printError("BuiltinError", f"Function 'stringInput' expects 1 argument got {argsLen}")
    
    if(not isinstance(args[0], VariableAccessNode)):
        printError("BuiltinError", f"Function 'stringInput' expects arguments to be pure variable type")

    argType = args[0].evaluateExprType()
    
    if(argType != EVAL_STRING):
        printError("BuiltinError", f"Function 'stringInput' expects argument to be of string type, got '{evalTypeToString(argType)}'")
    
    argId = args[0].__repr__()

    return f"fgets({argId}, sizeof({argId}), stdin)"