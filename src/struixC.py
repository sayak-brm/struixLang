import sys
from pycparser import c_parser, c_ast

class CompilationError(Exception):
    """Exception raised for errors during the compilation process."""
    pass

class StruixCC(c_ast.NodeVisitor):
    """
    A compiler that translates C code into a stack-based toy language using pycparser's AST.
    
    This class traverses the C Abstract Syntax Tree (AST) and generates corresponding
    instructions for a hypothetical stack-based language. It handles variable declarations,
    function definitions, control structures, and expressions.
    """
    
    def __init__(self):
        """Initialize the compiler with necessary data structures."""
        self.output = []               # List to collect generated code
        self.symbol_table = {}         # Tracks variables, their types, and scopes
        self.functions = {}            # Stores function definitions
        self.current_function = None   # Name of the current function being compiled
        self.errors = []               # List of compilation errors
        self.warnings = []             # List of compilation warnings

    def compile(self, code):
        """
        Compile the provided C code into the target toy language.
        
        Parameters:
            code (str): The C source code to compile.
        
        Returns:
            str: The compiled code in the toy language.
        
        Raises:
            CompilationError: If there are syntax errors or other compilation issues.
        """
        parser = c_parser.CParser()
        try:
            ast = parser.parse(code)
            self.visit(ast)
            if self.errors:
                raise CompilationError("Compilation failed with errors.")
            return '\n'.join(self.output)
        except c_parser.ParseError as e:
            self.error(f"Syntax error: {e}")
            raise CompilationError("Compilation failed due to syntax error.")

    def emit(self, code):
        """
        Append a line of code to the output.
        
        Parameters:
            code (str): The code line to emit.
        """
        self.output.append(code)

    def error(self, message):
        """
        Record a compilation error and print it to stderr.
        
        Parameters:
            message (str): The error message.
        """
        self.errors.append(message)
        print(f"Error: {message}", file=sys.stderr)

    def warning(self, message):
        """
        Record a compilation warning and print it to stderr.
        
        Parameters:
            message (str): The warning message.
        """
        self.warnings.append(message)
        print(f"Warning: {message}", file=sys.stderr)

    def visit_FuncDef(self, node):
        """
        Visit a function definition node and compile it.
        
        Parameters:
            node (c_ast.FuncDef): The function definition node.
        """
        func_name = node.decl.name
        self.current_function = func_name

        # Start function definition
        self.emit(f'DEF {func_name}')
        self.symbol_table = {}

        # Process parameters
        if isinstance(node.decl.type, c_ast.FuncDecl) and node.decl.type.args:
            for param in node.decl.type.args.params:
                var_name = param.name
                var_type = self.get_type(param.type)
                self.symbol_table[var_name] = var_type
                self.emit(f'VAR {var_name}')
                self.emit(f'{var_name} STORE')

        # Visit function body
        self.visit(node.body)

        # End function definition
        self.emit('END')
        self.current_function = None

    def get_type(self, type_node):
        """
        Determine the type of a given type node.
        
        Parameters:
            type_node (c_ast.Node): The type node to evaluate.
        
        Returns:
            str: The type as a string.
        """
        if isinstance(type_node, c_ast.TypeDecl):
            if isinstance(type_node.type, c_ast.IdentifierType):
                return type_node.type.names[0]
            else:
                return 'int'  # Default to int if unknown
        elif isinstance(type_node, c_ast.PtrDecl):
            return 'pointer'
        elif isinstance(type_node, c_ast.ArrayDecl):
            return 'array'
        elif isinstance(type_node, c_ast.FuncDecl):
            return 'function'
        else:
            return 'int'  # Default to int if unknown

    def visit_Decl(self, node):
        """
        Visit a variable declaration node and compile it.
        
        Parameters:
            node (c_ast.Decl): The declaration node.
        """
        var_name = node.name
        var_type = self.get_type(node.type)
        if var_type == 'array':
            # Handle array declarations
            array_size = self.get_array_size(node.type)
            self.symbol_table[var_name] = ('array', array_size)
            self.emit(f'VAR {var_name}')
            self.emit(f'[ {"0 " * array_size}] {var_name} STORE')  # Initialize array with zeros
            if node.init:
                self.warning(f"Array initialization not fully supported for {var_name}.")
        else:
            if var_name not in self.symbol_table:
                self.symbol_table[var_name] = var_type
                self.emit(f'VAR {var_name}')
                if node.init:
                    self.visit(node.init)
                    self.emit(f'{var_name} STORE')

    def get_array_size(self, array_decl):
        """
        Retrieve the size of an array from its declaration.
        
        Parameters:
            array_decl (c_ast.ArrayDecl): The array declaration node.
        
        Returns:
            int: The size of the array.
        """
        if isinstance(array_decl.dim, c_ast.Constant):
            return int(array_decl.dim.value)
        else:
            self.error("Array size must be a constant integer.")
            return 0

    def visit_Assignment(self, node):
        """
        Visit an assignment node and compile it.
        
        Parameters:
            node (c_ast.Assignment): The assignment node.
        """
        # Process right-hand side expression
        self.visit(node.rvalue)

        # Process left-hand side
        if isinstance(node.lvalue, c_ast.ID):
            var_name = node.lvalue.name
            if var_name not in self.symbol_table:
                # Assume int type if undeclared
                self.symbol_table[var_name] = 'int'
                self.emit(f'VAR {var_name}')
            self.emit(f'{var_name} STORE')
        elif isinstance(node.lvalue, c_ast.ArrayRef):
            # Handle array element assignment
            self.visit(node.lvalue.name)       # Array variable
            self.visit(node.lvalue.subscript)  # Index
            # The order of stack is: array variable, index, value
            self.emit('STORE_ITEM')            # Store value in array at index
        else:
            self.error(f"Unsupported assignment to {type(node.lvalue).__name__}")

    def visit_ArrayRef(self, node):
        """
        Visit an array reference node and compile it.
        
        Parameters:
            node (c_ast.ArrayRef): The array reference node.
        """
        self.visit(node.name)       # Array variable
        self.visit(node.subscript)  # Index
        # The order of stack is: array variable, index
        self.emit('ITEM')           # Retrieve item from array at index

    def visit_BinaryOp(self, node):
        """
        Visit a binary operation node and compile it.
        
        Parameters:
            node (c_ast.BinaryOp): The binary operation node.
        """
        self.visit(node.left)
        self.visit(node.right)
        op = self.translate_operator(node.op)
        if op:
            self.emit(op)
        else:
            self.error(f"Unsupported binary operator '{node.op}'")

    def visit_ID(self, node):
        """
        Visit an identifier node and compile it.
        
        Parameters:
            node (c_ast.ID): The identifier node.
        """
        var_name = node.name
        if var_name in self.symbol_table:
            self.emit(f'{var_name} FETCH')
        else:
            # It's a function call or undefined variable
            self.emit(f'{var_name}')

    def visit_Constant(self, node):
        """
        Visit a constant node and compile it.
        
        Parameters:
            node (c_ast.Constant): The constant node.
        """
        self.emit(f'{node.value}')

    def visit_Return(self, node):
        """
        Visit a return statement node and compile it.
        
        Parameters:
            node (c_ast.Return): The return statement node.
        """
        self.visit(node.expr)
        # In a stack-based language, leaving the result on the stack is sufficient

    def visit_If(self, node):
        """
        Visit an if statement node and compile it.
        
        Parameters:
            node (c_ast.If): The if statement node.
        """
        # Visit condition
        self.visit(node.cond)

        # Compile true branch
        true_branch_compiler = StruixCC()
        true_branch_compiler.symbol_table = self.symbol_table.copy()
        true_branch_compiler.visit(node.iftrue)
        true_branch_code = true_branch_compiler.output

        # Compile false branch if it exists
        if node.iffalse:
            false_branch_compiler = StruixCC()
            false_branch_compiler.symbol_table = self.symbol_table.copy()
            false_branch_compiler.visit(node.iffalse)
            false_branch_code = false_branch_compiler.output

            # Emit IFELSE with both branches
            self.emit(f'[ {" ".join(true_branch_code)} ]')
            self.emit(f'[ {" ".join(false_branch_code)} ]')
            self.emit('IFELSE')
        else:
            # Emit IFTRUE with only the true branch
            self.emit(f'[ {" ".join(true_branch_code)} ]')
            self.emit('IFTRUE')

    def visit_Switch(self, node):
        """
        Visit a switch statement node and compile it into chained if-else statements.
        
        Parameters:
            node (c_ast.Switch): The switch statement node.
        """
        self.warning("Switch statements are converted to chained if-else statements.")

        # Evaluate the switch expression
        self.visit(node.cond)
        # Store the switch expression in a variable
        self.emit('VAR SWITCH_EXPR')
        self.emit('SWITCH_EXPR STORE')

        # Process cases
        case_compiler = StruixCC()
        case_compiler.symbol_table = self.symbol_table.copy()
        case_compiler.switch_cases = []
        case_compiler.visit(node.stmt)

        # Build chained if-else
        else_code = None
        for case_value, case_code in reversed(case_compiler.switch_cases):
            # Emit code for each case
            self.emit('SWITCH_EXPR FETCH')
            self.emit(f'{case_value}')
            self.emit('==')
            self.emit(f'[ {" ".join(case_code)} ]')
            if else_code:
                self.emit(f'[ {" ".join(else_code)} ]')
                self.emit('IFELSE')
            else:
                self.emit('IFTRUE')
            else_code = self.output.copy()
            self.output = []

        # Handle default case if present
        if hasattr(case_compiler, 'default_code'):
            self.emit(f'[ {" ".join(case_compiler.default_code)} ]')
            self.emit('RUN')
        else:
            if else_code:
                self.output = else_code

        # Clean up the switch expression variable
        self.emit('SWITCH_EXPR DROP')

    def visit_Case(self, node):
        """
        Visit a case label within a switch statement and compile its body.
        
        Parameters:
            node (c_ast.Case): The case label node.
        """
        # Evaluate case value
        case_value = self.evaluate_constant(node.expr)  # Case value

        # Compile case body
        case_body_compiler = StruixCC()
        case_body_compiler.symbol_table = self.symbol_table.copy()
        for stmt in node.stmts or []:
            case_body_compiler.visit(stmt)
        case_body_code = case_body_compiler.output

        # Store case information
        if not hasattr(self, 'switch_cases'):
            self.switch_cases = []
        self.switch_cases.append((case_value, case_body_code))

    def visit_Default(self, node):
        """
        Visit a default label within a switch statement and compile its body.
        
        Parameters:
            node (c_ast.Default): The default label node.
        """
        # Compile default case body
        default_body_compiler = StruixCC()
        default_body_compiler.symbol_table = self.symbol_table.copy()
        for stmt in node.stmts or []:
            default_body_compiler.visit(stmt)
        self.default_code = default_body_compiler.output

    def evaluate_constant(self, node):
        """
        Evaluate a constant expression node.
        
        Parameters:
            node (c_ast.Node): The node to evaluate.
        
        Returns:
            str: The value of the constant as a string.
        """
        if isinstance(node, c_ast.Constant):
            return node.value
        else:
            self.error("Case value must be a constant.")
            return '0'

    def visit_While(self, node):
        """
        Visit a while loop node and compile it.
        
        Parameters:
            node (c_ast.While): The while loop node.
        """
        # Compile condition
        cond_compiler = StruixCC()
        cond_compiler.symbol_table = self.symbol_table.copy()
        cond_compiler.visit(node.cond)
        cond_code = cond_compiler.output

        # Compile loop body
        body_compiler = StruixCC()
        body_compiler.symbol_table = self.symbol_table.copy()
        body_compiler.visit(node.stmt)
        body_code = body_compiler.output

        # Emit WHILE loop with condition and body
        self.emit(f'[ {" ".join(cond_code)} ]')
        self.emit(f'[ {" ".join(body_code)} ]')
        self.emit('WHILE')

    def visit_DoWhile(self, node):
        """
        Visit a do-while loop node and compile it.
        
        Parameters:
            node (c_ast.DoWhile): The do-while loop node.
        """
        # Compile condition
        cond_compiler = StruixCC()
        cond_compiler.symbol_table = self.symbol_table.copy()
        cond_compiler.visit(node.cond)
        cond_code = cond_compiler.output

        # Compile loop body
        body_compiler = StruixCC()
        body_compiler.symbol_table = self.symbol_table.copy()
        body_compiler.visit(node.stmt)
        body_code = body_compiler.output

        # Emit DOWHILE loop with condition and body
        self.emit(f'[ {" ".join(cond_code)} ]')
        self.emit(f'[ {" ".join(body_code)} ]')
        self.emit('DOWHILE')

    def visit_For(self, node):
        """
        Visit a for loop node and compile it.
        
        Parameters:
            node (c_ast.For): The for loop node.
        """
        # Compile initialization
        if node.init:
            self.visit(node.init)

        # Compile condition
        cond_compiler = StruixCC()
        cond_compiler.symbol_table = self.symbol_table.copy()
        if node.cond:
            cond_compiler.visit(node.cond)
        else:
            # Infinite loop if no condition
            cond_compiler.emit('TRUE')
        cond_code = cond_compiler.output

        # Compile increment (next)
        next_compiler = StruixCC()
        next_compiler.symbol_table = self.symbol_table.copy()
        if node.next:
            next_compiler.visit(node.next)
        next_code = next_compiler.output

        # Compile loop body
        body_compiler = StruixCC()
        body_compiler.symbol_table = self.symbol_table.copy()
        body_compiler.visit(node.stmt)
        body_code = body_compiler.output

        # Combine body and increment
        loop_body = body_code + next_code

        # Emit WHILE loop with condition and combined body
        self.emit(f'[ {" ".join(cond_code)} ]')
        self.emit(f'[ {" ".join(loop_body)} ]')
        self.emit('WHILE')

    def visit_FuncCall(self, node):
        """
        Visit a function call node and compile it.
        
        Parameters:
            node (c_ast.FuncCall): The function call node.
        """
        # Compile arguments
        if node.args:
            for arg in node.args.exprs:
                self.visit(arg)
        # Emit function call
        func_name = node.name.name
        self.emit(func_name)

    def translate_operator(self, op):
        """
        Translate C operators to corresponding toy language operators.
        
        Parameters:
            op (str): The C operator.
        
        Returns:
            str or None: The translated operator or None if unsupported.
        """
        operator_mapping = {
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '%': '%',
            '==': '==',
            '!=': '!=',
            '<': '<',
            '<=': '<=',
            '>': '>',
            '>=': '>=',
            '&&': 'AND',
            '||': 'OR',
            '!': 'NOT',
            '~': 'BITNOT',
            '<<': '<<',
            '>>': '>>',
            '&': '&',
            '|': '|',
            '^': '^',
        }
        return operator_mapping.get(op)

    def visit_UnaryOp(self, node):
        """
        Visit a unary operation node and compile it.
        
        Parameters:
            node (c_ast.UnaryOp): The unary operation node.
        """
        op = node.op
        if op == 'p++':
            # Postfix increment
            self.visit(node.expr)
            self.emit('DUP')
            self.emit('1')
            self.emit('+')
            self.store_variable(node.expr)
        elif op == 'p--':
            # Postfix decrement
            self.visit(node.expr)
            self.emit('DUP')
            self.emit('1')
            self.emit('-')
            self.store_variable(node.expr)
        elif op == '++':
            # Prefix increment
            self.visit(node.expr)
            self.emit('1')
            self.emit('+')
            self.store_variable(node.expr)
            self.emit(f'{self.get_variable_name(node.expr)} FETCH')
        elif op == '--':
            # Prefix decrement
            self.visit(node.expr)
            self.emit('1')
            self.emit('-')
            self.store_variable(node.expr)
            self.emit(f'{self.get_variable_name(node.expr)} FETCH')
        elif op == '-':
            # Unary minus
            self.visit(node.expr)
            self.emit('NEGATE')
        elif op == '!':
            # Logical NOT
            self.visit(node.expr)
            self.emit('NOT')
        elif op == '~':
            # Bitwise NOT
            self.visit(node.expr)
            self.emit('BITNOT')
        else:
            self.error(f"Unsupported unary operator '{op}'")

    def store_variable(self, expr):
        """
        Store a computed value back to a variable.
        
        Parameters:
            expr (c_ast.Node): The expression representing the variable.
        """
        var_name = self.get_variable_name(expr)
        if var_name:
            self.emit(f'{var_name} STORE')
        else:
            self.error("Unsupported expression for increment/decrement.")

    def get_variable_name(self, expr):
        """
        Retrieve the variable name from an expression node.
        
        Parameters:
            expr (c_ast.Node): The expression node.
        
        Returns:
            str or None: The variable name or None if unsupported.
        """
        if isinstance(expr, c_ast.ID):
            return expr.name
        elif isinstance(expr, c_ast.ArrayRef):
            # Handle array element
            array_name = expr.name.name
            if array_name not in self.symbol_table:
                self.error(f"Undefined array '{array_name}'")
                return None
            self.visit(expr.name)       # Array variable
            self.visit(expr.subscript)  # Index
            # The value to store is on the stack
            # Stack order: value, array, index
            self.emit('STORE_ITEM')
            return None  # Since we handled storing, no need to return a variable name
        else:
            self.error("Unsupported expression type.")
            return None

    def visit_Compound(self, node):
        """
        Visit a compound statement node and compile its contained statements.
        
        Parameters:
            node (c_ast.Compound): The compound statement node.
        """
        for stmt in node.block_items or []:
            self.visit(stmt)

    def visit_ExprList(self, node):
        """
        Visit an expression list node and compile each expression.
        
        Parameters:
            node (c_ast.ExprList): The expression list node.
        """
        for expr in node.exprs:
            self.visit(expr)

    def visit_Cast(self, node):
        """
        Visit a cast node and compile it by ignoring the cast.
        
        Parameters:
            node (c_ast.Cast): The cast node.
        """
        # For now, ignore type casting
        self.visit(node.expr)

    def visit_TernaryOp(self, node):
        """
        Visit a ternary operation node and compile it.
        
        Parameters:
            node (c_ast.TernaryOp): The ternary operation node.
        """
        # Visit condition
        self.visit(node.cond)

        # Compile true expression
        true_compiler = StruixCC()
        true_compiler.symbol_table = self.symbol_table.copy()
        true_compiler.visit(node.iftrue)
        true_code = true_compiler.output

        # Compile false expression
        false_compiler = StruixCC()
        false_compiler.symbol_table = self.symbol_table.copy()
        false_compiler.visit(node.iffalse)
        false_code = false_compiler.output

        # Emit IFELSE with both expressions
        self.emit(f'[ {" ".join(true_code)} ]')
        self.emit(f'[ {" ".join(false_code)} ]')
        self.emit('IFELSE')

    def generic_visit(self, node):
        """
        Handle unsupported AST nodes by issuing a warning.
        
        Parameters:
            node (c_ast.Node): The AST node.
        """
        node_name = type(node).__name__
        self.warning(f"Unsupported node type '{node_name}'. Node will be ignored.")
        # Optionally, you can call super().generic_visit(node) to traverse children

    def visit_FileAST(self, node):
        """
        Visit the root of the AST, processing all top-level declarations.
        
        Parameters:
            node (c_ast.FileAST): The root AST node.
        """
        for ext in node.ext:
            self.visit(ext)


# Example usage
if __name__ == '__main__':
    c_code = r'''
    int main() {
        int arr[5];
        int i;
        for (i = 0; i < 5; i++) {
            arr[i] = i * 2;
        }
        int sum = 0;
        for (i = 0; i < 5; i++) {
            sum = sum + arr[i];
        }
        return sum;
    }
    '''

    compiler = StruixCC()
    try:
        toy_code = compiler.compile(c_code)
        print(toy_code)
    except CompilationError:
        print("Compilation failed due to errors.")
