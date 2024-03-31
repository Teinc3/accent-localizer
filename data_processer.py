import os
from collections import OrderedDict

import pandas as pd
from pandas import DataFrame as df

file_names = ["validated.tsv", "validated_all_accents.tsv", "validated_regions.tsv"]
region_codes = ["US", "CA", "CAR", "HIS",
                "EU", "ENG", "CEL", "FR", "GER ", "EAU",
                "ME", "WAF", "ZA", "EAF",
                "ZH", "IND", "SEA", "NEA",
                "AUS", "NZ"]

def save_file(output_file_path, data: df):
    data.to_csv(output_file_path, sep='\t', index=False)

def prune_empty_accents(data: df):
    new_data = data[data['accents'].notna()]
    save_file(os.path.join('__dataset/', file_names[1]), new_data)

def save_region_file(data: df):
    # Add a new column 'region' to the dataframe
    data['region'] = None

    # Write the new dataframe to a new file
    save_file(os.path.join('__dataset/', file_names[2]), data)

def assign_regions(data: df):
    '''
    Groups all rows with the same accent together and uses user input to assign a region to a corresponding accent.
    Continues the region assignment process from the last saved progress.

    Possible user input:
    - Corresponding region code for the accent
    - 'next' to skip current accent assignment and move to the next one
    - 'prev' to go back to the previous accent
    - 'view' to view all existing accents with indicies, row count and their assigned regions (if any)
    - 'goto <accent_index>' to edit the existing assigned region of an accent
    - 'continue' to continue from the largest remaining accent with no region assigned
    - 'exit' to save the current progress and exit the program

    All other invalid inputs will be ignored and the user will be re-prompted.
    '''

    # Get all unique accents in the dataframe
    accents = data['accents'].unique()

    # Initialize the accent_dict with the accent as the key and a List containing the region, index and count as the value
    accent_dict = {}
    # key-value pair structure - accent: [region, count]
    for accent in accents:
        # Search for any existing row in the dataframe with the accent and get the region
        same_accent_rows = data[data['accents'] == accent]
        region = None
        if not same_accent_rows.empty:
            region = same_accent_rows['region'].values[0]

        accent_dict[accent] = [region, len(same_accent_rows)]

    # Sort accent_dict by the count of the accents in descending order and store it in an OrderedDict
    accent_dict = OrderedDict(sorted(accent_dict.items(), key=lambda x: x[1][1], reverse=True))

    # Initialize variables
    user_input = ''
    current_accent_index = 0
    total_accents = len(accent_dict)

    # Set current_accent_index to the first occurrence in accent_dict where the region is None
    for i, (accent, values) in enumerate(accent_dict.items()):
        if values[0] is None:
            current_accent_index = i
            break
    
    # NOTE: THIS IS NOT COMPLETED AND NOT TESTED
    while user_input != 'exit' and current_accent_index < total_accents or user_input == '':
        # Get the current accent and its region
        current_accent = list(accent_dict.keys())[current_accent_index]
        current_region = accent_dict[current_accent][0]

        # Prompt the user for input
        if (current_region is None):
            user_input = input(f"\nEnter region for accent {current_accent_index} ('{current_accent}'): ")
        else:
            user_input = input(f"\nEnter region for accent {current_accent_index} ('{current_accent}' - Currently assigned to region {current_region}): ")

        # Handle user input
        if user_input == 'next':
            current_accent_index += 1
        elif user_input == 'prev':
            current_accent_index -= 1
        elif user_input == 'view':
            print("\n\nCurrent accent-region assignments:")
            for i, (accent, values) in enumerate(accent_dict.items()):
                print(f"{i}: {accent} - {values[0]} ({values[1]})")
            print("\n")
        elif user_input.startswith('goto '):
            try:
                index = int(user_input.split(' ')[1])
                if index < 0 or index >= total_accents:
                    raise ValueError
                current_accent_index = index
            except ValueError:
                print("Invalid index. Please enter a valid index.")
        elif user_input == 'continue':
            for i, (accent, values) in enumerate(accent_dict.items()):
                if values[0] is None:
                    current_accent_index = i
                    break
        elif user_input == 'exit':
            break
        elif user_input in region_codes:
            accent_dict[current_accent][0] = user_input
            current_accent_index += 1
        else:
            print("Invalid input. Please enter a valid region code or command.")

    # Save the updated dataframe
    for accent, values in accent_dict.items():
        data.loc[data['accents'] == accent, 'region'] = values[0]

    save_file(os.path.join('__dataset/', file_names[2]), data)

    print("\nFiles saved successfully.")


def main():
    # Find which file name we should be reading from
    read_file_index = 0

    for read_file_index in range(3):
        if not os.path.exists(os.path.join('__dataset/', file_names[read_file_index])):
            break

    while read_file_index <= 2:
        # Read the required file
        data = pd.read_csv(os.path.join('__dataset/', file_names[read_file_index]), sep='\t')

        if read_file_index == 0: # validated.tsv exists, but not the other two
            prune_empty_accents(data)
        elif read_file_index == 1: # validated_all_accents.tsv exists, but not validated_regions.tsv
            save_region_file(data)
        else: # validated_regions.tsv exists
            assign_regions(data)

        read_file_index += 1

if __name__ == "__main__":
    main()