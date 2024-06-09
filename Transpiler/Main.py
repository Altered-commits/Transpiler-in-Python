import Preprocessor
import Parser
import Emitter
import Printer
import argparse
# import Lexer

transpilerArgs = argparse.ArgumentParser(description="Transpile the given file into C Code")
transpilerArgs.add_argument("filename", help="Name of the file to be transpiled. ext -> .txt")

args = transpilerArgs.parse_args()

fileContent = None

try:
    with open(args.filename, "r") as inFile:
        fileContent = inFile.readlines()
except (FileNotFoundError, OSError):
    Printer.printError("Transpiler", f"File not found to transpile: {args.filename}")

preprocessor = Preprocessor.Preprocessor(fileContent)
parser       = Parser.Parser(preprocessor.preprocess())
emitter      = Emitter.Emitter(parser.parse())

with open("Generated.c", "w") as outFile:
    outFile.write(emitter.emit())

Printer.printSuccess("Successfully converted the code to C Language, check 'Generated.c' file")