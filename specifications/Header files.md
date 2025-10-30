---
tags:
  - plan
  - project
  - software
---
Starting Implementation for Handling Header Files in the Compiler

To implement header file processing for the given C-to-StruixCC compiler, the following steps can be considered:


---

1. Add Preprocessing for Header Files

Header files (#include <file.h>) need to be preprocessed. Extend the code to read and process the contents of included files before parsing.

Steps:

Use a preprocessing step to handle `#include` directives.

Identify standard headers (e.g., <stdio.h>) and user-defined headers (e.g., "file.h").

For standard headers, map to predefined content or symbols.

For user-defined headers, read the file content and inline it into the source.


Example Code Addition:

```
def preprocess_header_files(code, include_paths=[]):
    """
    Process #include directives in the code and inline the content.

    Parameters:
        code (str): The C code to preprocess.
        include_paths (list): List of directories to search for header files.

    Returns:
        str: The preprocessed C code with header content inlined.
    """
    def get_header_content(header_name):
        # Handle standard headers (e.g., stdio.h)
        if header_name in ["<stdio.h>", "<stdlib.h>"]:
            return f"// Predefined content for {header_name}\n"
        
        # Handle user-defined headers
        for path in include_paths:
            header_path = f"{path}/{header_name.strip('<>\"')}"
            try:
                with open(header_path, 'r') as f:
                    return f.read()
            except FileNotFoundError:
                continue
        raise CompilationError(f"Header file {header_name} not found.")
    
    # Replace #include directives with header content
    include_pattern = r'#include\s+[<"]([^">]+)[">]'
    code = re.sub(include_pattern, lambda match: get_header_content(match.group(1)), code)
    return code
```

Integration:

Update the compile method to preprocess the code before parsing:

```
def compile(self, code, include_paths=[]):
    """
    Compile the provided C code into the target toy language.

    Parameters:
        code (str): The C source code to compile.
        include_paths (list): List of paths to search for header files.

    Returns:
        str: The compiled code in the toy language.
    """
    parser = c_parser.CParser()
    try:
        cleaned_code = preprocess_header_files(code, include_paths)
        cleaned_code = remove_comments(cleaned_code)
        ast = parser.parse(cleaned_code)
        self.visit(ast)
        if self.errors:
            raise CompilationError(f"Compilation failed with errors: {', '.join(self.errors)}.")
        return '\n'.join(self.output)
    except c_parser.ParseError as e:
        self.error(f"Syntax error: {e}")
        raise CompilationError("Compilation failed due to syntax error:") from e
```

---

2. Symbol Table Integration for Headers

Variables, constants, and function prototypes from headers must be tracked in the symbol table.

Example:

Add a symbol for printf if <stdio.h> is included.

Add predefined macros (e.g., NULL).


Code Update:

Extend the symbol_table initialization to account for included headers:

def add_predefined_symbols(self, headers):
    """
    Add symbols for predefined functions, macros, and constants from headers.

    Parameters:
        headers (list): List of included header names.
    """
    if "<stdio.h>" in headers:
        self.symbol_table["printf"] = "function"
        self.symbol_table["NULL"] = "macro"

def visit(self, node):
    """
    Override visit method to initialize symbols from headers.

    Parameters:
        node (c_ast.Node): The AST node to visit.
    """
    included_headers = self.extract_included_headers(self.output)
    self.add_predefined_symbols(included_headers)
    super().visit(node)

def extract_included_headers(self, code):
    """
    Extract the names of included headers from the code.

    Parameters:
        code (str): The source code.

    Returns:
        list: A list of included headers.
    """
    return re.findall(r'#include\s+[<"]([^">]+)[">]', code)


---

3. Handle Function Prototypes

Header files often define function prototypes. Extend visit_Decl and visit_FuncDef to differentiate between a function prototype and a definition.

Update to visit_FuncDef:

def visit_FuncDecl(self, node):
    """
    Handle function prototypes from headers.
    
    Parameters:
        node (c_ast.FuncDecl): The function declaration node.
    """
    func_name = node.type.declname
    if func_name not in self.functions:
        self.functions[func_name] = "prototype"
        self.emit(f"// Prototype: {func_name}")


---

4. Test the Implementation

To verify header file processing:

1. Create a user-defined header (e.g., utils.h) with a function prototype or macro:
```
#define PI 3.14
int add(int a, int b);

```
2. Compile a main file that includes the header:
```
#include "utils.h"
int main() {
    int x = add(5, 10);
    return x;
}
```

3. Verify:

PI is added to the symbol table.

add is registered as a function prototype.





---

This structured approach ensures scalable and modular header file support for the compiler.

