# struixLang and struixCC

> A stack-based programming language and its C cross-compiler.

***Copyright 2016-2024 Sayak Brahmachari. Licensed under Apache v2.0.***

 


---

## Introduction

struixLang is a stack-based, case-insensitive, homoiconic, Turing-complete toy programming language, implemented in Python3. It operates on a stack—a dynamic list of objects—and includes a dictionary of pre-defined words (functions or subroutines). Users can define custom words directly within struixLang, making it highly extensible.

struixCC complements struixLang by acting as a lightweight C-to-struixLang compiler, enabling developers to write programs in a subset of C and compile them into struixLang's stack-based execution model. This bridges the familiarity of C syntax with the powerful simplicity of stack-based programming.


---

## Key Features

### struixLang

- Stack-based Execution: Operations are performed on a stack, with functions defined as "words" that manipulate stack values.

- Predefined Primitives: Built-in operations for arithmetic, logical manipulation, control structures, and more.

- Custom Word Definitions: Define new "words" (subroutines) directly within struixLang code.

- Homoiconicity: struixLang treats code as data, enabling advanced metaprogramming.

- Turing-complete: Capable of solving any computable problem (given sufficient resources).


### struixCC

C-to-struixLang Compiler: Translates a subset of C into struixLang for seamless execution.

Supported C Features:

- Basic data types: int, float, char.

- Arithmetic, logical, relational, and bitwise operators.

- Control structures: if, else, switch, loops (for, while, do-while).

- Functions, arrays, and local variable scopes.

- AST-based Translation: Parses C code into an Abstract Syntax Tree (AST) and generate equivalent struixLang code.

- Limitations: Does not support pointers, dynamic memory allocation, structs, or standard C libraries. *(yet)*



---

## Getting Started

### Prerequisites

- Python 3.x


### Installation

Clone the repository and navigate to the directory:

```sh
git clone https://github.com/sayak-brm/struixLang.git
cd struixLang
```

Create a python virtual environment:

```sh
python -m venv .venv
.venv/Scripts/activate
```

Activate the Virtual Environment:

- On Linux/MacOS:

  ```sh
  source venv/bin/activate
  ```

- On Windows (Command Prompt):

  ```sh
  venv\Scripts\activate
  ```

- On Windows (PowerShell):

  ```sh
  .\venv\Scripts\Activate.ps1
  ```

Install necessary packages and navigate to the `src` directory:

```sh
pip indtall -r requirements.txt
cd src
```

### Running struixLang Programs

Write a struixLang program (e.g., example.sx) and execute it using the interpreter:

```sh
python struixTerp.py example.sx
```

### Using struixCC

Write a C program (e.g., example.c) and compile it to struixLang using struixCC:

```sh
python struixCC.py example.c -o example.sx
```

Run the generated struixLang program:

```sh
python struixTerp.py example.sx
```

Or, combine both steps:

```sh
python struixCC.py -x example.c
```
---

## Documentation and Examples

Detailed documentation, including syntax, primitives, and examples, is available [here](https://github.com/sayak-brm/struixLang/blob/struixC/docs/index.md).

### Example: struixLang Program

```sx
# Example: If-Else statement

VAR a
5 a SWAP STORE          # Initialize a = 5

VAR b
a FETCH 0 >             # Check if a > 0
[ 1 b SWAP STORE ]      # If true, set b = 1
[ 2 b SWAP STORE ]      # If false, set b = 2
IFELSE                  # Execute the appropriate branch

b FETCH                 # Fetch b
RETURN                  # Return b
```

Example: C Program Compiled with struixCC

Input (example.c):

```c
// Example: While loop summing numbers
#include <stdio.h>

int main() {
    // Initialize variables
    int i = 0;        // Loop counter
    int sum = 0;      // Variable to store the sum

    // While loop: sum numbers from 0 to 4
    while (i < 5) {
        sum = sum + i;  // Add current value of i to sum
        i = i + 1;      // Increment i
    }

    // Return the final sum
    return sum;
}
```

Output (example.sx):

> Comments added later for clarity.

```sx
# Example: While loop summing numbers

IMPORT struixCC
DEF main

VAR i 0 i SWAP STORE           # Initialize i = 0
VAR sum 0 sum SWAP STORE       # Initialize sum = 0

VAR BREAK_FLAG FALSE STORE     # Flag to break loop
VAR CONTINUE_FLAG FALSE STORE  # Flag to continue loop

[ i FETCH 5 < BREAK_FLAG FETCH NOT AND ]  # While i < 5 and not BREAK_FLAG
[
    CONTINUE_FLAG FETCH NOT              # If CONTINUE_FLAG is FALSE
    [
        sum FETCH i FETCH + sum SWAP STORE  # sum += i
        i FETCH 1 + i SWAP STORE           # i++
    ] 
    IFTRUE 
    CONTINUE_FLAG FALSE STORE            # Reset CONTINUE_FLAG
]
WHILE

BREAK_FLAG DROP                          # Cleanup BREAK_FLAG
CONTINUE_FLAG DROP                       # Cleanup CONTINUE_FLAG

sum FETCH RETURN                         # Return sum
END

main PRINT                               # Execute and print result
```

Run the program using the struixLang interpreter.


---

## License

This project is licensed under the Apache License 2.0.


---

## Contributing

Contributions are welcome! Please refer to the contribution guidelines in the repository.

For issues, feature requests, or discussions, feel free to create a GitHub issue.
