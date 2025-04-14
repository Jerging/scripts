#!/bin/bash

# === Setup ===
if [[ ! -f "HIGH_SYMMETRY_POINTS" ]]; then
    echo "Error: HIGH_SYMMETRY_POINTS file not found."
    exit 1
fi

# Extract valid lines
VALID_LINES=($(awk '
    /^[[:space:]]*[0-9.-]+[[:space:]]+[0-9.-]+[[:space:]]+[0-9.-]+[[:space:]]+[A-Za-z0-9_]+/ {
        print $0
    }
' HIGH_SYMMETRY_POINTS))

if [[ ${#VALID_LINES[@]} -eq 0 ]]; then
    echo "Error: No valid high-symmetry point data found."
    exit 1
fi

# Extract point labels
OPTIONS=($(awk '
    /^[[:space:]]*[0-9.-]+[[:space:]]+[0-9.-]+[[:space:]]+[0-9.-]+[[:space:]]+[A-Za-z0-9_]+/ {
        print $4
    }
' HIGH_SYMMETRY_POINTS))

# Warn on duplicates
DUPLICATES=$(printf "%s\n" "${OPTIONS[@]}" | sort | uniq -d)
if [[ -n "$DUPLICATES" ]]; then
    echo "Warning: Duplicate labels found:"
    echo "$DUPLICATES"
fi

# === Create output directory ===
BASE_NAME=$(basename "$(pwd)")
OUT_DIR="${BASE_NAME}_animations"
mkdir -p "$OUT_DIR"
LOG_FILE="${OUT_DIR}/generation_log.txt"
echo "Logging output to $LOG_FILE" > "$LOG_FILE"

# === Coordinate formatting function ===
generate_ascii_file() {
    local label="$1"
    
    # Extract coordinates for the selected point
    read -r X Y Z <<< $(awk -v pt="$label" '$4 == pt {print $1, $2, $3; exit}' HIGH_SYMMETRY_POINTS)

    # Format the coordinates to one decimal place and remove unnecessary zeros
    COORDINATES=($X $Y $Z)
    FORMAT_COORDINATES=()
    for val in "${COORDINATES[@]}"; do
        rounded=$(printf "%.1f" "$val" | sed -E 's/(\.[0-9]*[1-9])0+$/\1/' | sed -E 's/\.0+$/\.0/')
        FORMAT_COORDINATES+=("$rounded")
    done
    COORD_STRING="${FORMAT_COORDINATES[*]}"
    
    # Run phonopy-load with the formatted coordinates
    phonopy-load --anime $COORD_STRING
    
    # Rename the generated file to anime_${label}.ascii
    mv anime.ascii "${OUT_DIR}/anime_${label}.ascii"
    
    # Log the file generation
    echo "Generated: anime_${label}.ascii" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
}

# === Ask: all or one? ===
read -p "Generate .ascii files for all high-symmetry points? (y/n): " GEN_ALL
GEN_ALL=${GEN_ALL,,}

if [[ "$GEN_ALL" == "y" ]]; then
    for pt in "${OPTIONS[@]}"; do
        generate_ascii_file "$pt"
    done
    echo "All .ascii files generated in: $OUT_DIR"

    # Ask to view one
    read -p "Would you like to open one of the animations in V_Sim now? (y/n): " VIEW_ONE
    VIEW_ONE=${VIEW_ONE,,}
    if [[ "$VIEW_ONE" == "y" ]]; then
        echo "Select a point to view:"
        select POINT in "${OPTIONS[@]}"; do
            if [[ -n "$POINT" ]]; then
                export GDK_BACKEND=x11
                v_sim "${OUT_DIR}/anime_${POINT}.ascii"
                break
            else
                echo "Invalid selection. Try again."
            fi
        done
    else
        echo "Skipping V_Sim preview."
    fi

else
    echo "Select one of the following high-symmetry points:"
    select POINT in "${OPTIONS[@]}"; do
        if [[ -n "$POINT" ]]; then
            break
        else
            echo "Invalid selection. Try again."
        fi
    done

    generate_ascii_file "$POINT"

    read -p "Open the animation in V_Sim? (y/n): " OPEN_VSIM
    OPEN_VSIM=${OPEN_VSIM,,}
    if [[ "$OPEN_VSIM" == "y" ]]; then
        export GDK_BACKEND=x11
        v_sim "${OUT_DIR}/anime_${POINT}.ascii"
    else
        echo "Skipping V_Sim preview."
    fi
fi

