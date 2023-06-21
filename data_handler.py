import pandas as pd
import os
import numpy as np
import glob

def process_enem_csv(file, frac=0.01):

    sampled_chunks = []

    for chunk in pd.read_csv(file, chunksize = 10000, encoding='ISO-8859-1', on_bad_lines='skip', sep=';'):
        sampled_chunk = chunk.sample(frac=frac)
        sampled_chunks.append(sampled_chunk)

    return pd.concat(sampled_chunks)

def read_enem(file, redo=False):
    """
    Reads a csv for enem microdata.

    Args:
        file(relative path): ENEM microdata file path
        redo(bool): If true, the data will be reloaded regardless of 
    """
    file_path = os.path.basename(file)
    data_path = 'enem_data/' + file_path + '.npy'
    data_path = os.path.abspath(data_path)

    if os.path.exists(data_path) and not redo:
        return np.load(data_path)

    enem_data = process_enem_csv(file)
    np.save(data_path, enem_data)

    return enem_data

if __name__ == '__main__':

    folder_path = 'enem_data/' 
    extension = '.csv'

    search_pattern = os.path.join(folder_path, f'*{extension}')
    file_list = glob.glob(search_pattern)

    for file in file_list:
        data = read_enem(file)
        print(file)

