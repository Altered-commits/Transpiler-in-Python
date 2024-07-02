'''
All valid nodes for AST defined here. Function used for Semantic Analysis built in the Node Types -> evaluateExprType
'''
from EvalTypes import determineExpressionType, invertIfIntegerType, EVAL_UINT8
from Token     import TOKEN_SUB, TOKEN_KEYWORD_NOT, tokenOperatorsToString
from Printer   import printError

#All node types defined here
class ValueNode:
    def __init__(self, value, evalType) -> None:
        self.value = value
        self.type  = evalType
    
    def __repr__(self) -> str:
        return f"{self.value}"

    def evaluateExprType(self) -> int:
        return self.type

class BinaryOperationNode:
    def __init__(self, leftExpr, operator, rightExpr) -> None:
        self.leftExpr  = leftExpr
        self.operator  = operator
        self.rightExpr = rightExpr
    
    def __repr__(self) -> str:
        return f"({self.leftExpr} {tokenOperatorsToString.get(self.operator)} {self.rightExpr})"
    
    def evaluateExprType(self) -> int:
        leftExprType  = self.leftExpr.evaluateExprType()
        rightExprType = self.rightExpr.evaluateExprType()

        return determineExpressionType(leftExprType, rightExprType, self.operator)

class UnaryOperationNode:
    def __init__(self, operator, rightExpr) -> None:
        self.operator  = operator
        self.rightExpr = rightExpr
    
    def __repr__(self) -> str:
        return f"({tokenOperatorsToString.get(self.operator)} {self.rightExpr})"
    
    def evaluateExprType(self) -> int:
        rightExprType = self.rightExpr
        shouldInvertInteger = True

        #We use loop instead of recursion now
        while isinstance(rightExprType, UnaryOperationNode):
            shouldInvertInteger = not shouldInvertInteger
            rightExprType = rightExprType.rightExpr

        #Invert integer if odd number of '-'
        if(self.operator == TOKEN_SUB):
            evalType = rightExprType.evaluateExprType()
            return invertIfIntegerType(evalType) if shouldInvertInteger else evalType

        if(self.operator == TOKEN_KEYWORD_NOT):
            return EVAL_UINT8
        
        # Raise an error if an unsupported unary operator is encountered
        printError("NodeError", f"Unsupported unary operator: {self.operator}")
    
class VariableAssignNode:
    def __init__(self, variableType, variableName, assignExpr, isReassignment = False) -> None:
        self.variableType   = variableType
        self.variableName   = variableName
        self.assignExpr     = assignExpr
        self.isReassignment = isReassignment
    
    def __repr__(self) -> str:
        if self.isReassignment:
            return f"({self.variableName} = {self.assignExpr})"
        return f"({self.variableType} {self.variableName} = {self.assignExpr});" 
    
    def evaluateExprType(self) -> int:
        #Used for reassignment of variable
        return self.variableType

class VariableAccessNode:
    def __init__(self, variableType, variableName) -> None:
        self.variableType = variableType
        self.variableName = variableName
    
    def __repr__(self) -> str:
        return f"{self.variableName}"
    
    def evaluateExprType(self) -> int:
        return self.variableType

#If -> condition, body
#Elif* -> list[Tuple[condition, body]]
#Else -> body
class IfNode:
    def __init__(self, ifCondition, ifBody, elifBlock, elseBody) -> None:
        self.ifCondition = ifCondition
        self.ifBody      = ifBody
        self.elifBlock   = elifBlock
        self.elseBody    = elseBody
    
    def __repr__(self) -> str:
        return "IF BLOCK"

    def evaluateExprType(self) -> int:
        raise NotImplementedError("no impl for IfNode")
    
class WhileNode:
    def __init__(self, whileCondition, whileBody) -> None:
        self.whileCondition = whileCondition
        self.whileBody      = whileBody
    
    def __repr__(self) -> str:
        return "WHILE BLOCK"
    
    def evaluateExprType(self) -> int:
        raise NotImplementedError("no impl for WhileNode")
    
class ForNode:
    def __init__(self, forAssignment, forCondition, forIncrement, forBody) -> None:
        self.forAssignment  = forAssignment
        self.forCondition   = forCondition
        self.forIncrement   = forIncrement
        self.forBody        = forBody

    def __repr__(self) -> str:
        return "FOR BLOCK"
    
    def evaluateExprType(self) -> int:
        raise NotImplementedError("no impl for ForNode")
    
class DoWhileNode:
    def __init__(self, dowhileCondition, dowhileBody) -> None:
        self.dowhileCondition = dowhileCondition
        self.dowhileBody      = dowhileBody

    def __repr__(self) -> str:
        return "DO-WHILE BLOCK"

    def evalauteExprType(self) -> int:
        raise NotImplementedError("no impl for DoWhileNode")    

# FUNCTIONS
class ReturnNode:
    def __init__(self, returnExpr) -> None:
        self.returnExpr = returnExpr
    
    def __repr__(self) -> str:
        return f"return {self.returnExpr}"

    def evaluateExprType(self) -> int:
        return self.returnExpr.evaluateExprType()

class FuncTemplateNode:
    def __init__(self, funcName, funcParams, funcBody) -> None:
        self.funcName   = funcName
        self.funcParams = funcParams
        self.funcBody   = funcBody

    def __repr__(self) -> str:
        return f"FunctionTemplate<{self.funcName}>"

    def evaluateExprType(self) -> int:
        raise NotImplementedError("No impl for func template node")

class FuncCallNode:
    def __init__(self, funcName, funcArgs, returnType) -> None:
        self.funcName   = funcName
        self.funcArgs   = funcArgs
        self.returnType = returnType
    
    def __repr__(self) -> str:
        args = ", ".join(repr(arg) for arg in self.funcArgs)
        return f"{self.funcName}({args})"

    def evaluateExprType(self) -> int:
        return self.returnType

class FuncDeclNode:
    def __init__(self, funcName, funcParams, funcBody, returnType, isInlineC = False, hasVargs = None, isBuiltinInlineC = None) -> None:
        self.funcName         = funcName
        self.funcParams       = funcParams #List of tuples[identifier, type] if normal function definition
        self.funcBody         = funcBody
        self.returnType       = returnType
        #Extra params for inline c functions
        self.isInlineC        = isInlineC
        self.hasVargs         = hasVargs
        self.isBuiltinInlineC = isBuiltinInlineC
    
    def __repr__(self) -> str:
        params = ", ".join(f"{paramValue}: {paramType}" for paramValue, paramType in self.funcParams)
        return f"func {self.funcName}({params}) -> {self.funcBody}"

    def evaluateExprType(self) -> int:
        raise NotImplementedError("No impl for func decl node")

class InlineCFuncNode:
    def __init__(self, inlineCCode, returnType) -> None:
        self.inlineCCode = inlineCCode
        self.returnType  = returnType
    
    def __repr__(self) -> str:
        return self.inlineCCode

    def evaluateExprType(self) -> int:
        return self.returnType