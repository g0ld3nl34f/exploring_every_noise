from sys import path
path.append('../')
from time import sleep
from numpy.random import choice
import pandas as pd
from every_noise_genre_scraper import extract_genres

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

        accept_suggestion = input('How about trying {}? (A)ccept or (G)et another?\n'.format(genre_csv.iloc[genre_choice, 1]))

        if accept_suggestion == 'A':
            print('♬ Enjoy {}! ♬'.format(genre_csv.iloc[genre_choice, 1]))
            sleep(2)
            
            print('{}: https://open.spotify.com/playlist/{} (follow link for a preview playlist made by Every Noise at Once)'.format(
                (genre_csv.iloc[genre_choice, 1]), (genre_csv.iloc[genre_choice, 2]).split(':')[-1]))
            break
        
        else:
            print("Let's find you another genre.")
            sleep(2)
        



