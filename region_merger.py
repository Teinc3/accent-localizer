import pandas as pd
import os

def main():
    # Set file path
    file_path = os.path.join('__dataset', 'validated_regions.tsv')

    # Read file
    data = pd.read_csv(file_path, sep='\t')

    user_input: str = ''

    # Loop through user input
    while True:
        # Get all unique region names
        regions = data['region'].unique()
        print("Available regions: ", regions)
        user_input = input('Enter the region you want to merge (Syntax: <parentRegion> <childRegion>).\nType "exit" to exit.\n')

        if user_input == 'exit':
            break
        
        region1, region2 = user_input.split(' ')

        # Check if the regions are valid
        if region1 not in regions or region2 not in regions:
            print('Invalid region name(s).')
            continue

        # Merge the regions
        data.loc[data['region'] == region2, 'region'] = region1

    # Save the updated data
    data.to_csv(file_path, sep='\t', index=False)

    print('Merged regions have been saved successfully.')

if __name__ == '__main__':
    main()