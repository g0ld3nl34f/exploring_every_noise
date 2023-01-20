import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
import re

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/103.0'}

# this function for the getting inforamtion of the web page
def get_genre_info(paper_url):

  #download the page
  response=requests.get(url,headers=headers)

  # check successful response
  if response.status_code != 200:
    print('Status code:', response.status_code)
    raise Exception('Failed to fetch web page ')

  #parse using beautiful soup
  paper_doc = BeautifulSoup(response.text,'html.parser')

  return paper_doc

# this function for the extracting information of the tags
def get_tags(doc):
  table_tag = doc.find_all('table')[0]

  return table_tag

def extract_genres():
    genre_numbers, genre_names, links = [], [], []

    # get url for the each page
    url = 'https://everynoise.com/everynoise1d.cgi?vector=popularity&scope=all'

    # function for the get content of each page
    doc = get_genre_info(url)
    # function for the collecting tags
    table = get_tags(doc)

    for row in tqdm(table.find_all('tr')):
      genre_number = row.find('td').text # Since it is the first column, can be just this
      genre_name = [a.text for a in row.find_all('a')][1] # Select second column element in a text span
      link = [a['href'] for a in row.find_all('a')][0]
      
      genre_numbers.append(genre_number)
      genre_names.append(genre_name)
      links.append(link)

    final = pd.DataFrame(data={'Number': genre_numbers, 'Genre': genre_names, 'Link': links})
    final.to_csv('every_noise_genre.csv', sep=',', index=False, header=True)