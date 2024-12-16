# struixCC Coding Guide

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Compiling C Code to struixLang](#compiling-c-code-to-struixlang)
- [Supported Features](#supported-features)
  - [Data Types](#data-types)
  - [Variables and Declarations](#variables-and-declarations)
  - [Operators](#operators)
  - [Control Structures](#control-structures)
  - [Functions](#functions)
  - [Arrays](#arrays)
- [Limitations and Differences from Standard C](#limitations-and-differences-from-standard-c)
  - [Unsupported Features](#unsupported-features)
  - [Scoping and Variable Lifetime](#scoping-and-variable-lifetime)
  - [Standard Libraries](#standard-libraries)
- [Helpful Features and Tips](#helpful-features-and-tips)
  - [Debugging](#debugging)
  - [Optimizing Code](#optimizing-code)
  - [Working with Arrays](#working-with-arrays)
  - [Control Flow Constructs](#control-flow-constructs)
- [Examples](#examples)
  - [Hello, World!](#hello-world)
  - [Factorial Function](#factorial-function)
  - [Array Manipulation](#array-manipulation)
  - [Control Flow Example](#control-flow-example)
- [Conclusion](#conclusion)

---

## Introduction

**struixCC** is a compiler that translates a subset of the C programming language into **struixLang**, a stack-based programming language. struixCC allows developers to write code using familiar C syntax and compiles it into struixLang code, which can then be executed within the struixLang interpreter.

This guide provides an overview of struixCC, including supported features, limitations, and helpful tips for programmers. It aims to assist developers in effectively using struixCC to write and compile C code for execution in the struixLang environment.

---

## Getting Started

### Installation

To use struixCC, ensure you have the following prerequisites:

- **Python 3.x**: struixCC is implemented in Python and requires Python 3.x.
- **Requirements**: Install necessary dependencies using `pip`:

  ```bash
  pip install -r requirements.txt
  ```

- **struixLang Interpreter**: The interpreter for executing compiled struixLang code.

### Compiling C Code to struixLang

1. **Write Your C Code**: Create a C source file (`example.c`) using the supported features of struixC.

2. **Compile Using struixCC**:

   Run the struixCC compiler to translate your C code into struixLang code:

   ```bash
   python struixCC.py example.c -o example.sx
   ```

   This command generates an output file `example.sx` containing the equivalent struixLang code.

3. **Run the struixLang Code**:

   Use the struixLang interpreter to execute the compiled code:

   ```bash
   python struixTerp.py example.sx
   ```

---

## Supported Features

struixCC supports a subset of the C programming language. Below are the key features and constructs that you can use.

### Data Types

- **Integers**: `int`
- **Floating-Point Numbers**: `float`
- **Characters**: `char`

### Variables and Declarations

- **Variable Declarations**:

  ```c
  int x;
  float y;
  char c;
  ```

- **Initialization**:

  ```c
  int x = 10;
  float y = 3.14;
  char c = 'A';
  ```

- **Assignments**:

  ```c
  x = 5;
  y = x + 2.5;
  ```

### Operators

- **Arithmetic Operators**:

  - Addition: `+`
  - Subtraction: `-`
  - Multiplication: `*`
  - Division: `/`
  - Modulus: `%`

- **Increment and Decrement**:

  - Increment: `++x`, `x++`
  - Decrement: `--x`, `x--`

- **Relational Operators**:

  - Equal to: `==`
  - Not equal to: `!=`
  - Greater than: `>`
  - Less than: `<`
  - Greater than or equal to: `>=`
  - Less than or equal to: `<=`

- **Logical Operators**:

  - Logical AND: `&&`
  - Logical OR: `||`
  - Logical NOT: `!`

- **Bitwise Operators**:

  - AND: `&`
  - OR: `|`
  - XOR: `^`
  - NOT: `~`
  - Left shift: `<<`
  - Right shift: `>>`

- **Assignment Operators**:

  - Simple assignment: `=`
  - Compound assignments: `+=`, `-=`, `*=`, `/=`, `%=`

### Control Structures

- **Conditional Statements**:

  - `if` statement:

    ```c
    if (condition) {
      // Code block
    }
    ```

  - `if-else` statement:

    ```c
    if (condition) {
      // Code block
    } else {
      // Code block
    }
    ```

  - `switch` statement:

    ```c
    switch (variable) {
      case value1:
        // Code block
        break;
      case value2:
        // Code block
        break;
      default:
        // Code block
    }
    ```

- **Switch Statements**:

  ```c
  switch (variable) {
      case value1:
          // Code block
          break;  // Terminates the case
      case value2:
          // Code block
          break;  // Terminates the case
      default:
          // Default code block
          break;  // Terminates the switch
  }
  ```

  Switch statements are supported with `break` statements terminating cases effectively:

  - When a `break` is encountered, remaining cases are skipped.
  - The `default` block is executed only if no prior case matched.

- **Loops**:

  - `for` loop:

    ```c
    for (initialization; condition; increment) {
      // Code block
      if (break_condition) {
        break;  // Terminates the loop
      }
    }
    ```

  - `while` loop:

    ```c
    while (condition) {
      // Code block
      if (break_condition) {
        break;  // Terminates the loop
      }
    }
    ```

  - `do-while` loop:

    ```c
    do {
      // Code block
      if (break_condition) {
        break;  // Terminates the loop
      }
    } while (condition);
    ```

### Functions

- **Function Definitions**:

  ```c
  return_type function_name(parameter_list) {
    // Code block
    return value;
  }
  ```

- **Function Calls**:

  ```c
  function_name(arguments);
  ```

- **Main Function**:

  The entry point of the program should be a `main` function:

  ```c
  int main() {
    // Code block
    return 0;
  }
  ```

### Arrays

- **Array Declarations**:

  ```c
  int arr[10];
  float matrix[5][5];
  ```

- **Array Initialization**:

  ```c
  int arr[3] = {1, 2, 3};
  ```

- **Accessing Elements**:

  ```c
  arr[0] = 10;
  int x = arr[2];
  ```

---

## Limitations and Differences from Standard C

struixCC aims to provide a subset of C features suitable for compilation into struixLang. Below are the limitations and differences compared to standard C on GCC/Linux.

### Unsupported Features

- **Pointers**: Pointer arithmetic and dereferencing are not supported.

- **Dynamic Memory Allocation**: Functions like `malloc`, `calloc`, `realloc`, and `free` are not available.

- **Structures, Unions, Enums**: Complex data types are not implemented.

- **Typedefs and Type Casting**: Custom type definitions and explicit type casting are not supported.

- **Preprocessor Directives**: `#include`, `#define`, and other preprocessor directives are not recognized.

- **Variable-Length Arrays**: Arrays with sizes determined at runtime are not supported.

- **Variadic Functions**: Functions with variable numbers of arguments (e.g., `printf`) are not supported.

- **Standard Library Functions**: Standard C libraries (e.g., `stdio.h`, `stdlib.h`, `math.h`) are not directly accessible.

### Scoping and Variable Lifetime

- **Global Variables**: All variables are treated with function-level scope. Global variables are not supported.

- **Block Scope**: Variables declared inside blocks (e.g., within `{}` inside loops or conditionals) are treated as function-level.

- **Lifetime**: Variables exist for the duration of the function execution.

### Standard Libraries

- **Input/Output**: Standard I/O functions like `printf` and `scanf` are not available. Use struixLang's `PRINT` and `INPUT` equivalents after compilation.

- **Math Functions**: Standard math functions are not directly accessible. Use struixLang's built-in functions or implement the functionality manually.

---

## Helpful Features and Tips

### Debugging

- **Verbose Output**: When compiling, you can enable verbose output to see the generated struixLang code for debugging purposes.

- **Error Messages**: struixC provides basic error messages. Pay attention to compiler warnings and errors to identify issues.

### Optimizing Code

- **Simplify Expressions**: Since struixCC compiles C expressions into stack operations, simplifying expressions can result in more efficient code.

- **Avoid Deep Nesting**: Excessive nesting of control structures can make the generated code complex. Keep the code structure as flat as possible.

### Working with Arrays

- **Initialize Arrays**: Always initialize arrays before use to avoid unexpected values.

- **Array Bounds**: struixCC does not enforce array bounds checking. Ensure you access valid indices to prevent runtime errors.

### Control Flow Constructs

- **Switch Statements**: `switch` statements are supported but translated into chained `if-else` constructs. For a large number of cases, consider alternative logic for efficiency.

- **Break and Continue**: `break` statements are supported within loops and switch cases. `continue` is not supported; use logic to skip iterations as needed.

---

## Examples

### Hello, World

```c
int main() {
  // Since printf is not available, we'll use struixLang's PRINT after compilation
  return 0;
}
```

**Note:** To display output, you can modify the generated struixLang code to include the `PRINT` word or use struixLang's features directly.

### Factorial Function

```c
int factorial(int n) {
  int result = 1;
  int i;
  for (i = 1; i <= n; i++) {
    result = result * i;
  }
  return result;
}

int main() {
  int number = 5;
  int fact = factorial(number);
  // Display the result using struixLang's PRINT after compilation
  return 0;
}
```

### Array Manipulation

```c
int main() {
  int arr[5];
  int i;
  for (i = 0; i < 5; i++) {
    arr[i] = i * 2;
  }
  // Access and manipulate array elements
  return 0;
}
```

### Control Flow Example

```c
int main() {
  int x = 10;
  if (x > 5) {
    x = x + 1;
  } else {
    x = x - 1;
  }

  switch (x) {
    case 10:
      // Do something
      break;
    case 11:
      // Do something else
      break;
    default:
      // Default case
      break;
  }
  return 0;
}
```

---

## Conclusion

struixCC offers a way to write programs using familiar C syntax and compile them into struixLang for execution in a stack-based environment. While it supports many fundamental features of C, there are limitations to consider.

When working with struixCC:

- **Understand the Supported Features**: Be aware of what is supported to write compatible code.

- **Adapt to Limitations**: Modify your programming approach to accommodate unsupported features.

- **Use struixLang Features**: After compilation, leverage struixLang's capabilities for input/output and other operations.

This guide serves as a starting point for developers looking to use struixCC. By keeping the limitations and differences in mind, you can effectively write and compile code for the struixLang interpreter.

Happy coding with struixCC!
