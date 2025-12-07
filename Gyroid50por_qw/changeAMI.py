import sys

def replace_in_out(file_path,patch):
    '''
        Change the initial conditions for using scalarTransportFoam
    '''
    try:
        # Read the contents of the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Prepare the new content
        replacement = patch+"\n{\n    type fixedValue;\n"
        found = False
        new_lines = []
        patch_AMI = patch+"_cyclicAMI"
        i = 0
        while i < len(lines):
            if patch_AMI in lines[i]:
                # Replace the next three lines
                new_lines.append(replacement)  # Add the replacement
                i += 3  # Skip the current line and the next three lines
            else:
                new_lines.append(lines[i])  # Add the current line as is
                i += 1  # Move to the next line

        # Write the modified contents back to the file
        with open(file_path, 'w') as file:
            file.writelines(new_lines)

        # print(f"Substitution complete in file: {file_path}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python changeInlet.py pathToFile")
        sys.exit(1)
    pathTofile = sys.argv[1]
    
    replace_in_out(pathTofile,"inlet")
    replace_in_out(pathTofile,"outlet")
