import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
sleep_min = 2
sleep_max = 5
start_time = time.time()
request_count = 0

#must enter personal id and secret in order to authenticate
client_id = ''
client_secret = 'b'

#authorizing access to spotify data
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret = client_secret)


#creating spotify object in order to access API
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


#user enters artist name for features they want to extract
name = input("Enter an artist: ")

#inputing artist into query
result = sp.search(name)

#returning artist page data
print(result['tracks']['items'][0]['artists'])


#extracting album URIs from artist
artist_uri = result['tracks']['items'][0]['artists'][0]['uri']

#extracting albums using uri
sp_albums = sp.artist_albums(artist_uri, album_type='album')


#storing artists names and uris into separate lists
album_names = []
album_uris = []

for i in range(len(sp_albums['items'])):
    album_names.append(sp_albums['items'][i]['name'])
    album_uris.append(sp_albums['items'][i]['uri'])


print(name.title(),"Album URIs:", album_uris)


#extract songs from each album through uri
def albumSongs(uri):
    album = uri

    #create dictionary for each album
    spotify_albums[album] = {}
    spotify_albums[album]['album'] = [] #create empty list
    spotify_albums[album]['track_number'] = []
    spotify_albums[album]['id'] = []
    spotify_albums[album]['name'] = []
    spotify_albums[album]['uri'] = []


    #extracting data for each album track
    tracks = sp.album_tracks(album)

    #iterate and extract dataa for each song in an album
    for n in range(len(tracks['items'])): #for each song track
        spotify_albums[album]['album'].append(album_names[album_count]) #append album name tracked via album_count
        spotify_albums[album]['track_number'].append(tracks['items'][n]['track_number'])
        spotify_albums[album]['id'].append(tracks['items'][n]['id'])
        spotify_albums[album]['name'].append(tracks['items'][n]['name'])
        spotify_albums[album]['uri'].append(tracks['items'][n]['uri'])


spotify_albums = {}
album_count = 0

#iterates through each album
for i in album_uris:
    albumSongs(i)
    print(name.title() + " Album " + str(album_names[album_count]) + " songs has been added to spotify_albums dictionary")
    album_count+=1


def audio_features(album):
    # Add new key-values to store audio features
    spotify_albums[album]['acousticness'] = []
    spotify_albums[album]['danceability'] = []
    spotify_albums[album]['energy'] = []
    spotify_albums[album]['instrumentalness'] = []
    spotify_albums[album]['liveness'] = []
    spotify_albums[album]['loudness'] = []
    spotify_albums[album]['speechiness'] = []
    spotify_albums[album]['tempo'] = []
    spotify_albums[album]['valence'] = []
    spotify_albums[album]['popularity'] = []
    # create a track counter
    track_count = 0
    for track in spotify_albums[album]['uri']:
        # pull audio features per track
        features = sp.audio_features(track)

        # Append to relevant key-value
        spotify_albums[album]['acousticness'].append(features[0]['acousticness'])
        spotify_albums[album]['danceability'].append(features[0]['danceability'])
        spotify_albums[album]['energy'].append(features[0]['energy'])
        spotify_albums[album]['instrumentalness'].append(features[0]['instrumentalness'])
        spotify_albums[album]['liveness'].append(features[0]['liveness'])
        spotify_albums[album]['loudness'].append(features[0]['loudness'])
        spotify_albums[album]['speechiness'].append(features[0]['speechiness'])
        spotify_albums[album]['tempo'].append(features[0]['tempo'])
        spotify_albums[album]['valence'].append(features[0]['valence'])
        # popularity is stored elsewhere
        pop = sp.track(track)
        spotify_albums[album]['popularity'].append(pop['popularity'])
        track_count += 1

 #extracting audio features for each song in each album
for i in spotify_albums:
    audio_features(i)
    request_count+=1
    if request_count % 5 == 0:
        print(str(request_count) + "playlists completed")

dic_df = {}
dic_df['album'] = []
dic_df['track_number'] = []
dic_df['id'] = []
dic_df['name'] = []
dic_df['uri'] = []
dic_df['acousticness'] = []
dic_df['danceability'] = []
dic_df['energy'] = []
dic_df['instrumentalness'] = []
dic_df['liveness'] = []
dic_df['loudness'] = []
dic_df['speechiness'] = []
dic_df['tempo'] = []
dic_df['valence'] = []
dic_df['popularity'] = []
for album in spotify_albums:
    for feature in spotify_albums[album]:
        dic_df[feature].extend(spotify_albums[album][feature])

len(dic_df['album'])

df = pd.DataFrame.from_dict(dic_df)

df = pd.DataFrame.from_dict(dic_df)
print(df)


print(len(df))
clean_df = df.sort_values('popularity', ascending = False).drop_duplicates('name').sort_index()

av_column = df.mean(axis=0)
print(av_column)

#input path
clean_df.to_csv("path...../features.csv")

labels = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Speechiness', 'valence']
markers = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
str_markers = ["0", ".1", ".2", ".3", ".4", ".5", ".6," ".7", ".8", ".9", "1"]


#making a spider chart for findings
def make_radar_chart(title, stats, attribute_labels = labels, plot_markers = markers, plot_str_markers = str_markers ):

    labels = np.array(attribute_labels)

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    stats = np.concatenate((stats,[stats[0]]))
    angles = np.concatenate((angles,[angles[0]]))

    fig= plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, labels)
    plt.yticks(markers)
    ax.set_title(title)
    ax.grid(True)

    #input directory for saving graphs
    fig.savefig("path.../%s.png" % name)

    return plt.show()



#df2 = av_column


#converting dataframe to list for visualization
val_list=av_column.values.tolist()
index_selection = [1,2,3,4,7,9]

to_graph = [val_list[i] for i in index_selection]
print(to_graph)
)
make_radar_chart(name.title() + " Average Acoustic Features", to_graph) # example


