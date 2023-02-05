from sys import path
from pathlib import Path
path.insert(0, Path('.').absolute().parent.__str__())

from time import sleep
from numpy.random import choice
import pandas as pd
from every_noise_genre_scraper import extract_playlists_by_country

if __name__ == '__main__':
    needle_csv = None

    while(True):
        x = input('Need to extract Neddle playlists?\n(Y) -> Extract\n(N) -> Proceed (Already extracted previously)\n')
        
        if x == 'Y':
            extract_playlists_by_country()
            print('Extracted playlists!')
            needle_csv = pd.read_csv('every_noise_needle.csv')
            break
        
        elif x == 'N':
            print('Checking Needle...')
            sleep(2)
            try:
                needle_csv = pd.read_csv('every_noise_needle.csv')
                print('Found playlists.')
                sleep(2)
                break
            except:
                print('Please extract Needle playlists!')

        else:
            print('Please input one of the options!')
            sleep(2)
    
    country_list = needle_csv.iloc[:, 0]
    
    while(True):
        print("What would you like to find from the Needle?")
        routine0 = "1 -> Random country playlist"
        routine1 = "2 -> Random country Current playlist"
        routine2 = "3 -> Random country Emergent playlist (if available)"
        routine3 = "4 -> Random country Underground playlist (if available)"
        routine_choice = input(routine0 + '\n' + routine1 + '\n' + routine2 + '\n' + routine3 + '\n')

        if routine_choice == '1':
            while(True):
                country_choice = choice([i for i in range(needle_csv.shape[0])], size=1, replace=False)[0]
                accept_suggestion = input('From {}? (A)ccept or (G)et another?\n'.format(country_list[country_choice]))

                if accept_suggestion == 'A':
                    print('Follow the link to hear the playlist from {}: https://open.spotify.com/playlist/{}'.format(
                        (country_list[country_choice]), (needle_csv.iloc[country_choice, 1]).split(':')[-1]))
                    break
            break
        elif routine_choice == '2':
            while(True):
                country_choice = choice([i for i in range(needle_csv.shape[0])], size=1, replace=False)[0]

                if needle_csv.iloc[country_choice, 2] == 'No playlist.':
                    continue

                accept_suggestion = input('From {}? (A)ccept or (G)et another?\n'.format(country_list[country_choice]))

                if accept_suggestion == 'A':
                    print('Follow the link to hear the Current playlist from {}: https://open.spotify.com/playlist/{}'.format(
                        (country_list[country_choice]), (needle_csv.iloc[country_choice, 2]).split(':')[-1]))
                    break
            break
        elif routine_choice == '3':
            while(True):
                country_choice = choice([i for i in range(needle_csv.shape[0])], size=1, replace=False)[0]
 
                if needle_csv.iloc[country_choice, 3] == 'No playlist.':
                    continue

                accept_suggestion = input('From {}? (A)ccept or (G)et another?\n'.format(country_list[country_choice]))

                if accept_suggestion == 'A':
                    print('Follow the link to hear the Emergent playlist from {}: https://open.spotify.com/playlist/{}'.format(
                        (country_list[country_choice]), (needle_csv.iloc[country_choice, 3]).split(':')[-1]))
                    break
            break
        elif routine_choice == '4':
            while(True):
                country_choice = choice([i for i in range(needle_csv.shape[0])], size=1, replace=False)[0]
                
                if needle_csv.iloc[country_choice, 4] == 'No playlist.':
                    continue
                
                accept_suggestion = input('From {}? (A)ccept or (G)et another?\n'.format(country_list[country_choice]))

                if accept_suggestion == 'A':
                    print('Follow the link to hear the Underground playlist from {}: https://open.spotify.com/playlist/{}'.format(
                        (country_list[country_choice]), (needle_csv.iloc[country_choice, 4]).split(':')[-1]))
                    break
            break
        else:
            print('Choose one of the routines!')
            sleep(2)