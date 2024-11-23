# test_cases.py
test_cases = [
    {
        "description": "Basic array manipulation and summation",
        "code": r'''
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
    },
    {
        "description": "Simple arithmetic and conditionals",
        "code": r'''
        int main() {
            int a = 10, b = 20;
            int result = 0;
            if (a < b) {
                result = a + b;
            } else {
                result = a - b;
            }
            return result;
        }
        '''
    },
    {
        "description": "Nested loops with multiplication table",
        "code": r'''
        int main() {
            int i, j;
            int table[10][10];
            for (i = 1; i <= 10; i++) {
                for (j = 1; j <= 10; j++) {
                    table[i-1][j-1] = i * j;
                }
            }
            return table[9][9]; // Return 10 * 10
        }
        '''
    },
    {
        "description": "Switch statement example",
        "code": r'''
        int main() {
            int value = 3;
            int result = 0;
            switch (value) {
                case 1: result = 10; break;
                case 2: result = 20; break;
                case 3: result = 30; break;
                default: result = -1; break;
            }
            return result;
        }
        '''
    },
    {
        "description": "Function call with parameters",
        "code": r'''
        int add(int a, int b) {
            return a + b;
        }

        int main() {
            int x = 5, y = 10;
            int sum = add(x, y);
            return sum;
        }
        '''
    }
]
