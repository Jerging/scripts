import numpy as np
import argparse

def load_npy_files(file_paths):
    # Create a dictionary to store the variables
    variables = {}

    # Loop through the list of file paths and load them
    for file_path in file_paths:
        try:
            # Extract the file name (without extension) to use as the variable name
            variable_name = file_path.split("/")[-1].split(".")[0]
            
            # Load the .npy file
            data = np.load(file_path)
            
            # Store the data in the dictionary with the file name as the variable name
            variables[variable_name] = data
            print(f"Loaded '{variable_name}' from '{file_path}'")
        except Exception as e:
            print(f"Error loading file '{file_path}': {e}")

    return variables

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Load .npy files and save them as variables.")
    parser.add_argument("files", nargs='+', help="Paths to .npy files")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Load the .npy files and save them as variables
    variables = load_npy_files(args.files)
    
    # Now you can perform calculations using the loaded variables.
    # For example:
    # if you have variables like matrix1 and matrix2, you can perform matrix operations
    if 'matrix1' in variables and 'matrix2' in variables:
        result = np.dot(variables['matrix1'], variables['matrix2'])
        print("Result of matrix multiplication:", result)

if __name__ == "__main__":
    main()

