from Node      import *
from EvalTypes import evalTypeToString, EVAL_STRING
from Printer   import printError
from Token     import tokenOperatorsToString

class Emitter:
    '''
    STAGE 3 of Transpiler: Final stage, Emitter. Responsible for emitting C Code given AST generated by Parser
    Example: For the code given below,
    
    var a = 10;

    Generated C Code:\n
    #include <stdint.h>

    int main(void)
    {
        uint8 a = 10;\n
        return 0;
    }
    '''
    def __init__(self, parsedCode, cIncludeFiles) -> None:
        self.statements       = parsedCode[0]
        self.funcs            = parsedCode[1].values()
        self.globalVars       = parsedCode[2].values()
        self.cIncludeFiles    = cIncludeFiles
        #String repr to be written to file
        self.code             = ""
        self.indentationLevel = 0
        #Pre-cache some indentation levels
        self.identationCache  = {
            0: "",
            1: "    ",
            2: "        ",
            3: "            ",
            4: "                "
        }
    
    #------------Helper functions------------
    def incIndentationLevel(self) -> None:
        self.indentationLevel += 1
    
    def decIndentationLevel(self) -> None:
        self.indentationLevel = max(0, self.indentationLevel - 1)
    
    def getIndentation(self) -> str:
        return self.identationCache.setdefault(self.indentationLevel, " " * (self.indentationLevel * 4))

    #------------Emitter------------
    def emit(self) -> str:
        self.emitHeader()
        self.emitGlobalVars()
        self.emitUserDefinedFunctions()
        self.emitMainFunction()
        return self.code
    
    def emitGlobalVars(self) -> None:
        for var in self.globalVars:
            self.emitVariableAssignment(var[1]) #[1] is the variable assign node itself
            self.code += ';\n'
        
        self.code += '\n'

    def emitUserDefinedFunctions(self) -> None:
        for func in self.funcs:
            self.emitFunction(func)
    
    def emitFunction(self, func) -> None:
        self.code += f"{evalTypeToString(func.returnType)} {func.funcName}("
        #Parameters
        self.code += ", ".join(f"{evalTypeToString(paramType)} {paramId}" for paramId, paramType in func.funcParams)
        self.code += ")\n{\n"
        
        #Inc indentation
        self.incIndentationLevel()
        #Function body
        for statement in func.funcBody:
            self.emitStatement(statement)
        
        self.decIndentationLevel()
        self.code += "}\n\n"

    def emitHeader(self) -> None:
        for i in self.cIncludeFiles:
            self.code += f"#include <{i}>\n"
        self.code += "#include <stdint.h>\n"
    
    def emitMainFunction(self) -> None:
        #Start of main function
        self.code += "int main(void)\n{"
        self.incIndentationLevel()
        
        previousNodeType = None
        for statement in self.statements:
            # Add newline for better readability between different types of statements
            if isinstance(statement, VariableAssignNode) and isinstance(previousNodeType, VariableAssignNode):
                if statement.isReassignment != previousNodeType.isReassignment:
                    self.code += "\n"
            elif type(statement) != type(previousNodeType):
                self.code += "\n"
            
            previousNodeType = statement
            self.emitStatement(statement)
        
        self.decIndentationLevel()

        #End of main function
        self.code += "\n    return 0;\n}"

    def emitStatement(self, node, forceNoSemicolon = False) -> None:
        shouldEndWithSemic = False
        if(isinstance(node, VariableAssignNode)):
            shouldEndWithSemic = True
            self.emitVariableAssignment(node)

        elif(isinstance(node, IfNode)):
            self.emitIfNode(node)

        elif(isinstance(node, WhileNode)):
            self.emitWhileNode(node)

        elif(isinstance(node, ForNode)):
            self.emitForNode(node)

        elif(isinstance(node, DoWhileNode)):
            shouldEndWithSemic = True
            self.emitDoWhileNode(node)

        elif(isinstance(node, ReturnNode)):
            shouldEndWithSemic = True
            self.code += f"{self.getIndentation()}return "
            self.emitExpression(node.returnExpr)
        #Expression
        else:
            shouldEndWithSemic = True
            self.code += self.getIndentation()
            self.emitExpression(node)
        
        #End statements for now in ';', later we will change this
        if(shouldEndWithSemic and not forceNoSemicolon):
            self.code += ";\n"
        shouldEndWithSemic = False
    
    def emitBlock(self, block) -> None:
        self.code += " {\n"
        self.incIndentationLevel()

        for statement in block:
            self.emitStatement(statement)
        
        self.decIndentationLevel()
        
        self.code += f"{self.getIndentation()}" "}\n"
    
    def emitIfNode(self, node) -> None:
        self.code += f"{self.getIndentation()}if ("
        self.emitExpression(node.ifCondition)
        self.code += ")"

        self.emitBlock(node.ifBody)

        #If the list isn't empty, else if exists
        if(node.elifBlock != []):
            for condition, body in node.elifBlock:
                self.code += f"{self.getIndentation()}else if ("
                self.emitExpression(condition)
                self.code += ")"

                self.emitBlock(body)
        
        if(node.elseBody != None):
            self.code += f"{self.getIndentation()}else"
            self.emitBlock(node.elseBody)

    def emitWhileNode(self, node) -> None:
        self.code += f"{self.getIndentation()}while ("
        self.emitExpression(node.whileCondition)
        self.code += ")"
        self.emitBlock(node.whileBody)  

    def emitForNode(self, node) -> None:
        self.code += f"{self.getIndentation()}for ("

        oldIndentationLevel = self.indentationLevel
        self.indentationLevel = 0

        self.emitStatement(node.forAssignment, True)
        self.code += "; "
        self.emitExpression(node.forCondition)
        self.code += "; "
        self.emitExpression(node.forIncrement)
        self.code += ")"

        self.indentationLevel = oldIndentationLevel
        self.emitBlock(node.forBody)

    def emitDoWhileNode(self, node) -> None:
        self.code += f"{self.getIndentation()}do"
        self.emitBlock(node.dowhileBody)
        self.code += f"{self.getIndentation()}while ("
        self.emitExpression(node.dowhileCondition)
        self.code += ")" 

    def emitVariableAssignment(self, node) -> None:
        if(node.isReassignment):
            self.code += f"{self.getIndentation()}{node.variableName} = "
            self.emitExpression(node.assignExpr)
        else:
            #String needs special initialization
            if(node.variableType == EVAL_STRING):
                bufferSize = 128 #Default buffer size for empty string initializations
                stringLen  = 0
                #Strings cannot be with other operators, hence when we assign a string, chances are, its going to be a single value node
                if(isinstance(node.assignExpr, ValueNode)):
                    #An empty string only consists of two quotes, min size -> 2
                    stringLen = len(node.assignExpr.value)
                    if stringLen != 2:
                        self.code += f"{self.getIndentation()}char {node.variableName}[{stringLen - 1}] = {node.assignExpr}"
                    else:
                        self.code += f"{self.getIndentation()}char {node.variableName}[{bufferSize}]"
                else:
                    printError("EmitterError", "Found other node instead of ValueNode for string")
            
            #For other variables its normal initialization
            else:
                cType = evalTypeToString(node.variableType)
                if cType is None:
                    printError("EmitterError", f"Unsupported cType: {node.variableType}")
                
                self.code += f"{self.getIndentation()}{cType} {node.variableName} = "
                self.emitExpression(node.assignExpr)
    
    def emitExpression(self, node) -> None:
        if(isinstance(node, InlineCFuncNode)):
            self.code += f"{node.inlineCCode}"

        elif isinstance(node, BinaryOperationNode):
            self.emitExpression(node.leftExpr)
            self.code += f" {tokenOperatorsToString[node.operator]} "
            self.emitExpression(node.rightExpr)

        elif isinstance(node, UnaryOperationNode):
            self.code += f"{tokenOperatorsToString[node.operator]}("
            self.emitExpression(node.rightExpr)
            self.code += ")"

        elif isinstance(node, ValueNode):
            self.code += f"{node.value}"
        
        elif isinstance(node, ParenthesizedNode):
            self.code += "("
            self.emitExpression(node.expr)
            self.code += ")"

        elif isinstance(node, VariableAccessNode):
            self.code += f"{node.variableName}"
        
        #Re-assignment
        elif isinstance(node, VariableAssignNode):
            #Temporarily reset indentation for nested expressions like these
            oldIndentationLevel = self.indentationLevel
            self.indentationLevel = 0

            self.emitVariableAssignment(node)

            self.indentationLevel = oldIndentationLevel
        
        elif isinstance(node, FuncCallNode):
            self.code += f"{node.funcName}("
            #Args
            argLen = len(node.funcArgs)
            for idx, arg in enumerate(node.funcArgs):
                self.emitExpression(arg)
                if(idx < argLen - 1):
                    self.code += ", "
            
            #Closing parentheses
            self.code += ")"