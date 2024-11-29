test_cases = [
    {
        "description": "Basic variable declaration and assignment",
        "code": r'''
        int main() {
            int a;
            a = 5;
            return a;
        }
        ''',
        "output": 5
    },
    {
        "description": "Arithmetic expressions with variables",
        "code": r'''
        int main() {
            int a = 5;
            int b = 10;
            int c = a + b * 2;
            return c;
        }
        ''',
        "output": 25
    },
    {
        "description": "If statement with else clause",
        "code": r'''
        int main() {
            int a = 5;
            int b;
            if (a > 0) {
                b = 1;
            } else {
                b = 2;
            }
            return b;
        }
        ''',
        "output": 1
    },
    {
        "description": "While loop summing numbers",
        "code": r'''
        int main() {
            int i = 0;
            int sum = 0;
            while (i < 5) {
                sum = sum + i;
                i = i + 1;
            }
            return sum;
        }
        ''',
        "output": 10
    },
    {
        "description": "Function call with two arguments",
        "code": r'''
        int add(int x, int y) {
            return x + y;
        }
        int main() {
            int result = add(5, 10);
            return result;
        }
        ''',
        "output": 15
    },
    {
        "description": "Switch statement with cases and break",
        "code": r'''
        int main() {
            int x = 2;
            int y;
            switch(x) {
                case 1:
                    y = 10;
                    break;
                case 2:
                    y = 20;
                    break;
                default:
                    y = 30;
                    break;
            }
            return y;
        }
        ''',
        "output": 20
    },
    {
        "description": "For loop summing numbers",
        "code": r'''
        int main() {
            int sum = 0;
            int i;
            for (i = 0; i < 5; i = i + 1) {
                sum = sum + i;
            }
            return sum;
        }
        ''',
        "output": 10
    },
    {
        "description": "Array usage and summation",
        "code": r'''
        int main() {
            int arr[3];
            arr[0] = 5;
            arr[1] = 10;
            arr[2] = 15;
            int sum = arr[0] + arr[1] + arr[2];
            return sum;
        }
        ''',
        "output": 30
    },
    {
        "description": "Post-increment operator",
        "code": r'''
        int main() {
            int a = 5;
            a++;
            return a;
        }
        ''',
        "output": 6
    },
    {
        "description": "Logical AND operator in if statement",
        "code": r'''
        int main() {
            int a = 5;
            int b = 10;
            int c;
            if (a < b && b > 0) {
                c = 1;
            } else {
                c = 0;
            }
            return c;
        }
        ''',
        "output": 1
    },
    {
        "description": "Bitwise AND operator",
        "code": r'''
        int main() {
            int a = 5;  // Binary: 0101
            int b = 3;  // Binary: 0011
            int c = a & b;  // Result: 0001
            return c;
        }
        ''',
        "output": 1
    },
    {
        "description": "Nested for loops",
        "code": r'''
        int main() {
            int i, j;
            int sum = 0;
            for (i = 0; i < 3; i++) {
                for (j = 0; j < 2; j++) {
                    sum = sum + i + j;
                }
            }
            return sum;
        }
        ''',
        "output": 9
    },
    {
        "description": "Do-while loop summing numbers",
        "code": r'''
        int main() {
            int i = 0;
            int sum = 0;
            do {
                sum = sum + i;
                i = i + 1;
            } while (i < 5);
            return sum;
        }
        ''',
        "output": 10
    },
    {
        "description": "Break statement in for loop",
        "code": r'''
        int main() {
            int i;
            int sum = 0;
            for (i = 0; i < 10; i++) {
                if (i == 5) {
                    break;
                }
                sum = sum + i;
            }
            return sum;
        }
        ''',
        "output": 10
    },
    {
        "description": "Continue statement in for loop",
        "code": r'''
        int main() {
            int i;
            int sum = 0;
            for (i = 0; i < 5; i++) {
                if (i == 2) {
                    continue;
                }
                sum = sum + i;
            }
            return sum;
        }
        ''',
        "output": 8
    },
    {
        "description": "Ternary operator usage",
        "code": r'''
        int main() {
            int a = 5;
            int b = (a > 0) ? 1 : -1;
            return b;
        }
        ''',
        "output": 1
    },
    {
        "description": "Nested if statements",
        "code": r'''
        int main() {
            int a = 5;
            int b = 10;
            int c;
            if (a > 0) {
                if (b > 0) {
                    c = 1;
                } else {
                    c = 2;
                }
            } else {
                c = 3;
            }
            return c;
        }
        ''',
        "output": 1
    },
    {
        "description": "Recursive function (factorial)",
        "code": r'''
        int factorial(int n) {
            if (n <= 1) {
                return 1;
            } else {
                return n * factorial(n - 1);
            }
        }
        int main() {
            int result = factorial(5);
            return result;
        }
        ''',
        "output": 120
    },
    {
        "description": "Array initialization with constants",
        "code": r'''
        int main() {
            int arr[3] = {1, 2, 3};
            int sum = arr[0] + arr[1] + arr[2];
            return sum;
        }
        ''',
        "output": 6
    },
    {
        "description": "Pointer usage to modify variable",
        "code": r'''
        int main() {
            int a = 5;
            int *p = &a;
            *p = 10;
            return a;
        }
        ''',
        "output": 10
    },
    {
        "description": "Cast expression ignored by compiler",
        "code": r'''
        int main() {
            int a = (int)5.5;
            return a;
        }
        ''',
        "output": 5
    },
    {
        "description": "Post-increment operator assignment",
        "code": r'''
        int main() {
            int a = 5;
            int b = a++;
            return b;
        }
        ''',
        "output": 5
    },
    {
        "description": "Pre-increment operator assignment",
        "code": r'''
        int main() {
            int a = 5;
            int b = ++a;
            return b;
        }
        ''',
        "output": 6
    },
    {
        "description": "Complex arithmetic expression",
        "code": r'''
        int main() {
            int a = 5;
            int b = 10;
            int c = (a + b) * (a - b);
            return c;
        }
        ''',
        "output": -75
    },
    {
        "description": "Logical NOT operator",
        "code": r'''
        int main() {
            int a = 0;
            int b = !a;
            return b;
        }
        ''',
        "output": 1
    },
    {
        "description": "Unary minus operator",
        "code": r'''
        int main() {
            int a = 5;
            int b = -a;
            return b;
        }
        ''',
        "output": -5
    },
    {
        "description": "Global variable usage",
        "code": r'''
        int a = 5;
        int main() {
            return a;
        }
        ''',
        "output": 5
    },
    {
        "description": "Array indexing with variable",
        "code": r'''
        int main() {
            int arr[5];
            int i;
            for (i = 0; i < 5; i++) {
                arr[i] = i * i;
            }
            int sum = 0;
            for (i = 0; i < 5; i++) {
                sum = sum + arr[i];
            }
            return sum;
        }
        ''',
        "output": 30
    },
    {
        "description": "Function with no parameters",
        "code": r'''
        int get_five() {
            return 5;
        }
        int main() {
            int a = get_five();
            return a;
        }
        ''',
        "output": 5
    },
    {
        "description": "Function with multiple parameters",
        "code": r'''
        int add_three(int a, int b, int c) {
            return a + b + c;
        }
        int main() {
            int result = add_three(1, 2, 3);
            return result;
        }
        ''',
        "output": 6
    },
    {
        "description": "Assignment in condition",
        "code": r'''
        int main() {
            int a = 0;
            if (a = 5) {
                return a;
            } else {
                return 0;
            }
        }
        ''',
        "output": 5
    },
    {
        "description": "Undefined variable usage",
        "code": r'''
        int main() {
            int a = b + 5;
            return a;
        }
        ''',
        "output": "Error: Undefined variable 'b'"
    },
    {
        "description": "Division by zero",
        "code": r'''
        int main() {
            int a = 5 / 0;
            return a;
        }
        ''',
        "output": "Error: Division by zero"
    },
    {
        "description": "Modulus operator usage",
        "code": r'''
        int main() {
            int a = 10 % 3;
            return a;
        }
        ''',
        "output": 1
    },
    {
        "description": "Left shift operator",
        "code": r'''
        int main() {
            int a = 1 << 3;
            return a;
        }
        ''',
        "output": 8
    },
    {
        "description": "Bitwise XOR operator",
        "code": r'''
        int main() {
            int a = 5 ^ 3;
            return a;
        }
        ''',
        "output": 6
    },
    {
        "description": "Compound assignment operator += (unsupported)",
        "code": r'''
        int main() {
            int a = 5;
            a += 3;
            return a;
        }
        ''',
        "output": "Error: Unsupported assignment operator '+='"
    },
    {
        "description": "Empty for loop body",
        "code": r'''
        int main() {
            int i;
            for (i = 0; i < 5; i++);
            return i;
        }
        ''',
        "output": 5
    },
    {
        "description": "Variable shadowing with global and local",
        "code": r'''
        int a = 5;
        int main() {
            int a = 10;
            return a;
        }
        ''',
        "output": 10
    },
    {
        "description": "String constants (unsupported)",
        "code": r'''
        int main() {
            char *s = "Hello";
            return 0;
        }
        ''',
        "output": "Warning: Unsupported node type 'Constant'. Node will be ignored."
    },
    {
        "description": "Multiple variable declarations",
        "code": r'''
        int main() {
            int a, b, c;
            a = 1;
            b = 2;
            c = 3;
            return a + b + c;
        }
        ''',
        "output": 6
    },
    {
        "description": "Variable initialization at declaration",
        "code": r'''
        int main() {
            int a = 5;
            int b = a + 2;
            return b;
        }
        ''',
        "output": 7
    },
    {
        "description": "Variable usage before declaration (error)",
        "code": r'''
        int main() {
            a = 5;
            int a;
            return a;
        }
        ''',
        "output": "Error: Variable 'a' used before declaration"
    },
    {
        "description": "Function prototype and definition",
        "code": r'''
        int add(int, int);
        int main() {
            int result = add(5, 10);
            return result;
        }
        int add(int x, int y) {
            return x + y;
        }
        ''',
        "output": 15
    },
    {
        "description": "Struct definitions (unsupported)",
        "code": r'''
        struct Point {
            int x;
            int y;
        };
        int main() {
            struct Point p;
            p.x = 5;
            p.y = 10;
            return p.x + p.y;
        }
        ''',
        "output": "Warning: Unsupported node type 'Struct'. Node will be ignored."
    },
    {
        "description": "Conditional compilation directives (unsupported)",
        "code": r'''
        int main() {
        #ifdef TEST
            return 1;
        #else
            return 0;
        #endif
        }
        ''',
        "output": "Warning: Preprocessor directives are ignored"
    },
    {
        "description": "Enum usage (unsupported)",
        "code": r'''
        enum Color { RED, GREEN, BLUE };
        int main() {
            enum Color c = GREEN;
            return c;
        }
        ''',
        "output": "Warning: Unsupported node type 'Enum'. Node will be ignored."
    },
    {
        "description": "Pointer arithmetic (unsupported)",
        "code": r'''
        int main() {
            int arr[3] = {1, 2, 3};
            int *p = arr;
            int sum = *p + *(p + 1) + *(p + 2);
            return sum;
        }
        ''',
        "output": "Error: Pointer arithmetic not supported"
    },
    {
        "description": "Conditional operator with logical expressions",
        "code": r'''
        int main() {
            int a = 5;
            int b = 10;
            int max = (a > b) ? a : b;
            return max;
        }
        ''',
        "output": 10
    },
    {
        "description": "Nested ternary operators",
        "code": r'''
        int main() {
            int a = 5;
            int b = 10;
            int c = 15;
            int max = (a > b) ? (a > c ? a : c) : (b > c ? b : c);
            return max;
        }
        ''',
        "output": 15
    },
    {
        "description": "Chained assignments",
        "code": r'''
        int main() {
            int a, b, c;
            a = b = c = 5;
            return a + b + c;
        }
        ''',
        "output": 15
    },
    {
        "description": "Comma operator in for loop",
        "code": r'''
        int main() {
            int sum = 0;
            int i, j;
            for (i = 0, j = 5; i < 5; i++, j--) {
                sum = sum + i + j;
            }
            return sum;
        }
        ''',
        "output": 25
    },
    {
        "description": "Function returning void (unsupported)",
        "code": r'''
        void display() {
            // Do nothing
        }
        int main() {
            display();
            return 0;
        }
        ''',
        "output": 0
    },
    {
        "description": "Array passed to function",
        "code": r'''
        int sum_array(int arr[], int size) {
            int i, sum = 0;
            for (i = 0; i < size; i++) {
                sum = sum + arr[i];
            }
            return sum;
        }
        int main() {
            int arr[3] = {1, 2, 3};
            int result = sum_array(arr, 3);
            return result;
        }
        ''',
        "output": 6
    }
]
