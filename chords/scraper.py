import requests
from bs4 import BeautifulSoup
from .models import ChordProgression

def get_song_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    song_title = soup.find('h1').text
    singer = soup.find('div', {'class': 'singer'}).text
    key = soup.find('div', {'class': 'key'}).text
    progression = soup.find('div', {'id': 'chord_section'}).text

    return {
        'song_title': song_title,
        'singer': singer,
        'key': key,
        'progression': progression,
        'url': url
    }

def save_song_data(song_data):
    ChordProgression.objects.create(
        song_title=song_data['song_title'],
        singer=song_data['singer'],
        key=song_data['key'],
        progression=song_data['progression'],
        url=song_data['url']
    )

def main():
    ## スクレイピング無理かも
    url = 'https://www.ufret.jp/song.php?data=156149'
    response = requests.get(url)
    print(response.text)
    ##song_data = get_song_data(url)
    ##if song_data:
    ##    save_song_data(song_data)
    ##else:
    ##    print('Failed to retrieve song data.')

if __name__ == "__main__":
    main()