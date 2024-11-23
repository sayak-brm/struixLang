import sys
import os

# Add the src directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, src_dir)

from test_cases import test_cases
from struixLang.struixTerp import Terp
from struixLang.struixPrimitives import AddWords
from struixCC import StruixCC, CompilationError


def run_test_case(index=None):
    """
    Run the specified test case(s) by index. If no index is provided, run all test cases.

    Parameters:
        index (int or list[int]): Index or list of indices of test cases to run.
    """

    # If index is None, run all test cases
    if index is None:
        selected_cases = enumerate(test_cases, start=1)
    else:
        if isinstance(index, int):
            index = [index]
        selected_cases = ((i, test_cases[i - 1]) for i in index if 0 < i <= len(test_cases))

    # Run the test cases
    for idx, test in selected_cases:
        print(f"Test Case {idx}: {test['description']}")
        compiler = StruixCC()  # Initialize the compiler for each test case
        try:
            # Compile the C code
            sx_code = compiler.compile(test['code'])
            print("Generated struixLang Code:")
            print(sx_code)

            # Initialize struixLang interpreter
            terp = Terp()
            AddWords(terp)

            # Define a function to capture the return value of 'main'
            def capture_return():
                terp.run(sx_code)
                # Fetch the return value of 'main' from the stack
                if terp.stack:
                    return terp.stack.pop()
                else:
                    return None

            # Execute the code and capture the return value
            print("Executing Toy Code:")
            result = capture_return()
            expected = test['output']

            # Compare the result with the expected output
            if result == expected:
                print(f"Test Case {idx} Passed! Output: {result}")
            else:
                print(f"Test Case {idx} Failed!")
                print(f"Expected Output: {expected}, Actual Output: {result}")

            print("-" * 40)
        except CompilationError as e:
            expected = test['output']
            error_message = str(e)
            if expected in error_message:
                print(f"Test Case {idx} Passed! Expected error occurred: {expected}")
                print("-" * 40)
            else:
                print(f"Test Case {idx} Failed!")
                print(f"Expected Output: {expected}, Error during compilation: {error_message}")
        except Exception as e:
            print(f"Execution failed with exception: {e}")
            print("-" * 40)
            break

if __name__ == "__main__":
    # Get the indices of test cases to run from command-line arguments
    if len(sys.argv) > 1:
        try:
            indices = [int(arg) for arg in sys.argv[1:]]
            run_test_case(indices)
        except ValueError:
            print("Please provide valid test case indices as integers.")
    else:
        run_test_case()
