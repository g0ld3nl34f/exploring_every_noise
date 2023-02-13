from sys import path
path.append('../')
from time import sleep
from numpy.random import choice
import requests
from bs4 import BeautifulSoup
import pandas as pd
from every_noise_genre_scraper import extract_genres

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/103.0'}

def get_intro_playlist_url(paper_url):

    #download the page
    response=requests.get(paper_url,headers=headers)

    # check successful response
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ')

    #parse using beautiful soup
    paper_doc = BeautifulSoup(response.text,'html.parser')
    
    link_if_available = paper_doc.find_all('a', {'style': 'color: #a6a6a6'})

    if len(link_if_available) == 0:
        return None

    return link_if_available[0].get('href')

if __name__ == '__main__':
    genre_csv = None

    while(True):
        x = input('Need to extract genres?\n(Y) -> Extract\n(N) -> Proceed (Already extracted previously)\n')
        
        if x == 'Y':
            extract_genres()
            print('Extracted genres!')
            genre_csv = pd.read_csv('every_noise_genre.csv')
            break
        
        elif x == 'N':
            print('Checking genres...')
            sleep(2)
            try:
                genre_csv = pd.read_csv('every_noise_genre.csv')
                print('Found genres.')
                sleep(2)
                break
            except:
                print('Please extract genres!')
                sleep(2)

        else:
            print('Please input one of the options!')
            sleep(2)
    
    while(True):
        genre_choice = choice([i for i in range(genre_csv.shape[0])], size=1, replace=False)[0]
        link_to_intro = None
        
        while(link_to_intro is None):
            genre_url = "".join(list([val for val in genre_csv.iloc[genre_choice, 1]
            if val.isalpha() or val.isnumeric()]))

            link_available = get_intro_playlist_url('https://everynoise.com/engenremap-{}.html'.format(genre_url))

            if link_available is None:
                print('No intro playlist for {}. Retrying...'.format(genre_csv.iloc[genre_choice, 1]))
                sleep(2)
                continue
            
            link_to_intro = link_available
            
        accept_suggestion = input('How about getting to know {}? (A)ccept or (G)et another?\n'.format(genre_csv.iloc[genre_choice, 1]))

        if accept_suggestion == 'A':
            print('♬ Enjoy an intro to {}! ♬'.format(genre_csv.iloc[genre_choice, 1]))
            sleep(2)
            
            print('{}: {} (follow link to the playlist made by Every Noise at Once)'.format(
                (genre_csv.iloc[genre_choice, 1]), link_available))
            break

        else:
            print("Let's find you another genre.")
            sleep(2)