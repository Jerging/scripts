import numpy as np
import os
import argparse

def convert_npy_to_txt(directory):
    # List all .npy files in the specified directory
    npy_files = [f for f in os.listdir(directory) if f.endswith('.npy')]
    
    for file in npy_files:
        file_path = os.path.join(directory, file)
        print(f"Loading {file_path}")
        
        # Load the .npy file
        data = np.load(file_path)
        
        # Define the output text file path
        txt_file_path = os.path.join(directory, file.replace(".npy", ".txt"))
        
        # Print the shape of the array
        print(f"Shape of {file}: {data.shape}")
        
        # Check if the data is complex
        if np.iscomplexobj(data):
            print(f"Complex data: Saving as a+bi format")
            
            # Handle 2D complex matrix
            if data.ndim == 2:
                formatted_data = [[f"{x.real:.6f}{'+' if x.imag >= 0 else ''}{x.imag:.6f}j" for x in row] for row in data]
            # Handle 1D complex array
            elif data.ndim == 1:
                formatted_data = [f"{x.real:.6f}{'+' if x.imag >= 0 else ''}{x.imag:.6f}j" for x in data]
            
            # Save the formatted data to a text file, maintaining matrix shape
            np.savetxt(txt_file_path, formatted_data, fmt="%s", delimiter=" ", header="Complex Numbers (a+bi format)")
        else:
            # Save real data to text file while maintaining the shape
            np.savetxt(txt_file_path, data, fmt="%.6f", delimiter=" ", header="Real Numbers")
        
        print(f"Converted {file} to {txt_file_path}")

def save_npy_files(directory):
    # List all .npy files in the specified directory
    npy_files = [f for f in os.listdir(directory) if f.endswith('.npy')]
    
    for file in npy_files:
        file_path = os.path.join(directory, file)
        data = np.load(file_path)
        
        # Save the file in the same directory as .npy
        np.save(file_path, data)
        print(f"Saved .npy file: {file_path}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Load .npy files, save as human-readable .txt files, and .npy files.")
    parser.add_argument("directory", help="Directory containing .npy files")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Check if the directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: The directory {args.directory} does not exist.")
    else:
        # Save .npy files and convert them to .txt files
        save_npy_files(args.directory)
        convert_npy_to_txt(args.directory)

