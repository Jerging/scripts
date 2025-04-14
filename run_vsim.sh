#!/bin/bash

# Look for all .ascii files in the current directory
ASCII_FILES=(*.ascii)

# Check if any .ascii files are found
if [[ ${#ASCII_FILES[@]} -eq 0 ]]; then
    echo "No .ascii files found in the current directory."
    exit 1
fi

# Prompt user to choose a file
echo "Select an animation file to open with V_Sim:"
select FILE in "${ASCII_FILES[@]}"; do
    if [[ -n "$FILE" ]]; then
        echo "Opening $FILE in V_Sim..."
        export GDK_BACKEND=x11
        v_sim "$FILE"
        break
    else
        echo "Invalid selection. Try again."
    fi
done

