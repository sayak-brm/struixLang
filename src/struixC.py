import sys
from pycparser import c_parser, c_ast

class CompilationError(Exception):
    pass

class StruixCC(c_ast.NodeVisitor):
    def __init__(self):
        self.output = []
        self.symbol_table = {}  # To keep track of variables, their types, and scopes
        self.functions = {}     # To store function definitions
        self.current_function = None
        self.errors = []
        self.warnings = []

    def compile(self, code):
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
        self.output.append(code)

    def error(self, message):
        self.errors.append(message)
        print(f"Error: {message}", file=sys.stderr)

    def warning(self, message):
        self.warnings.append(message)
        print(f"Warning: {message}", file=sys.stderr)

    # Visit functions
    def visit_FuncDef(self, node):
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

    # Get variable type
    def get_type(self, type_node):
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

    # Visit declarations (e.g., int x;)
    def visit_Decl(self, node):
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
        if isinstance(array_decl.dim, c_ast.Constant):
            return int(array_decl.dim.value)
        else:
            self.error("Array size must be a constant integer.")
            return 0

    # Visit assignment statements (e.g., x = 5;)
    def visit_Assignment(self, node):
        # Process right-hand side
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

    # Visit array references (e.g., arr[i])
    def visit_ArrayRef(self, node):
        self.visit(node.name)       # Array variable
        self.visit(node.subscript)  # Index
        # The order of stack is: array variable, index
        self.emit('ITEM')           # Retrieve item from array at index

    # Visit binary operations (e.g., a + b)
    def visit_BinaryOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        op = self.translate_operator(node.op)
        if op:
            self.emit(op)
        else:
            self.error(f"Unsupported binary operator '{node.op}'")

    # Visit identifiers (e.g., variable names)
    def visit_ID(self, node):
        var_name = node.name
        if var_name in self.symbol_table:
            self.emit(f'{var_name} FETCH')
        else:
            # It's a function call or undefined variable
            self.emit(f'{var_name}')

    # Visit constant values (e.g., numbers)
    def visit_Constant(self, node):
        self.emit(f'{node.value}')

    # Visit return statements
    def visit_Return(self, node):
        self.visit(node.expr)
        # In a stack-based language, leaving the result on the stack is sufficient

    # Visit if statements
    def visit_If(self, node):
        # Visit condition
        self.visit(node.cond)

        # True branch
        true_branch_compiler = StruixCC()
        true_branch_compiler.symbol_table = self.symbol_table.copy()
        true_branch_compiler.visit(node.iftrue)
        true_branch_code = true_branch_compiler.output

        # False branch
        if node.iffalse:
            false_branch_compiler = StruixCC()
            false_branch_compiler.symbol_table = self.symbol_table.copy()
            false_branch_compiler.visit(node.iffalse)
            false_branch_code = false_branch_compiler.output

            # Emit IFELSE
            self.emit(f'[ {" ".join(true_branch_code)} ]')
            self.emit(f'[ {" ".join(false_branch_code)} ]')
            self.emit('IFELSE')
        else:
            # Emit IFTRUE
            self.emit(f'[ {" ".join(true_branch_code)} ]')
            self.emit('IFTRUE')

    # Visit switch statements
    def visit_Switch(self, node):
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

        # Default case
        if hasattr(case_compiler, 'default_code'):
            self.emit(f'[ {" ".join(case_compiler.default_code)} ]')
            self.emit('RUN')
        else:
            if else_code:
                self.output = else_code

        # Clean up
        self.emit('SWITCH_EXPR DROP')

    def visit_Case(self, node):
        # Evaluate case value
        case_value = self.evaluate_constant(node.expr)  # Case value

        # Case body
        case_body_compiler = StruixCC()
        case_body_compiler.symbol_table = self.symbol_table.copy()
        for stmt in node.stmts or []:
            case_body_compiler.visit(stmt)
        case_body_code = case_body_compiler.output

        # Store case
        if not hasattr(self, 'switch_cases'):
            self.switch_cases = []
        self.switch_cases.append((case_value, case_body_code))

    def visit_Default(self, node):
        # Default case
        default_body_compiler = StruixCC()
        default_body_compiler.symbol_table = self.symbol_table.copy()
        for stmt in node.stmts or []:
            default_body_compiler.visit(stmt)
        self.default_code = default_body_compiler.output

    def evaluate_constant(self, node):
        if isinstance(node, c_ast.Constant):
            return node.value
        else:
            self.error("Case value must be a constant.")
            return '0'

    # Visit while loops
    def visit_While(self, node):
        # Condition code
        cond_compiler = StruixCC()
        cond_compiler.symbol_table = self.symbol_table.copy()
        cond_compiler.visit(node.cond)
        cond_code = cond_compiler.output

        # Loop body code
        body_compiler = StruixCC()
        body_compiler.symbol_table = self.symbol_table.copy()
        body_compiler.visit(node.stmt)
        body_code = body_compiler.output

        # Emit WHILE
        self.emit(f'[ {" ".join(cond_code)} ]')
        self.emit(f'[ {" ".join(body_code)} ]')
        self.emit('WHILE')

    # Visit do-while loops
    def visit_DoWhile(self, node):
        # Condition code
        cond_compiler = StruixCC()
        cond_compiler.symbol_table = self.symbol_table.copy()
        cond_compiler.visit(node.cond)
        cond_code = cond_compiler.output

        # Loop body code
        body_compiler = StruixCC()
        body_compiler.symbol_table = self.symbol_table.copy()
        body_compiler.visit(node.stmt)
        body_code = body_compiler.output

        # Emit DOWHILE
        self.emit(f'[ {" ".join(cond_code)} ]')
        self.emit(f'[ {" ".join(body_code)} ]')
        self.emit('DOWHILE')

    # Visit for loops
    def visit_For(self, node):
        # Initialization
        if node.init:
            self.visit(node.init)

        # Condition code
        cond_compiler = StruixCC()
        cond_compiler.symbol_table = self.symbol_table.copy()
        if node.cond:
            cond_compiler.visit(node.cond)
        else:
            # Infinite loop if no condition
            cond_compiler.emit('TRUE')
        cond_code = cond_compiler.output

        # Next (increment)
        next_compiler = StruixCC()
        next_compiler.symbol_table = self.symbol_table.copy()
        if node.next:
            next_compiler.visit(node.next)
        next_code = next_compiler.output

        # Loop body code
        body_compiler = StruixCC()
        body_compiler.symbol_table = self.symbol_table.copy()
        body_compiler.visit(node.stmt)
        body_code = body_compiler.output

        # Combine body and next
        loop_body = body_code + next_code

        # Emit WHILE
        self.emit(f'[ {" ".join(cond_code)} ]')
        self.emit(f'[ {" ".join(loop_body)} ]')
        self.emit('WHILE')

    # Visit function calls
    def visit_FuncCall(self, node):
        # Visit arguments
        if node.args:
            for arg in node.args.exprs:
                self.visit(arg)
        # Emit function call
        func_name = node.name.name
        self.emit(func_name)

    # Translate C operators to toy language operators
    def translate_operator(self, op):
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

    # Visit unary operations (e.g., -a, !a, ++a, --a)
    def visit_UnaryOp(self, node):
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
        # Helper function to store value back to variable
        var_name = self.get_variable_name(expr)
        if var_name:
            self.emit(f'{var_name} STORE')
        else:
            self.error("Unsupported expression for increment/decrement.")

    def get_variable_name(self, expr):
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

    # Visit compound statements (e.g., { ... })
    def visit_Compound(self, node):
        for stmt in node.block_items or []:
            self.visit(stmt)

    # Visit expressions that are statements
    def visit_ExprList(self, node):
        for expr in node.exprs:
            self.visit(expr)

    def visit_Cast(self, node):
        # For now, ignore type casting
        self.visit(node.expr)

    def visit_TernaryOp(self, node):
        # Visit condition
        self.visit(node.cond)

        # True expression
        true_compiler = StruixCC()
        true_compiler.symbol_table = self.symbol_table.copy()
        true_compiler.visit(node.iftrue)
        true_code = true_compiler.output

        # False expression
        false_compiler = StruixCC()
        false_compiler.symbol_table = self.symbol_table.copy()
        false_compiler.visit(node.iffalse)
        false_code = false_compiler.output

        # Emit IFELSE
        self.emit(f'[ {" ".join(true_code)} ]')
        self.emit(f'[ {" ".join(false_code)} ]')
        self.emit('IFELSE')

    # Handle unsupported nodes
    def generic_visit(self, node):
        node_name = type(node).__name__
        self.warning(f"Unsupported node type '{node_name}'. Node will be ignored.")
        # Optionally, you can call super().generic_visit(node) to traverse children

    def visit_FileAST(self, node):
        """
        Visit the root of the AST, which is the FileAST node. It processes
        all top-level declarations like functions and global variables.
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
