import requests
from bs4 import BeautifulSoup
import os
import re

#You must insert your own authentication token
GENIUS_API_TOKEN='INSERT TOKEN'



def request_artist(artist_name, page):
    '''
    This function requests artist data from Genius
    
    artist_name = artist to selected data on 
    page = artist url info
    '''
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response



def request_song(artist_name, song_cap):
    '''
    This function requests specific song data
    
    artist_name = artists to request song information from
    song_cap = limits the number of songs requested for artists with large discographies
    
    '''
    
    page = 1
    songs = []

    while True:
        response = request_artist(artist_name, page)
        json = response.json()
       
    # Limiting script to collect data on song_cap number of songs
        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)

        # Collecting URLs from song objects
        for song in song_info:
            if (len(songs) < song_cap):
                url = song['result']['url']
                songs.append(url)

        if (len(songs) == song_cap):
            break
        else:
            page += 1

    print('Successfully scraped {} songs by {}'.format(len(songs), artist_name))

    return songs



def scrape_song(url):
    '''
    This function requests lyrics through the API based on song URL
    
    url = individual song url
    '''
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    #removing labels within lyric data (ex: chorus, verse etc...)
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #removing empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics


def write_lyrics(artist_name, song_count):
    '''
    This function writes collected lyrics to a new text file
    artist_name = user selected artist -> used in .txt creation for organization
    song_count = limits number of songs written
    '''
    f = open('/path' + artist_name.lower() + '.txt', 'wb')
    urls = request_song(artist_name, song_count)
    for url in urls:
        lyrics = scrape_song(url)
        f.write(lyrics.encode("utf8"))
    f.close()
    num_lines = sum(1 for line in open('/path' + artist_name.lower() + '.txt', 'rb'))
    print('Successfully wrote {} lines to new text file based on {} songs'.format(num_lines, song_count))


write_lyrics('Drake', 100)
