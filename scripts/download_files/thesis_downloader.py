import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import Timeout, ReadTimeout
import http
import logging
import pandas as pd
import numpy as np
from scripts.progress_bar.progress_bar import printProgressBar

from requests.adapters import HTTPAdapter, Retry

http.client.HTTPConnection.debuglevel = 1

logging.basicConfig(level=logging.DEBUG)

s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
s.mount('http://', HTTPAdapter(max_retries=retries))

def download_thesis(path_to_save, thesis_title, url, size):
    try:
        pdf_response = s.get(url, timeout=10.0)
        #filename = unquote(pdf_response.url).split('/')[-1].replace(' ', '_')
        filename = str(thesis_title)
        l = int(size)
        #print(filename)
        printProgressBar(int(thesis_title), l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        with open('./' + path_to_save + '/' + filename + '.pdf', 'wb') as f:
            # write PDF to local file
            f.write(pdf_response.content)
    except Timeout as ex:
        pass
    except ReadTimeout as exr:
        pass
    except Exception as anything:
        pass


def download_from_file(csv_source, path_to_save):
    df = pd.read_csv(csv_source)
    df_head = df.copy()
    size = len(df_head.index)
    print(df_head)

    df_head['path'] = path_to_save
    donwload_func = np.vectorize(download_thesis)
    donwload_func(df_head['path'], df_head['index'], df_head['pdf_link'], size)


if __name__ == '__main__':
    download_from_file('./csv_files/url_thesis_8212.csv', 'thesis_pdf_test')

