## Changelog

---

### Refined Immediate Word Handling and Unified Scope Management (27/11/2024)

**Overview:**

- **Immediate Word Behavior:**
  - Immediate word termination (`DEF`...`END`) is unified under the `END` keyword, deprecating the need for `IMMEND`. This simplification enables handling of both regular and immediate words seamlessly.

- **Scope Management:**
  - Introduced `newBlockScope` and `newAotScope` methods for consistent management of runtime and AOT workflows.
  - Replaced the legacy compile stack model with a unified scoped stack and dictionary structure.

- **Error Handling:**
  - Improved error reporting for undefined symbols or misuse of immediate words during runtime or preprocessing.

- **Removed Features:**
  - Removed `IMMEND` as `END` now handles all cases.

**Impact:**

- Enhanced predictability and reduced complexity for immediate word handling.
- Simplified syntax for users with the removal of `IMMEND`.
- Improved debugging and error tracking through refined error handling.

---

### Enhance struixLang functionality and refactor modules for clarity (23/11/2024)

**Overview:**

- **Control Structure Enhancements**:
  - Added `SET_BREAK_FLAG` and `RESET_BREAK_FLAG` functions in `control_ext.sxlib` to improve handling of breakable control structures.

- **Bug Fixes**:
  - Resolved issues with logical operations in `logic_ops.sxlib` for `NAND`, `NOR`, and `XOR`.

- **Lexer Optimization**:
  - Fixed and optimized lexer behavior in `struixLexer.py` to handle multiline strings and improve tokenization accuracy.

- **Compiler Improvements**:
  - Enhanced C-to-struixLang compiler (`struixCC.py`) with better handling of switch-case flows and break statements.

- **Testing and Tools**:
  - Introduced test cases and a test case runner to validate functionality.
  - Added a library listing tool (`src/tools/list_libs.py`) to facilitate easy management of struixLang libraries.

- **Refactoring**:
  - Performed a comprehensive refactor for improved readability, maintainability, and enhanced docstrings for better documentation.

**Impact**:

- Improved functionality and reliability for struixLang users.
- Streamlined the development and debugging processes with better tooling and documentation.

---

### Introduction of struixC: A Subset of C Compiling to struixLang (22/11/2024)

**Overview:**

- **Added `struixC.py`**, a compiler that translates a subset of the C programming language into **struixLang** code.
- Enables developers to write code using familiar **C syntax** and compile it into **struixLang**, leveraging its stack-based execution model.
- Facilitates the integration of C codebases with struixLang applications, enhancing code reusability and flexibility.

**Supported Features:**

- **Function Definitions and Calls:**
  - Supports defining functions in C and invoking them within the code.
  - Manages function parameters and local symbol tables.

- **Variables and Data Types:**
  - Supports basic data types: `int`, `float`, `char`.
  - Allows array declarations and initializations with constant sizes.
  - Maintains a symbol table to track variable names, types, and scopes.

- **Control Structures:**
  - **Conditional Statements:**
    - Supports `if`, `else`, and `switch` statements.
    - Converts `switch` statements into chained `IFELSE` constructs in struixLang.
  - **Loops:**
    - Supports `for`, `while`, and `do-while` loops.
    - Translates loops using `WHILE` and `DOWHILE` primitives in struixLang.

- **Operators:**
  - **Arithmetic Operators:** `+`, `-`, `*`, `/`, `%`.
  - **Relational Operators:** `==`, `!=`, `<`, `<=`, `>`, `>=`.
  - **Logical Operators:** `&&`, `||`, `!`.
  - **Bitwise Operators:** `&`, `|`, `^`, `~`, `<<`, `>>`.
  - **Increment and Decrement Operators:** `++`, `--`.
  - **Unary Operators:** Handles unary minus, logical NOT, and bitwise NOT.

- **Array Operations:**
  - Supports array element assignment and access.
  - Uses `STORE_ITEM` and `ITEM` primitives in struixLang for array manipulations.
  - Initializes arrays with default values and handles array size declarations.

- **Functionality Enhancements:**
  - **Operator Translation:** Maps C operators to corresponding struixLang primitives.
  - **Error and Warning Handling:** Provides meaningful messages during compilation.
  - **Symbol Table Management:** Keeps track of variables and their scopes for accurate code generation.

**Limitations:**

- **Unsupported Features:**
  - **Pointers:** Pointer arithmetic and dereferencing are not supported.
  - **Complex Data Types:** Structures (`struct`), unions, and enums are not implemented.
  - **Dynamic Memory Allocation:** Functions like `malloc` and `free` are not available.
  - **Variable Scoping:** Limited to function-level scope; no block-level scoping within functions.
  - **Standard Libraries:** Standard C libraries (e.g., `stdio.h`, `stdlib.h`) are not directly supported.

