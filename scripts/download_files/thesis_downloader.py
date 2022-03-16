import requests
import pandas as pd
import numpy as np
from scripts.progress_bar.progress_bar import printProgressBar

def download_thesis(path_to_save, thesis_title, url, size):
    pdf_response = requests.get(url)
    #filename = unquote(pdf_response.url).split('/')[-1].replace(' ', '_')
    filename = str(thesis_title)
    l = int(size)
    #print(filename)
    printProgressBar(int(thesis_title), l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    with open('./' + path_to_save + '/' + filename + '.pdf', 'wb') as f:
        # write PDF to local file
        f.write(pdf_response.content)

def download_from_file(csv_source):
    df = pd.read_csv(csv_source)
    df_head = df.copy()
    size = len(df_head.index)
    print(df_head)

    df_head['path'] = 'thesis_pdf'
    donwload_func = np.vectorize(download_thesis)
    donwload_func(df_head['path'], df_head['index'], df_head['pdf_link'], size)


if __name__ == '__main__':
    download_from_file('./csv_files/url_thesis_250.csv')

