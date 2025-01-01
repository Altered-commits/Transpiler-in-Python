'''
Given a list of tokens it simply advances, used for function templates.
'''

from Token import TOKEN_EOF, Token

class TokenAdvancer:
    def __init__(self, tokensList) -> None:
        self.tList = tokensList
        self.tLen  = len(tokensList)
        self.tIdx  = 0
        self.tEOF  = Token("\0", TOKEN_EOF)
        self.tCur  = self.tList[0] if self.tLen > 0 else self.tEOF
    
    def advance(self):
        self.tIdx += 1
        self.tCur = self.tList[self.tIdx] if self.tIdx < self.tLen else self.tEOF
    
    #Keeping the name same to have compatibility with lexer.getToken() or lexer.peekToken()
    def peekToken(self, _):
        #The reason why we dont do + 1 to tIdx is, its already ahead, as getToken() advances it before returning so its ahead one token
        return self.tList[self.tIdx] if self.tIdx < self.tLen else self.tEOF

    def getToken(self, _):
        token = self.tCur
        self.advance()
        return token