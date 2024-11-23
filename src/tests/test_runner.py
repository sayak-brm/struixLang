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
    # Initialize struixLang interpreter
    terp = Terp()
    AddWords(terp)

    # Initialize the compiler
    compiler = StruixCC()

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
        try:
            # Compile the C code
            toy_code = compiler.compile(test['code'])
            print("Generated Toy Code:")
            print(toy_code)
            print("Executing Toy Code:")
            
            # Execute the struixLang code
            terp.run(toy_code)
            print("-" * 40)
        except CompilationError:
            print("Compilation failed due to errors.")
            print("-" * 40)

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
