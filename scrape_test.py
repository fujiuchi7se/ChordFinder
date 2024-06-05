import requests
from bs4 import BeautifulSoup

major_intervals = [2, 2, 1, 2, 2, 2, 1]
degree_names = ["I", "II", "III", "IV", "V", "VI", "VII"]
notes_sharp = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']
notes_flat = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']
sharp_keys = ['G', 'D', 'A', 'E', 'B', 'F♯']   # ♯, ♯♯, ...
flat_keys = ['F', 'B♭', 'E♭', 'A♭', 'D♭', 'G♭'] # ♭, ♭♭, ...

# 'on' -> '/'
#  '#' -> '♯' (efbc83 -> e299af)
def shape(chords):
    return [c.replace('on', '/').replace('\uFF03', '\u266F') for c in chords]

# get scale from key
def getScale(key):
    notes = notes_sharp if key in sharp_keys else notes_flat
    
    scale = []
    i = notes.index(key)
    for j in major_intervals:
        scale.append(notes[i])
        i = (i + j) % 12
    
    return scale

# convert chords to degree name
def toDegree(chords, key):
    chords = shape(chords)
    scale = getScale(key)
    chords_degree = []
    for c in chords:
        replaced_chord = c
        for i in range(len(degree_names)):
            replaced_chord = replaced_chord.replace(scale[i], degree_names[i])
        chords_degree.append(replaced_chord)
    return chords_degree

url = 'https://gakufu.gakki.me/m/data/DT01794.html'
html = requests.get(url)
html.encoding = 'UTF-8'
bs = BeautifulSoup(html.text, 'html.parser')

title = bs.find('h2', class_='tit').find('span').text.strip('「」')
artist = bs.find('h2', class_='tit').find('small').text
print('楽曲名: ' + title)
print('アーティスト: ' + artist)

key = 'E'
print('Key: ' + key)
print(getScale(key))

chords = [c.text for c in bs.find_all('span', class_='cd_fontpos')]
print(chords)
print()

chords = toDegree(chords, key)
print(chords)
