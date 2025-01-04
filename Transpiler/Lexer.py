from Token   import *
from Printer import printError, printWarning
from Context import updateContext

class Lexer:
    '''
    STAGE 1 of Transpiler: Lexer. Divides string into tokens to be used by Parser\n
    Example: Var a = 10;\n
    Tokens generated:\n
            \t- 'Var': Keyword\n
            \t- 'a'  : Identifier\n
            \t- '='  : Equals\n
            \t- '10' : Integer\n
    '''
    def __init__(self, sourceCode: str) -> None:
        self.text       = sourceCode
        self.textLen    = len(sourceCode)
        #------------------
        self.curIndex   = 0
        self.curChar    = sourceCode[self.curIndex] if self.textLen > 0 else '\0'
        self.curLine    = 1
        self.curCol     = 1
        self.minusCount = 0
    
    #-----------------HELPER FUNCTIONS-----------------
    #i++ but for lexer
    def advance(self, offset = 1) -> None:
        self.curIndex += offset
        self.curChar = self.text[self.curIndex] if self.curIndex < self.textLen else '\0'

        if(self.curChar == '\n'):
            self.curLine += 1
            self.curCol = 1
        else:
            self.curCol += 1

    def peekChar(self, offset) -> str:
        return self.text[self.peekIndex(offset)]

    def peekIndex(self, offset) -> int:
        calculatedOffset = self.curIndex + offset
        return calculatedOffset if calculatedOffset < self.textLen else self.textLen - 1

    def peekToken(self, isExpr) -> Token:
        #Save the current state of the lexer
        savedIndex      = self.curIndex
        savedCurChar    = self.curChar
        savedCurLine    = self.curLine
        savedCurCol     = self.curCol
        savedMinusCount = self.minusCount
        
        #Get the next token
        nextToken = self.getToken(isExpr)
        
        #Restore the lexer state
        self.curIndex   = savedIndex
        self.curChar    = savedCurChar
        self.curLine    = savedCurLine
        self.curCol     = savedCurCol
        self.minusCount = savedMinusCount

        return nextToken

    def skipSpaces(self) -> None:
        while (self.curChar in ' \t\n\r'):
            self.advance()

    #-----------------LEXING FUNCTIONS-----------------
    def lexNumeric(self) -> Token:
        dotCount   = 0
        digitCount = 0
        startPos = self.curIndex

        #Allow '-' character as well
        while (self.curChar.isdigit() or self.curChar in '.-'):
            if(self.curChar == '.'):
                dotCount += 1
            
            elif(self.curChar != '-'):
                digitCount += 1

            elif(self.curChar == '-' and digitCount != 0):
                break

            self.advance()
    
        if(dotCount > 1):
            printWarning("LexerWarning", "Multiple dots found while lexing float")

        tokenType = TOKEN_FLOAT if dotCount > 0 else TOKEN_INT
        return Token(self.text[startPos : self.curIndex], tokenType)

    def lexIdentifierOrKeyword(self) -> Token:
        startPos = self.curIndex

        while (self.curChar.isalnum() or self.curChar == "_"):
            self.advance()
        
        lexedText = self.text[startPos : self.curIndex]
        tokenType = keywordToTokenType.get(lexedText, TOKEN_IDENTIFIER)

        return Token(lexedText, tokenType)

    def lexChar(self) -> Token:
        charLiteral = None
        #Advance the starting quote
        self.advance()

        if(self.curChar == "'"):
            printError("LexerError", "Quoted character literal should contain atleast one character or escape sequence")

        #Escape sequence
        if(self.curChar == '\\'):
            self.advance()
            #Valid escape sequence: \n, \r, \t, \0, \", \', \\
            if(self.curChar in "nrt0'\"\\"):
                escapeSequences = {
                    'n': '\n',
                    'r': '\r',
                    't': '\t',
                    '0': '\0',
                    '"': '\"',
                    "'": '\'',
                    "\\": "\\"
                }
                charLiteral = escapeSequences.get(self.curChar)
                self.advance()

            #Valid Unicode escape sequence: \uFFFF (16bit), \UFFFFFFFF (32bit)
            elif(self.curChar in "uU"):
                hexDigits = 4 if self.curChar == 'u' else 8
                self.advance()
                hexValue = self.text[self.curIndex : self.peekIndex(hexDigits)]

                if all(c in '0123456789abcdefABCDEF' for c in hexValue):
                    charLiteral = chr(int(hexValue, 16))
                    self.advance(hexDigits)
                else:
                    printError("LexerError", f"Invalid Unicode escape sequence: \\{hexValue}")

            #Invalid escape sequence
            else:
                printError("LexerError", f"Invalid escape sequence: \\{self.curChar}")
                
        #Simple character
        else:
            charLiteral = self.curChar
            self.advance()
        
        if(self.curChar != "'"):
            printError("LexerError", f"Unterminated character literal, found character '{self.curChar}' instead of `'`")
        
        #Advance past the ending quote (') 
        self.advance()
        return Token(charLiteral, TOKEN_CHAR)

    def lexString(self):
        #We add `"` ourselves
        stringLiteral = "\""

        #Advance the `"`
        self.advance()

        #Strings escape sequence should not affect code generation, hence they are raw escape sequence
        rawEscapeSequences = {
            'n': '\\n',
            'r': '\\r',
            't': '\\t',
            '0': '\\0',
            '"': '\\"',
            "'": "\\'",
            "\\": "\\\\"
        }

        while self.curChar != '"' and self.curChar != '\0':
            if self.curChar == '\\':
                self.advance()
                stringLiteral += rawEscapeSequences.get(self.curChar, self.curChar)
            else:
                stringLiteral += self.curChar
            self.advance()
        
        if(self.curChar != '"'):
            printError("LexerError", f"Unterminated string literal: \"{stringLiteral}")
        self.advance()

        #Also the ending `"`
        stringLiteral += '"'
        return Token(stringLiteral, TOKEN_STRING)

    def getToken(self, isExpr) -> Token:
        while self.curChar != '\0':
            updateContext(self.curLine, self.curCol)
            self.skipSpaces()

            #We handle - manually, if we have number after - its a negative number, else its minus symbol
            if(self.curChar == '-'):
                self.minusCount += 1

                if(self.peekChar(1).isdigit() and (self.minusCount > 1 or not isExpr)):
                    numericToken = self.lexNumeric()
                    self.minusCount = 0
                    return numericToken
                
                self.advance()
                return Token("-", TOKEN_SUB)
            
            if(self.curChar == '.' and self.peekChar(1) == '.' and self.peekChar(2) == '.'):
                self.advance(3)
                return Token("...", TOKEN_ELLIPSIS)

            if(self.curChar.isdigit() or self.curChar == '.'):
                self.minusCount = 0
                return self.lexNumeric()
            
            if(self.curChar.isalpha() or self.curChar == "_"):
                self.minusCount = 0
                return self.lexIdentifierOrKeyword()
            
            if(self.curChar == "'"):
                self.minusCount = 0
                return self.lexChar()

            if(self.curChar == '"'):
                return self.lexString()

            tokenValue = self.curChar
            self.advance()

            #If the character is an =, we use the = along with the previous character
            if(self.curChar == '='):
                tokenValue += '='
                self.advance()
            
            tokenType = operatorToTokenType.get(tokenValue)
            if(tokenType == None):
                printError("LexerError", f"{tokenValue} is not a supported token")
            
            return Token(tokenValue, tokenType)

        #We are at the end so return a EOF
        return Token("EOF", TOKEN_EOF)