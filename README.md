# Transpiler in Python

This Python transpiler converts custom language to C code. Made as a college project by two individuals as a part of NTCC (After we completed 2nd year at our college)

## Features
1. Preprocessor capable of handling `include` and `define` directives without the need for '#' symbol. Can access files within folders using '.' syntax. It also processes single line comments.
2. Transpiler capable of handling:
    - Primitive types such as ints, floats, chars, strings.
    - Variable assignments, re-assignments and globals.
    - Arithmetic, Logical and Comparision operators.
    - if-elif-else condition.
    - for, while and do-while loops.
    - user defined, pure inline and built-in functions.

## Usage

To use the transpiler, follow these steps:

1. **Requirements**: Make sure you have Python installed on your system.

2. **Installation**: Clone this repository or download the source code.

3. **Run the Transpiler**: Navigate to the directory containing the source code and run the transpiler using the following command:

   ```bash
   python Transpiler/Main.py filename.txt
Replace the filename.txt with name of the input file you want to transpile.

# Example
Suppose you have a file named input.txt with the following content:

### input.txt
```
var x = 10;
var y = -10;
x = y;
```
When transpiled using command `python Transpiler/Main.py intput.txt`, it generates a `Generated.c` file containing C code with proper type deduction.

### Generated.c
```c
#include <stdint.h>

int main(void)
{
    int8_t x = 10;
    int8_t y = -10;

    x = y;

    return 0;
}
```
