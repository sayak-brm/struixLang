import os

def list_libs(lib_directory):
    """
    Lists all .sxlib files in the specified directory and prints their names and contents.
    
    Args:
        lib_directory (str): The path to the directory containing .sxlib files.
    """
    # Check if the directory exists
    if not os.path.exists(lib_directory):
        print(f"Error: Directory '{lib_directory}' does not exist.")
        return
    
    # Iterate through all files in the directory
    for filename in sorted(os.listdir(lib_directory)):
        # Only process files with the .sxlib extension
        if filename.endswith(".sxlib"):
            file_path = os.path.join(lib_directory, filename)
            print(f"--- File: {filename} ---")
            
            # Open and read the file's contents
            try:
                with open(file_path, "r") as file:
                    contents = file.read()
                    print(contents)
            except Exception as e:
                print(f"Error reading file '{filename}': {e}")
            
            print("\n" + "-" * 40 + "\n")  # Separator between files

if __name__ == "__main__":
    # Assuming this script is inside the 'src/tools' directory
    # Adjust the relative path to the 'lib' directory
    lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib")
    list_libs(lib_dir)
