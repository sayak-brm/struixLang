# struixLang Documentation

## Table of Contents

- [About struixLang](#about-struixlang)
- [Use Cases](#use-cases)
- [Getting Started](#getting-started)
- [Data Types](#data-types)
- [Core Concepts](#core-concepts)
  - [The Stack](#the-stack)
  - [Words (Commands)](#words-commands)
  - [Variables and Constants](#variables-and-constants)
  - [Comments](#comments)
- [Basic Operations](#basic-operations)
  - [Input and Output](#input-and-output)
  - [Mathematical Operations](#mathematical-operations)
  - [Stack Manipulation](#stack-manipulation)
- [Advanced Operations](#advanced-operations)
  - [Logical Operations](#logical-operations)
  - [Bitwise Operations](#bitwise-operations)
  - [String Manipulation](#string-manipulation)
  - [Lists and Arrays](#lists-and-arrays)
  - [Control Structures](#control-structures)
- [Built-in Functions](#built-in-functions)
  - [Mathematical Functions](#mathematical-functions)
  - [Time and Date Functions](#time-and-date-functions)
  - [Random Number Generation](#random-number-generation)
  - [File Input/Output](#file-inputoutput)
  - [Networking Functions](#networking-functions)
- [Examples](#examples)
  - [Hello, World!](#hello-world)
  - [Factorial Calculation](#factorial-calculation)
  - [Fibonacci Sequence](#fibonacci-sequence)
  - [File Reading](#file-reading)
- [Conclusion](#conclusion)

---

## About struixLang

**struixLang** is a stack-based, case-insensitive programming language implemented in Python 3. It operates on a **stack**, which is a list of objects that the program manipulates. The language also utilizes a **dictionary** containing words (functions or commands) that can be executed within a program.

struixLang includes a rich set of built-in words and provides mechanisms for defining new user-defined words within the language itself.

---

## Use Cases

struixLang is ideal for:

- **Embedded Scripting**: Adding scripting capabilities to applications.
- **Educational Purposes**: Teaching programming concepts in a simple and interactive way.
- **Rapid Prototyping**: Quickly testing ideas and algorithms.

---

## Getting Started

To run the struixLang interpreter, execute the `repl.py` file using Python 3:

```bash
python3 repl.py
```

Alternatively, you can integrate the interpreter into your own Python programs:

```python
import struixTerp
import struixPrimitives

# Create a new interpreter instance
terp = struixTerp.Terp()

# Add built-in words to the interpreter
struixPrimitives.AddWords(terp)

# Run struixLang code
terp.run("""
    var a
    a = 10
    "The value of a is:" print
    a fetch print
""")
```

---

## Data Types

struixLang supports the following data types:

- **Integers**
- **Floats**
- **Strings**
- **Booleans**
- **Lists (Arrays)**
- **Variables**
- **Words (Functions)**

---

## Core Concepts

### The Stack

At the heart of struixLang is the **stack**. The stack operates on a Last-In-First-Out (LIFO) principle. Items are **pushed** onto the stack and **popped** off the stack during operations.

### Words (Commands)

Words are the commands or functions in struixLang. They manipulate the stack or perform actions.

- **Built-in Words**: Predefined commands provided by the language.
- **User-defined Words**: Custom commands created using `DEF` and `END`.

### Variables and Constants

- **Variables**: Named storage locations that can hold values.

  ```plaintext
  var x
  x = 42
  x fetch print
  ```

- **Constants**: Named values that cannot be changed after initialization.

  ```plaintext
  const PI 3.14159
  PI print
  ```

### Comments

Comments are used to include explanatory notes in the code and are ignored during execution.

- Single-line comments start with `#`.

  ```plaintext
  # This is a comment
  ```

---

## Basic Operations

### Input and Output

- **PRINT**: Pops and displays the top item on the stack.

  ```plaintext
  "Hello, World!" print
  ```

- **INPUT**: Prompts the user for input and pushes the entered value onto the stack.

  ```plaintext
  "Enter your name:" print
  input
  "Hello, " swap + print
  ```

- **PSTACK**: Displays all items in the stack.

  ```plaintext
  pstack
  ```

### Mathematical Operations

struixLang uses **postfix notation** (Reverse Polish Notation) for operations.

- **Addition (`+`)**

  ```plaintext
  5 3 + print  # Outputs 8
  ```

- **Subtraction (`-`)**

  ```plaintext
  10 4 - print  # Outputs 6
  ```

- **Multiplication (`*`)**

  ```plaintext
  7 6 * print  # Outputs 42
  ```

- **Division (`/`)**

  ```plaintext
  20 5 / print  # Outputs 4.0
  ```

- **Integer Division (`//`)**

  ```plaintext
  20 3 // print  # Outputs 6
  ```

- **Modulus (`%`)**

  ```plaintext
  20 3 % print  # Outputs 2
  ```

- **Exponentiation (`**`)**

  ```plaintext
  2 8 ** print  # Outputs 256
  ```

### Stack Manipulation

- **DUP**: Duplicates the top item on the stack.

  ```plaintext
  5 dup print print  # Outputs 5 twice
  ```

- **DROP**: Removes the top item from the stack.

  ```plaintext
  1 2 3 drop pstack  # Stack now has 2 and 1
  ```

- **SWAP**: Swaps the top two items on the stack.

  ```plaintext
  "World" "Hello" swap print print  # Outputs "Hello" then "World"
  ```

- **OVER**: Copies the second item on the stack and pushes it to the top.

  ```plaintext
  1 2 over print print print  # Outputs 2, 1, 2
  ```

- **ROT**: Rotates the third item to the top of the stack.

  ```plaintext
  1 2 3 rot pstack  # Stack order is now 1, 3, 2
  ```

---

## Advanced Operations

### Logical Operations

Logical operations in struixLang work with boolean values (`true` and `false`).

- **NOT**: Logical NOT operation.

  ```plaintext
  true not print  # Outputs False
  ```

- **AND**: Logical AND operation.

  ```plaintext
  true false and print  # Outputs False
  ```

- **OR**: Logical OR operation.

  ```plaintext
  true false or print  # Outputs True
  ```

- **NAND**: Logical NAND operation. Returns the negation of `AND`.

  ```plaintext
  true false nand print  # Outputs True
  true true nand print   # Outputs False
  ```

- **NOR**: Logical NOR operation. Returns the negation of `OR`.

  ```plaintext
  true false nor print   # Outputs False
  false false nor print  # Outputs True
  ```

- **XOR**: Logical XOR operation. Returns `true` if one operand is true and the other is false.

  ```plaintext
  true false xor print   # Outputs True
  true true xor print    # Outputs False
  ```

### Bitwise Operations

- **BITNOT (`~`)**: Bitwise NOT.

  ```plaintext
  5 ~ print  # Outputs -6
  ```

- **BITAND (`&`)**: Bitwise AND.

  ```plaintext
  6 3 & print  # Outputs 2
  ```

- **BITOR (`|`)**: Bitwise OR.

  ```plaintext
  6 3 | print  # Outputs 7
  ```

- **BITXOR (`^`)**: Bitwise XOR.

  ```plaintext
  6 3 ^ print  # Outputs 5
  ```

- **SHL (`<<`)**: Bitwise shift left.

  ```plaintext
  2 3 << print  # Outputs 16
  ```

- **SHR (`>>`)**: Bitwise shift right.

  ```plaintext
  16 2 >> print  # Outputs 4
  ```

### String Manipulation

- **STRCAT**: Concatenates two strings.

  ```plaintext
  "Hello, " "World!" strcat print  # Outputs "Hello, World!"
  ```

- **STRLEN**: Retrieves the length of a string.

  ```plaintext
  "Hello" strlen print  # Outputs 5
  ```

- **SUBSTR**: Extracts a substring.

  ```plaintext
  "Hello, World!" 7 12 substr print  # Outputs "World"
  ```

#### Multiline Strings

- Multiline strings are enclosed in triple quotes (`"""` or `'''`).
- They allow for more readable code when dealing with long text or multiline outputs.

  ```plaintext
  """This is a 
  multiline string""" print
  ```

- Multiline strings can also contain embedded newlines or special characters without requiring explicit escape sequences:

  ```plaintext
  """Line 1
  Line 2
  Line 3""" print
  ```

### Lists and Arrays

- **Creating Lists**:

  ```plaintext
  [ 1 2 3 4 5 ]  # Pushes a list onto the stack
  ```

- **Accessing Elements (`ITEM`)**:

  ```plaintext
  [ 10 20 30 ] 1 item print  # Outputs 20
  ```

- **Modifying Elements (`STORE_ITEM`)**:

  ```plaintext
  [ 0 0 0 ] 1 99 store_item pstack  # List becomes [0, 99, 0]
  ```

- **Getting Length (`LENGTH`)**:

  ```plaintext
  [ 1 2 3 ] length print  # Outputs 3
  ```

### Control Structures

- **Conditional Execution**:

  - **IFTRUE**: Executes a block if the condition is true.

    ```plaintext
    true [ "Condition is true" print ] iftrue
    ```

  - **IFFALSE**: Executes a block if the condition is false.

    ```plaintext
    false [ "Condition is false" print ] iffalse
    ```

  - **IFELSE**: Chooses between two blocks based on a condition.

    ```plaintext
    true [ "True block" print ] [ "False block" print ] ifelse
    ```

- **Loops**:

  - **TIMES**: Repeats a block a specified number of times.

    ```plaintext
    [ "Hello!" print ] 3 times
    ```

  - **WHILE**: Repeats a block while a condition is true.

    ```plaintext
    var i
    i = 0
    [ i fetch 5 < ] [ i fetch print i incr ] while
    ```

  - **DOWHILE**: Executes a block at least once and repeats while a condition is true.

    ```plaintext
    var i
    i = 0
    [ i fetch 3 < ] [ "Looping" print i incr ] dowhile
    ```

- **Defining Functions**:

  ```plaintext
  def greet
    "Hello from function!" print
  end

  greet  # Calls the function
  ```

---

## Built-in Functions

### Mathematical Functions

- **SIN**, **COS**, **TAN**: Trigonometric functions.

  ```plaintext
  0.5 sin print  # Outputs the sine of 0.5 radians
  ```

- **LOG**: Natural logarithm.

  ```plaintext
  10 log print  # Outputs the natural log of 10
  ```

- **EXP**: Exponential function.

  ```plaintext
  2 exp print  # Outputs e^2
  ```

### Time and Date Functions

- **CURRENT_TIME**: Gets the current timestamp.

  ```plaintext
  current_time print
  ```

- **SLEEP**: Pauses execution for a specified number of seconds.

  ```plaintext
  2 sleep  # Pauses for 2 seconds
  ```

- **FORMAT_TIME**: Formats a timestamp.

  ```plaintext
  current_time "%Y-%m-%d %H:%M:%S" format_time print
  ```

### Random Number Generation

- **RANDOM**: Generates a random float between 0 and 1.

  ```plaintext
  random print
  ```

- **RANDINT**: Generates a random integer between two values.

  ```plaintext
  1 10 randint print  # Random integer between 1 and 10
  ```

- **CHOICE**: Selects a random element from a list.

  ```plaintext
  [ "apple" "banana" "cherry" ] choice print
  ```

### File Input/Output

- **OPEN_FILE**: Opens a file.

  ```plaintext
  "r" "example.txt" open_file  # Opens file in read mode
  ```

- **READ_FILE**: Reads content from a file.

  ```plaintext
  file_variable read_file print
  ```

- **WRITE_FILE**: Writes data to a file.

  ```plaintext
  "Some data to write" file_variable write_file
  ```

- **CLOSE_FILE**: Closes a file.

  ```plaintext
  file_variable close_file
  ```

### Networking Functions

- **HTTP_GET**: Performs an HTTP GET request.

  ```plaintext
  "http://example.com" http_get print
  ```

- **HTTP_POST**: Performs an HTTP POST request.

  ```plaintext
  "http://example.com/api" "{'key':'value'}" http_post print
  ```

---

## Examples

### Hello, World

```plaintext
"Hello, World!" print
```

### Factorial Calculation

```plaintext
var n
"Enter a number:" print
input n store
var result
1 result store

[ n fetch 1 > ]  # Condition
[
  n fetch result fetch * result store
  n fetch 1 - n store
] while

"Factorial is:" print
result fetch print
```

### Fibonacci Sequence

```plaintext
var a
var b
var temp
0 a store
1 b store
10 var count count store  # Number of terms

[ count fetch 0 > ]  # Condition
[
  a fetch print
  b fetch a store
  a fetch b fetch + b store
  count fetch 1 - count store
] while
```

### File Reading

```plaintext
"r" "data.txt" open_file var file file store
file fetch read_file print
file fetch close_file
```

---

## Conclusion

struixLang is a versatile and powerful stack-based programming language that provides a rich set of features for both simple and complex programming tasks. Its simplicity and extensibility make it suitable for a wide range of applications, from scripting and automation to educational purposes.
