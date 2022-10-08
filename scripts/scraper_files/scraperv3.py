from bs4 import BeautifulSoup
import requests
import csv
from scripts.progress_bar.progress_bar import printProgressBar
from pdf_info_extracter import getSize, get_pdf_link, get_resumen 
import logging
from requests.adapters import HTTPAdapter, Retry

logging.basicConfig(level=logging.DEBUG)

s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
s.mount('http://', HTTPAdapter(max_retries=retries))

def find_n_rows(n_rows = 5, dest_file = './csv_files/url_thesis_{}.csv', url_link = "http://saber.ucv.ve/handle/10872/2/browse?type=dateissued&sort_by=2&order=ASC&rpp={}&etal=0&submit_browse=Actualizar"):
    """Scraps the amount of thesis in the argument n_rows, it cannot be more than 8210, or the number of thesis that UCV has for Pregrado at that time.

    Parameters:
    ------------
    n_rows: int 
        Number of rows to scrap, it most be more than 0 and less than 8210 or the number of thesis that UCV has for Pregrado in that time.
        By default it does 5.
    dest_file: str
        Name of the destination file to save the csv (it must end in .csv).
        By default it names its by ./csv_files/url_thesis_{#number of thesis}.csv, where #number of thesis is the same number in n_rows.
    url_link: str
        It's the URL link where all the Pregado thesis are. By default it's http://saber.ucv.ve/handle/10872/2/browse?type=dateissued&sort_by=2&order=ASC&rpp={}&etal=0&submit_browse=Actualizar.

    Return:
    ---------
    None
    This function doesn't return anything, but it write a csv file with the info from thesis.
    """
    url_link = url_link.format(n_rows)
    n_source = s.get(url_link).text

    soup = BeautifulSoup(n_source, 'lxml')

    # This part gets all the links to the individual thesis
    content = soup.find('td', class_='pageContents')
    tdbody = content.find('table', class_='miscTable')
    tr = tdbody.find_all('tr')

    dest_file = dest_file.format(n_rows)
    csv_file = open(dest_file, 'w')

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['index', 'thesis_year','thesis_title','thesis_author','size','thesis_link','pdf_link', 'resumen'])

    progressbar_counter = 0
    l = n_rows
    for tds in tr[1:]:
        progressbar_counter +=1
        try:
            date = tds.find('td', headers='t1').strong.text
        except Exception as e:
            date = ""
        try:  
            title = tds.find('td', headers='t2').text
        except Exception as e:
            title = ""
        try:
            aref_old = tds.find('td', headers='t2').a['href']
            aref = 'http://saber.ucv.ve{}'.format(aref_old)
        except Exception as e:
            aref = ""
        try:
            aref_old = tds.find('td', headers='t2').a['href']
            aref = 'http://saber.ucv.ve{}'.format(aref_old)
            pdf_url = get_pdf_link(aref)
        except Exception as e:
            pdf_url = ""
        try:
            author = tds.find('td', headers='t3').text
        except Exception as e:
            author = ""
        try:
            size = getSize(aref)
        except Exception as e:
            size = ""
        try:
            resumen = ""
        except Exception as e:
            resumen = ""
        #print(date, title, author, size, aref)
        csv_writer.writerow([progressbar_counter, date, title, author, size, aref, pdf_url, resumen])
        #print(pdf_url + '\n')
        printProgressBar(progressbar_counter, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    csv_file.close()

if __name__ == '__main__':
    find_n_rows(8212)

