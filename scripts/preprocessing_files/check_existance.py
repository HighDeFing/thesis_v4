from os.path import exists
import pandas as pd
import numpy as np
from scripts.progress_bar.progress_bar import printProgressBar

def check_one_file(file_path, index, l):
    printProgressBar(index, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    return exists(file_path)

def concatenate(row, other_row):
    return str(row) + str(other_row) + '.pdf'

def make_path_check_exist(csv_source, csv_dest, source_folder):
    df = pd.read_csv(csv_source)
    df_copy = df.copy()

    df_copy['path'] = source_folder
    
    func_concat = np.vectorize(concatenate)
    values = func_concat(df_copy['path'], df_copy['index'])
    df_copy['path'] = values.tolist()

    l = len(df_copy.index)

    func_check_exist = np.vectorize(check_one_file)
    values = func_check_exist(df_copy['path'], df_copy['index'], l)

    df_copy['exist'] = values.tolist()
    df_copy.to_csv(csv_dest, index=False)


if __name__ == '__main__':
    make_path_check_exist('csv_files/url_thesis_8211.csv', 'csv_files/url_thesis_8211_exist.csv', 'thesis_pdf_all/')
