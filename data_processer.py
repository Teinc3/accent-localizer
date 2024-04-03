import os
from collections import OrderedDict

import pandas as pd
from pandas import DataFrame as df
from pydub import AudioSegment
from pydub.playback import play

file_names = ["validated.tsv", "validated_all_accents.tsv", "validated_regions.tsv"]
region_codes = {
    'US': 'Generic American / Mid-Atlantic',
    'CAN': 'Generic Canadian (Except Quebec)',
    'CAB': 'Carribean (Except Creoles)',
    'HIS': 'Latino / Romance (Except French)',

    'EU': 'Generic European (Unspecified)',
    'ENG': 'England English',
    'CEL': 'Irish / Scottish / Welsh',
    'FR': 'French / Quebec / Creoles',
    'GER': 'Germanic Languages',
    'EAU': 'Eastern European / Slavic',

    'ME': 'Middle Eastern and North African',
    'WAF': 'West African',
    'ZA': 'South African',
    'EAF': 'East African',

    'ETA': 'East Asian (Mandarin / Cantonese, Japanese, Korean etc.)',
    'IN': 'Indian (Indian, Pakistani, Bangladeshi etc.)',
    'SEA': 'South-East Asian (Vietnamese, Thai, Malaysian, Indonesian, Filipino etc.)',
    'NEA': 'Turkish / Persian / Central Asian (Near East Asian)',

    'AUS': 'Australian',
    'NZ': 'New Zealander / Pacific Islander'
}

def save_file(output_file_path, data: df):
    data.to_csv(output_file_path, sep='\t', index=False)

def prune_empty_accents(data: df):
    new_data = data[data['accents'].notna()]
    save_file(os.path.join('__dataset/', file_names[1]), new_data)
    print("Pruned empty accents.")

def save_region_file(data: df):
    # Add a new column 'region' to the dataframe
    data['region'] = ''

    # Write the new dataframe to a new file
    save_file(os.path.join('__dataset/', file_names[2]), data)

    print("Saved new region file.")

def assign_regions(data: df):
    '''
    Groups all rows with the same accent together and uses user input to assign a region to a corresponding accent.
    Continues the region assignment process from the last saved progress.

    Possible user input:
    - Corresponding region code for the accent
    - 'regions' for a list of all possible region codes
    - 'next' to skip current accent assignment and move to the next one
    - 'prev' to go back to the previous accent
    - 'view' to view all existing accents with indicies, row count and their assigned regions (if any)
    - 'goto <accent_index>' to edit the existing assigned region of an accent
    - 'continue' to continue from the largest remaining accent with no region assigned
    - 'exit' to save the current progress and exit the program
    - 'listen' to listen to a random audio clip of the accent
    - 'help' to view the list of possible commands

    All other invalid inputs will be ignored and the user will be re-prompted.
    '''

    # Get all unique accents in the dataframe
    accents = data['accents'].unique()

    # Initialize the accent_dict with the accent as the key and a List containing the region, index and count as the value
    accent_dict = {}
    for accent in accents:
        # Search for any existing row in the dataframe with the accent and get the region
        same_accent_rows = data[data['accents'] == accent]
        region = ''
        if not same_accent_rows.empty:
            region = same_accent_rows['region'].values[0]

        # key-value pair structure - accent: [region, count]
        accent_dict[accent] = [region, len(same_accent_rows)]

    # Sort accent_dict by the count of the accents in descending order and store it in an OrderedDict
    accent_dict = OrderedDict(sorted(accent_dict.items(), key=lambda x: x[1][1], reverse=True))

    # Initialize variables
    user_input = ''
    current_accent_index = 0
    total_accents = len(accent_dict)

    # Set current_accent_index to the first occurrence in accent_dict where the region DNE ('')
    for i, (accent, values) in enumerate(accent_dict.items()):
        if values[0] == '':
            current_accent_index = i
            break
    
    assign_helper()

    # Handle user input
    while user_input != 'exit' and current_accent_index < total_accents or user_input == '':
        # Get the current accent and its region
        current_accent = list(accent_dict.keys())[current_accent_index]
        current_region = accent_dict[current_accent][0]

        # Prompt the user for input
        if pd.isna(current_region):
            user_input = input(f"\n{current_accent_index}. (Max {total_accents - 1}) - Enter region for accent '{current_accent}': ")
        else:
            user_input = input(f"\n{current_accent_index}. (Max {total_accents - 1}) - Enter new region for accent '{current_accent}' (Region {current_region}): ")

        if user_input == 'next':
            current_accent_index += 1
        elif user_input == 'prev':
            current_accent_index -= 1
            if current_accent_index < 0:
                current_accent_index = total_accents - 1
        elif user_input == 'view':
            print("\n\nCurrent accent-region assignments:")
            for i, (accent, values) in enumerate(accent_dict.items()):
                print(f"{i}: {accent} - {values[0]} ({'Unassigned' if pd.isna(values[1]) else values[1]})")
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
                if pd.isna(values[0]):
                    current_accent_index = i
                    break
        elif user_input == 'exit':
            break
        elif user_input == 'help':
            assign_helper()
        elif user_input == 'regions':
            print("\n\nList of possible region codes:")
            for code, region in region_codes.items():
                print(f"{code}: {region}")
            print("\n")
            
        elif user_input == 'listen':
            # Search for all rows with the current accent and get a random audio clip
            same_accent_rows = data[data['accents'] == current_accent]
            if not same_accent_rows.empty:
                sample_row = same_accent_rows.sample(1)
                audio_file = sample_row['path'].values[0]
                sentence = sample_row['sentence'].values[0]
                audio = AudioSegment.from_file(os.path.join('__dataset/clips/', audio_file))
                print(f"Playing audio clip {audio_file} for accent '{current_accent}'.\nSentence: '{sentence}'")
                play(audio)

        elif user_input in region_codes.keys():
            accent_dict[current_accent][0] = user_input
            current_accent_index += 1
        else:
            print("Invalid input. Please enter a valid region code or command.")
            assign_helper()

    # Save the updated dataframe
    for accent, values in accent_dict.items():
        data.loc[data['accents'] == accent, 'region'] = values[0]

    save_file(os.path.join('__dataset/', file_names[2]), data)

    print("\nAccent region assignment finished. Saving progress.")

def assign_helper():
    print(f"\n\nList of possible commands:\n{assign_regions.__doc__}")

def main():
    # Find which file name we should be reading from
    read_file_index = 0

    # -1: validated DNE, 0: all_accents DNE, 1: regions DNE, 2: all exist
    for read_file_index in range(3):
        if not os.path.exists(os.path.join('__dataset/', file_names[read_file_index])):
            read_file_index -= 1
            break
    
    if read_file_index == -1:
        print("validated.tsv does not exist. Exiting...")
        return

    while read_file_index <= 2:
        # Specify the data types of the columns
        dtypes = {'sentence_domain': str, 'segment': str}
        if read_file_index >= 1:  # 'region' column exists
            dtypes['region'] = str

        # Read the required file
        data = pd.read_csv(os.path.join('__dataset/', file_names[read_file_index]), sep='\t', dtype=dtypes)

        if read_file_index == 0: # validated.tsv exists, but not the other two
            prune_empty_accents(data)
        elif read_file_index == 1: # validated_all_accents.tsv exists, but not validated_regions.tsv
            save_region_file(data)
        else: # validated_regions.tsv exists
            assign_regions(data)

        read_file_index += 1
    
    print("Data processing complete. Exiting...")

if __name__ == "__main__":
    main()