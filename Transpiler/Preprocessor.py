from Printer import printPreprocessorError, printWarning
from typing import Tuple

class Preprocessor:
    '''
        STAGE 0: Preprocessor runs before compiler, it's job is to handle any file includes or macro substitution\n
        Example:\n
        include txt.txt\n
        or\n
        define TRUE 1
    '''
    def __init__(self, sourceCode) -> None:
        self.sourceCode    = sourceCode
        self.macros        = dict()
        self.includedFiles = set()
        self.outputString  = str()
        self.cIncludeFiles = set()
    
    def preprocess(self) -> Tuple[str, set[str]]:
        self.preprocessInternal(self.sourceCode)
        return self.outputString, self.cIncludeFiles

    def preprocessInternal(self, source) -> None:
        for line in source:
            strippedLine = line.strip(' \n')

            if(strippedLine.startswith('__c_include__')):
                cIncludePath = strippedLine[14:].strip()
                
                if(cIncludePath in self.cIncludeFiles):
                    printWarning("PreprocessorWarning", f"'{filePath}' was already included before, ignoring this '__c_include__' directive")
                    continue
                    
                self.cIncludeFiles.add(cIncludePath)
            
            elif(strippedLine.startswith("include")):
                includePath = strippedLine[8:].strip()
                filePath    = includePath.replace('.', '/') + ".txt"

                if filePath in self.includedFiles:
                    printWarning("PreprocessorWarning", f"'{filePath}' was already included before, ignoring this 'include' directive")
                    continue
                    
                self.includedFiles.add(filePath)

                try:
                    with open(filePath) as file:
                        self.preprocessInternal(file.readlines())
                        self.outputString += '\n'

                except FileNotFoundError:
                    printPreprocessorError(f"File not found for 'include' directive: {filePath}")

            elif(strippedLine.startswith("define")):
                parts = strippedLine.split(maxsplit=2)
                
                if(len(parts) < 3):
                    printPreprocessorError("expected key and value after 'define' directive, with space")
                
                key = parts[1]
                val = parts[2]
                
                if(not key.isidentifier()):
                    printPreprocessorError(f"'key' needs to belong to alpha numeric characters, got '{key}' for 'define' directive")

                self.macros[key] = val
            
            else:
                self.preprocessLine(strippedLine)

    def preprocessLine(self, line) -> None:
        self.outputString += self.expandMacros(line) + '\n'

    def expandMacros(self, value) -> str:
        result = []
        i = 0
        n = len(value)

        while i < n:
            if value[i].isalnum() or value[i] == '_':
                start = i
                while i < n and (value[i].isalnum() or value[i] == '_'):
                    i += 1
                
                word = value[start:i]
                if word in self.macros:
                    result.append(self.expandMacros(self.macros[word]))
                else:
                    result.append(word)
            else:
                result.append(value[i])
                i += 1

        return ''.join(result)