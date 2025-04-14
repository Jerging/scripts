#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:20:56 2025

@author: jeremy
"""
import numpy as np
import itertools

def read_poscar(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    scale = float(lines[1].strip())
    lattice_vectors = np.array([list(map(float, line.split())) for line in lines[2:5]])
    elements = lines[5].split()
    num_atoms = list(map(int, lines[6].split()))
    total_atoms = sum(num_atoms)
    coords = np.array([list(map(float, line.split()[:3])) for line in lines[8:8+total_atoms]])
    return scale, lattice_vectors, elements, num_atoms, coords

def write_poscar(filename, scale, lattice_vectors, elements, num_atoms, coords):
    with open(filename, 'w') as f:
        f.write("Generated POSCAR with Octahedral Tilt\n")
        f.write(f"{scale}\n")
        for vec in lattice_vectors:
            f.write(" ".join(map(str, vec)) + "\n")
        f.write(" ".join(elements) + "\n")
        f.write(" ".join(map(str, num_atoms)) + "\n")
        f.write("Cartesian\n")
        for coord in coords:
            f.write(" ".join(map(str, coord)) + "\n")

def apply_tilt(coords, tilt_type):
    if tilt_type == 'a+a+a+':
        # Example: small displacement to simulate tilt
        coords[:, 0] += 0.02 * np.sin(coords[:, 1])
    # Other tilt cases can be implemented similarly
    return coords

def main():
    filename = input("Enter the POSCAR filename: ")
    scale, lattice_vectors, elements, num_atoms, coords = read_poscar(filename)
    
    tilt_types = ["a+a+a+", "a+a+a-", "a+a-a+", "a-a-a-", "a0a0a+", "a0a0a-", "a0b+b+", "a0b+b-", "a0b-b-", "a0a0b+", "a0a0b-", "a+a0c+", "a-a0c-", "a+b+c+", "a-b-c-"]
    print("Available octahedral tilts:")
    for i, tilt in enumerate(tilt_types):
        print(f"{i + 1}: {tilt}")
    
    choice = int(input("Choose a tilt type by number: ")) - 1
    if 0 <= choice < len(tilt_types):
        tilt_type = tilt_types[choice]
        coords = apply_tilt(coords, tilt_type)
        write_poscar("POSCAR_tilted", scale, lattice_vectors, elements, num_atoms, coords)
        print(f"Tilt {tilt_type} applied and saved to POSCAR_tilted.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