- **Error Handling:**
  - Compilation errors may be general; detailed syntax error reporting is limited.
  - Unsupported C constructs may generate warnings or be ignored.

**Implementation Details:**

- **Parser Integration:**
  - Utilizes **`pycparser`** to parse C code into an Abstract Syntax Tree (AST).
  - The AST nodes are visited to generate equivalent struixLang code.

- **Compiler Structure:**
  - Implements a `ToyLangCompiler` class that extends `c_ast.NodeVisitor`.
  - Contains methods to handle various AST node types, such as `FuncDef`, `Decl`, `Assignment`, `BinaryOp`, `UnaryOp`, `If`, `Switch`, `For`, `While`, and `DoWhile`.

- **Code Generation:**
  - Maintains an output list (`self.output`) to accumulate generated struixLang code.
  - Emits code by appending to the output list and joins them into a single string upon completion.
  - Handles variable storage and retrieval using `STORE` and `FETCH` primitives.

- **Control Flow Translation:**
  - **Conditional Statements:** Converts `if` and `else` blocks into `IFTRUE`, `IFFALSE`, and `IFELSE` constructs.
  - **Loops:** Translates loops into `WHILE` and `DOWHILE` primitives with condition and body blocks.
  - **Switch Statements:** Converts `switch` cases into chained `IFELSE` statements, evaluating cases sequentially.

- **Operator Handling:**
  - Translates C operators into struixLang equivalents, ensuring correct operator precedence and associativity.
  - Supports both unary and binary operations with appropriate stack manipulation.

**Testing and Examples:**

- **Example Program:**
  - Included an example C program demonstrating:
    - Array declaration and initialization.
    - Loop constructs (`for` loops).
    - Arithmetic operations and accumulation.
    - Function definition (`main` function) and return statements.

- **Compilation and Output:**
  - The compiler processes the example C code and outputs equivalent struixLang code.
  - The generated code can be executed in the struixLang interpreter to verify correctness.

---

### 21/11/2024: Restructuring, Code Cleanup, and New Features Added

- **Updated Documentation to Include New Primitives and Features**

  - **New Data Types:**
    - **Arrays**: Introduced arrays (implemented as lists) and explained how to use them with list operations.

  - **Added New Primitives:**

    - **Mathematical Operators:**
      - **BITNOT (`~`)**: Performs bitwise NOT on the top value of the stack.

    - **Unary Operators:**
      - **NEGATE**: Negates the top value of the stack.

        ```plaintext
        10 negate print  # Outputs -10
        ```

      - **INCR**: Increments the value of a variable.

        ```plaintext
        var a
        a = 5
        a incr
        a fetch print  # Outputs 6
        ```

      - **DECR**: Decrements the value of a variable.

        ```plaintext
        var a
        a = 5
        a decr
        a fetch print  # Outputs 4
        ```

    - **List Operations:**
      - **STORE_ITEM**: Stores a value in a list at a given index.

        ```plaintext
        [ 0 0 0 ] 1 99 store_item
        pstack  # Outputs [0, 99, 0]
        ```

  - **Enhanced Control Structures:**

    - **Detailed Explanations and Usage of:**
      - **IFTRUE**, **IFFALSE**, **IFELSE**
      - **TIMES**, **WHILE**, **DOWHILE**

    - **Added Examples:**
      - Demonstrated how to use control structures in various scenarios.

  - **Expanded Built-in Functions:**

    - **Mathematical Functions:**
      - **SIN**, **COS**, **TAN**, **LOG**, **EXP**

    - **Time and Date Functions:**
      - **CURRENT_TIME**, **SLEEP**, **FORMAT_TIME**

    - **Random Number Generation:**
      - **RANDOM**, **RANDINT**, **CHOICE**

    - **File Input/Output:**
      - **OPEN_FILE**, **READ_FILE**, **WRITE_FILE**, **CLOSE_FILE**

    - **Networking Functions:**
      - **HTTP_GET**, **HTTP_POST**

  - **Improved String Manipulation:**
    - Added functions like **STRCAT**, **STRLEN**, **SUBSTR** with usage examples.

  - **Enhanced Examples Section:**

    - **New Examples Added:**
      - **Factorial Calculation**: Demonstrated using loops and variables.
      - **Fibonacci Sequence**: Showed iterative calculation using variables and loops.
      - **File Reading**: Illustrated basic file I/O operations.

  - **Abstracted Implementation Details:**

    - Removed references to custom libraries and source code.
    - Focused on providing clear documentation on how to use the available words.
    - Simplified explanations to enhance understanding without unnecessary complexity.

  - **Organized Content for Clarity:**

    - Updated the **Table of Contents** to reflect new sections and features.
    - Reorganized sections for better flow and readability.
    - Ensured consistency in formatting and examples throughout the documentation.
