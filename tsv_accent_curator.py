import os
import pandas as pd

files = ['train', 'dev', 'test']

output_dir = '__dataset/curated'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for file in files:
    # Define paths
    filename = f'{file}.tsv'
    input_path = os.path.join('__dataset', filename)
    output_path = os.path.join(output_dir, filename)

    # Load training data
    train_data = pd.read_csv(input_path, sep='\t')

    # Filter out rows without "accents" column
    train_data = train_data[train_data['accents'].notna()]

    # Sort by "accents" column
    train_data = train_data.sort_values(by='accents')

    # Save curated dataset
    train_data.to_csv(output_path, sep='\t', index=False)