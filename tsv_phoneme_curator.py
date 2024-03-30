import os
import subprocess
import multiprocessing

import pandas as pd

from allosaurus.app import read_recognizer

files = ['dev', 'test', 'train']
tmp_dir = '__dataset/tmp'

def file_namer(path):
    return path.split('_')[-1].split('.')[0]

def extract_phonemes(tuple):
    row = tuple[1]
    input_name = row['path']

    # If the phonemes have already been extracted, skip this row
    if row['phonemes'] is not None:
        return row['phonemes']

    # get the path to the audio file
    audio_path = os.path.join('__dataset/clips', input_name)

    # Save the audio file as a wav file in the tmp directory using ffmpeg
    new_audio_path = os.path.join(tmp_dir, f'{file_namer(input_name)}.wav')
    subprocess.run(['ffmpeg', '-i', audio_path, new_audio_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Get the phonemes from the audio file
    recognizer = read_recognizer()
    phonemes = recognizer.recognize(new_audio_path)

    # Remove the temporary audio file
    os.remove(new_audio_path)

    return phonemes

def main():

    # Read the files
    for file in files:
        filename = f'{file}.tsv'
        filepath = os.path.join('__dataset/curated', filename)
        data = pd.read_csv(filepath, sep='\t')

        # Add a new column called "phonemes" if it doesn't exist
        if 'phonemes' not in data.columns:
            data['phonemes'] = None
        
        # Create the tmp directory if it doesn't exist (Wipe its contents if it does)
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        else:
            for file in os.listdir(tmp_dir):
                os.remove(os.path.join(tmp_dir, file))
        
        # Use a multiprocessing Pool to parallelize the phoneme extraction process
        with multiprocessing.Pool() as p:
            data['phonemes'] = p.map(extract_phonemes, data.iterrows())
        
        # Save the updated data
        data.to_csv(filepath, sep='\t', index=False)

    print("\nPhonemes extracted and saved successfully.")

if __name__ == '__main__':
    main()