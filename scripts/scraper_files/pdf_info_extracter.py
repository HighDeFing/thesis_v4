from bs4 import BeautifulSoup
import requests
import csv
from urllib.request import unquote

# link http://saber.ucv.ve/handle/10872/17712

# This file holds functions for scraping the downloadable file and the size of the file.

def get_pdf_link(uri_path):
    """ Scraps the url link that has the downloadable pdf from the page.

    Parameters:
    -------------
    uri_path: str
        The url link of saber.ucv page that has the link for the pdf file.
        Example url: http://saber.ucv.ve/handle/10872/314

    Returns:
    -----------
    str
        A string with the pdf downloadable link.
        Example url: http://saber.ucv.ve/bitstream/10872/314/1/tesis_DD162dacevedo.PDF
    """
    source = requests.get(uri_path).text
    soup = BeautifulSoup(source, 'lxml')
    content = soup.find('td', class_='pageContents')
    table = content.find_all('table', class_='miscTable')[1]
    inside_table = table.find_all('tr')[2]
    td = inside_table.find('td', headers='t1')

    pdf_link = 'http://saber.ucv.ve{}'.format(td.a['href'])
    #print(pdf_link + '\n')
    return pdf_link

def get_resumen(uri_path):
    """ Scraps the summary of the file of the page.
    
    Parameters:
    -------------
    uri_path: str
        The url link of saber.ucv page that has the size.
        Example url: http://saber.ucv.ve/handle/10872/314

    Returns:
    -----------
    str
        A string with the summary.
        Example summary: Se realiza un estudio de sobretensiones por maniobra
        Se realiza un estudio de sobretensiones por maniobra dirigido hacia la simulación, determinación y análisis de las perturbaciones posibles en 
        las líneas de transmisión en 115kV comprendidas en la ampliación del sistema de 
        dirigido hacia la simulación, determinación y análisis de las perturbaciones posibles en las 
        líneas de transmisión en 115kV comprendidas en la ampliación del sistema de [...]
    """
    source = requests.get(uri_path).text
    soup = BeautifulSoup(source, 'lxml')
    content = soup.find('td', class_='pageContents')
    label_resumen = soup.find_all('td', class_='metadataFieldLabel')
    index_resumen = None
    for index, labels in enumerate(label_resumen):
        aux = labels.text.split()
        if aux[0].lower() == 'resumen':
            #print('There is a resume in index', index)
            index_resumen = index
            break
    if(index_resumen == None):
        return None
    inside_table = content.find_all('td', class_='metadataFieldValue')[index_resumen]
    #print(inside_table.text)
    return inside_table.text
    

def download_pdf(pdf_link):
    pdf_response = requests.get(pdf_link)
    filename = unquote(pdf_response.url).split('/')[-1].replace(' ', '_')
    #print(filename)
    with open('./pdf/' + filename, 'wb') as f:
        # write PDF to local file
        f.write(pdf_response.content)

def getSize(uri_path):
    """ Scraps the size of the file of the page.
    
    Parameters:
    -------------
    uri_path: str
        The url link of saber.ucv page that has the size.
        Example url: http://saber.ucv.ve/handle/10872/314

    Returns:
    -----------
    str
        A string with the size.
        Example sizes: 6.77 MB, 2 MB, 995.92 kB.
    
    """
    source = requests.get(uri_path).text
    soup = BeautifulSoup(source, 'lxml')
    content = soup.find('td', class_='pageContents')
    table = content.find_all('table', class_='miscTable')[1]
    inside_table = table.find_all('tr')[2]
    td = inside_table.find('td', headers='t3')
    #print(td.text)
    return td.text

if __name__ == '__main__':
    #something = get_pdf_link('http://saber.ucv.ve/handle/10872/17712')
    #download_url(something)
    get_resumen('http://saber.ucv.ve/handle/10872/16245')
    #getSize('http://saber.ucv.ve/handle/10872/17712')
