import os
import pandas as pd

files = ['train', 'dev', 'test']
output_dir = '__dataset/curated'

# Check if the curated files already exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
curated_files_exist = all(os.path.exists(os.path.join(output_dir, f'{file}.tsv')) for file in files)

if not curated_files_exist:
    # Mode 1: Accent curation
    print("\nFiles not found in the 'curated' directory. Curating accent data...")

    for file in files:
        # Define paths
        filename = f'{file}.tsv'
        input_path = os.path.join('__dataset', filename)
        output_path = os.path.join(output_dir, filename)

        # Load data
        data = pd.read_csv(input_path, sep='\t')

        # Filter out rows without "accents" column
        data = data[data['accents'].notna()]

        # Sort by "accents" column
        data = data.sort_values(by='accents')

        # Save curated dataset
        data.to_csv(output_path, sep='\t', index=False)
else:
    # Mode 2: Region curation
    print("\nCurated files found in the 'curated' directory. Curating region data...")
    
    for file in files:
        # Define paths
        filename = f'{file}.tsv'
        filepath = os.path.join(output_dir, filename)

        # Load data
        data = pd.read_csv(filepath, sep='\t')

        # Filter out rows without "region" column
        data = data[data['region'].notna()]

        # Save curated dataset
        data.to_csv(filepath, sep='\t', index=False)

print("\nFiles updated successfully.")