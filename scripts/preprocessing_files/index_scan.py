import os

import pdfplumber
import random

import pandas as pd
import numpy as np

from scripts.progress_bar.progress_bar import printProgressBar


def is_image_n_page(file, n_page = 1):
    """ Determinates if a especific
    page of a file has text or is scanned.

    Parameters:
    -----------
    file : str
        The file location of the pdf file.
    n_page: int, optional
        The page number to check, must be less the the maximum ammoun of page of the pdf. 
        By default it checks on the first page.
    
    Returns:
    -----------
    boolean
        A boolean value if the page has text returns FALSE, if it's a image it return TRUE.
    """
    with pdfplumber.open(file) as pdf:
        if n_page < len(pdf.pages) and n_page >= 0:
            page = pdf.pages[n_page]
            #print(n_page)
        else:
            raise('Selected page to check must be inside the range of pages of the file')
        #print(len(pdf.pages))
        #print(random.randrange(2,len(pdf.pages)))

        text = page.extract_text()
        #print(text)  
    if text == '':
        return(True)
    else:
        return(False)


def check_conditions(file, thesis_title, l, conditions_to_meet = 4):
    """Checks if the whole pdf file is an image or has enough text to be treated as text.
    It work with 5 conditions described in parameters.

    Parameters:
    -----------
    file : str
        The file location of the pdf file.
    conditions_to_meet: int, optional
        The number of conditions to meet, it goes with first page, second page,
        the middle page plus one, the page -20 from the end, and a random page that is not the first and the second.
        By defualt it check the conditions in order and it must meet at least 4 to be True.
    
    Returns:
    -----------
    boolean
        A boolean value that if you meet the number of 
        conditions_to_meet parameter then it return True.
    """
    printProgressBar(int(thesis_title), l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    conditions = [False, False, False, False, False]
    if is_image_n_page(file, 0):
        conditions[0] = True
    if is_image_n_page(file, 1):
        conditions[1] = True
    with pdfplumber.open(file) as pdf:
        if is_image_n_page(file, int(len(pdf.pages)/2) + 1):
            conditions[2] = True
        if is_image_n_page(file, len(pdf.pages)-20):
            conditions[3] = True
        if is_image_n_page(file, random.randrange(2,len(pdf.pages))):
            conditions[4] = True
    if int(sum(conditions)) >= conditions_to_meet:
        return True
    else:
        return False

def concatenate(row, other_row):
    return str(row) + str(other_row) + '.pdf'


def isScan(csv_source, csv_dest):
    df = pd.read_csv(csv_source)
    df_head = df.copy()
    
    l = len(df_head.index)
    df_head['path'] = 'thesis_pdf/'
    func_concat = np.vectorize(concatenate)
    values = func_concat(df_head['path'], df_head['index'])
    df_head['path'] = values.tolist()
    func_check = np.vectorize(check_conditions)
    values_c = func_check(df_head['path'], df_head['index'], l)

    df_head['isScan'] = values_c.tolist()
    df_head.to_csv(csv_dest, index=False)
    #print(values_c)

if __name__ == '__main__':
    isScan('./csv_files/url_thesis_250.csv', './csv_files/url_thesis_200_with_scan.csv')



