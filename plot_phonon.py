#!/usr/bin/env python3
import matplotlib.pyplot as plt
import argparse
import os
import sys

def read_high_symmetry_points(filename):
    """Read high symmetry points from KLABELS file"""
    labels = []
    try:
        with open(filename, 'r') as f:
            next(f)  # Skip header line
            for line in f:
                line = line.strip()
                if not line or line.startswith('*'):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        label = parts[0]
                        coord = float(parts[1])
                        labels.append((label, coord))
                    except (ValueError, IndexError):
                        continue
    except FileNotFoundError:
        print(f"Error: File {filename} not found!")
        sys.exit(1)
    return labels

def read_branches(file_path):
    """Read phonon branches from data file"""
    branches = []
    current_branch = None
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('# Branch-Index:'):
                    if current_branch is not None:
                        branches.append(current_branch)
                    current_branch = []
                elif line.strip() and not line.startswith('#'):
                    x, y = map(float, line.split())
                    current_branch.append((x, y))
        
        if current_branch is not None:
            branches.append(current_branch)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found!")
        sys.exit(1)
    return branches

def plot_combined(branches, high_symmetry_points, output_file="phonon_bands.png", title="Phonon Band Structure"):
    """Plot and save combined figure"""
    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    # Plot phonon branches
    for i, branch in enumerate(branches):
        x_vals = [point[0] for point in branch]
        y_vals = [point[1] for point in branch]
        ax.plot(x_vals, y_vals, linewidth=1)

    # Plot high-symmetry points
    if high_symmetry_points:
        x_coords = [coord for _, coord in high_symmetry_points]
        x_labels = [label for label, _ in high_symmetry_points]
        
        # Add vertical lines
        for x in x_coords:
            ax.axvline(x, color='gray', linestyle='--', linewidth=0.5)
        
        # Configure axis labels
        ax.set_xticks(x_coords)
        ax.set_xticklabels(x_labels)
        ax.set_xlim(x_coords[0], x_coords[-1])

    # Formatting
    ax.set_xlabel('K-Path')
    ax.set_ylabel('Frequency (meV)')
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    plt.savefig(output_file, dpi=300)
    print(f"Plot saved as {output_file}")

if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description='Plot phonon band structure from VASP/VASPKIT output')
    parser.add_argument('-b', '--bands', default='PHONON_BAND.dat',
                       help='Input phonon bands file (default: PHONON_BAND.dat)')
    parser.add_argument('-k', '--klabels', default='KLABELS',
                       help='Input k-labels file (default: KLABELS)')
    parser.add_argument('-o', '--output', default='phonon_bands.png',
                       help='Output plot filename (default: phonon_bands.png)')
    # Add title argument
    parser.add_argument('-t', '--title', default='Phonon Band Structure',
                       help='Title for the plot (default: "Phonon Band Structure")')
    
    args = parser.parse_args()

    # Read data
    branches = read_branches(args.bands)
    high_symmetry_points = read_high_symmetry_points(args.klabels)
    
    # Generate plot with title
    plot_combined(branches, high_symmetry_points, args.output, args.title)
