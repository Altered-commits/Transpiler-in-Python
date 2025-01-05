import Preprocessor
import Parser
import Emitter
import Printer
import argparse
import time 

transpilerArgs = argparse.ArgumentParser(description="Transpile the given file into C Code")
transpilerArgs.add_argument("filename", help="Name of the file to be transpiled. [file ext -> .txt]")

args = transpilerArgs.parse_args()

fileContent = None

try:
    with open(args.filename, "r") as inFile:
        fileContent = inFile.readlines()
except (FileNotFoundError, OSError):
    Printer.printError("Transpiler", f"File not found to transpile: {args.filename}")

start = time.perf_counter()

preprocessor = Preprocessor.Preprocessor(fileContent)
preprocessedCode, cIncludeFiles = preprocessor.preprocess()
parser       = Parser.Parser(preprocessedCode)
emitter      = Emitter.Emitter(parser.parse(), cIncludeFiles)

end = time.perf_counter()

with open("Generated.c", "w") as outFile:
    outFile.write(emitter.emit())

Printer.printSuccess(f"Successfully converted the code to C Language. Time to transpile: {(end - start) * 1000} milliseconds")