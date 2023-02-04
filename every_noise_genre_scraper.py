import copy
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
import re
from natsort import natsorted


headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/103.0'}


# this function for the getting inforamtion of the web page
def get_doc_info(paper_url):

	#download the page
	response=requests.get(paper_url,headers=headers)

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


def get_cp_info(doc):
	playlists = doc.find_all('div', {'class': 'plink'})

	return playlists


def extract_genres():
	genre_numbers, genre_names, links = [], [], []

	# get url for the each page
	url = 'https://everynoise.com/everynoise1d.cgi?vector=popularity&scope=all'

	# function for the get content of each page
	doc = get_doc_info(url)
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

	print('Collected playlists by genre ♬')


def extract_playlists_by_country():
	countries_names, general_playlists, current_playlists, emerging_playlists, underground_playlists = [], [], [], [], []
	countries_aux = []

	url = 'https://everynoise.com/theneedle.html'

	doc = get_doc_info(url)
	countries_playlists = get_cp_info(doc)

	names_plus_playlists = []
	for playlist in countries_playlists:
		names_plus_playlists.append([playlist.get_text(), playlist.a['href']])
	names_plus_playlists.sort(key= lambda names_plus_playlists: names_plus_playlists[0])

	countries_aux = np.unique(np.asarray([curr_pl[0].split('/')[1].split('-')[0].strip() for curr_pl in names_plus_playlists[4:]]))
	
	# Since Timor-Leste is the only country with an hyphen, its individually replaced by the current name
	where_is_timor = np.where(countries_aux == 'Timor')[0]
	countries_aux[where_is_timor] = 'Timor-Leste'
	
	countries_names.append('Global')
	general_playlists.append(names_plus_playlists[0][1])
	current_playlists.append(names_plus_playlists[1][1])
	emerging_playlists.append(names_plus_playlists[2][1])
	underground_playlists.append(names_plus_playlists[3][1])

	for country in countries_aux:
		country_needle_playlists = natsorted([pl for pl in names_plus_playlists if country in pl[0]])
		cnp_aux = copy.deepcopy(country_needle_playlists)

		for i in cnp_aux:
			curr_country = i[0].split(' / ')[1].split(' - ')[0]
			if curr_country != country:
				country_needle_playlists.remove(i)

		countries_names.append(country)
		number_playlists = len(country_needle_playlists)

		if number_playlists == 1:
			general_playlists.append(country_needle_playlists[0][1])
			current_playlists.append('No playlist.')
			emerging_playlists.append('No playlist.')
			underground_playlists.append('No playlist.')
		elif number_playlists == 2:
			general_playlists.append(country_needle_playlists[0][1])
			current_playlists.append(country_needle_playlists[1][1])
			emerging_playlists.append('No playlist.')
			underground_playlists.append('No playlist.')
		elif number_playlists == 3:
			general_playlists.append(country_needle_playlists[0][1])
			current_playlists.append(country_needle_playlists[1][1])
			emerging_playlists.append(country_needle_playlists[2][1])
			underground_playlists.append('No playlist.')
		elif number_playlists == 4:
			general_playlists.append(country_needle_playlists[0][1])
			current_playlists.append(country_needle_playlists[1][1])
			emerging_playlists.append(country_needle_playlists[2][1])
			underground_playlists.append(country_needle_playlists[3][1])
		else:
			print(country)
			print(country_needle_playlists)
			print('Ops')
			raise KeyError


	final = pd.DataFrame(data={'Country': countries_names, 
								'General': general_playlists, 
								'Current': current_playlists,
								'Emerging': emerging_playlists,
								'Underground': underground_playlists})
	final.to_csv('every_noise_needle.csv', sep=',', index=False, header=True)

	print('Collected Needle playlists by country ♬')