import requests
from bs4 import BeautifulSoup
import os
import re

GENIUS_API_TOKEN='cC-xIjHvk_L0UaJyCqCgHHBOT8eAYad0Cv2GpaLlZRkfN0oh-B-tl_bIQPPJRLZe'


# Functio to request artist data from Genius API
def request_artist(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response


#function for requesting song urls from the Genius API
def request_song(artist_name, song_cap):
    page = 1
    songs = []

    while True:
        response = request_artist(artist_name, page)
        json = response.json()
        # Collect up to song_cap song objects from artist
        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)

        # Collect song URL's from song objects
        for song in song_info:
            if (len(songs) < song_cap):
                url = song['result']['url']
                songs.append(url)

        if (len(songs) == song_cap):
            break
        else:
            page += 1

    print('Found {} songs by {}'.format(len(songs), artist_name))

    return songs


#scrapes lyrics through genius API given song url
def scrape_song(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    #remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics

#writes scrapes lyrics to a new file
def write_lyrics(artist_name, song_count):
    f = open('/Users/jacobfarner/PycharmProjects/SpotifyTest/' + artist_name.lower() + '.txt', 'wb')
    urls = request_song(artist_name, song_count)
    for url in urls:
        lyrics = scrape_song(url)
        f.write(lyrics.encode("utf8"))
    f.close()
    num_lines = sum(1 for line in open('/Users/jacobfarner/PycharmProjects/SpotifyTest/' + artist_name.lower() + '.txt', 'rb'))
    print('Wrote {} lines to file from {} songs'.format(num_lines, song_count))



write_lyrics('Drake', 100)
