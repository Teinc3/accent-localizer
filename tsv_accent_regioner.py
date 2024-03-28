import os
import pandas as pd

files = ['train', 'dev', 'test']
accent_dict = {}

for file in files:
    filename = f'{file}.tsv'
    filepath = os.path.join('__dataset/curated', filename)

    data = pd.read_csv(filepath, sep='\t')
    # Get unique values in "accents" column and add their corresponding count to accent_dict
    for accent in data['accents'].unique():
        if accent not in accent_dict:
            accent_dict[accent] = 0
        accent_dict[accent] += len(data[data['accents'] == accent])

# Sort accent_dict by count in descending order
accent_dict = {k: v for k, v in sorted(accent_dict.items(), key=lambda item: item[1], reverse=True)}

# Print accent_dict
print("\nAccent counts:")
for accent, count in accent_dict.items():
    print(f"{accent}: {count}")

# Loop from top accent to bottom - we assign a new category called "region" to each accent.
# We will use this new category to group accents into regions.
# We ask the user to input the region for each accent.
# We store the region for each accent in a dictionary called accent_region.
accent_region = {}
print("\nAssign regions to accents:")
for accent in accent_dict:
    region = input(f"\nEnter region for accent '{accent}': ")
    accent_region[accent] = region

    # Print all existing regions
    print("\nCurrent accent-region assignments:")
    for a, r in accent_region.items():
        print(f"{a}: {r}")

# Read existing files, add "region" column, and save the region where the accent is found.
print("\nUpdating files with region information...")
for file in files:
    filename = f'{file}.tsv'
    filepath = os.path.join('__dataset/curated', filename)

    data = pd.read_csv(filepath, sep='\t')
    data['region'] = data['accents'].map(accent_region)
    data.to_csv(filepath, sep='\t', index=False)

print("\nFiles updated successfully.")