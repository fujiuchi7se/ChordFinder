import requests
from bs4 import BeautifulSoup
import re

# +2, +2, +1, +2, +2, +2
#s_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
#f_scale = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']
#R_scale = ['I', '♭I', '♯I', 'II', '♭II', '♯II', 'III', '♭III', '♯III', 'IV', '♭IV','♯IV', 'V', '♭V', '♯V', 'VI', '♭VI', '♯VI', 'VII', '♭VII', '♯VII']
# C_scale = [ 'C',  'D',   'E',  'F',  'G',  'A',   'B']
# D_scale = [ 'D',  'E',  'F#',  'G',  'A',  'B',  'C#']
# E_scale = [ 'E', 'F#',  'G#',  'A',  'B', 'C#',  'D#']
# F_scale = [ 'F',  'G',   'A', 'B♭',  'C',  'D',   'E']
# G_scale = [ 'G',  'A',   'B',  'C',  'D',  'E',  'F#']
# A_scale = [ 'A',  'B',  'C#',  'D',  'E', 'F#',  'G#']
# B_scale = [ 'B', 'C#',  'D#',  'E', 'F#', 'G#',  'A#']
# R_scale = [ 'I', 'II', 'III', 'IV',  'V', 'VI', 'VII']
#notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
#enharmonics = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#", "A#": "Bb", "D#": "Eb", "G#": "Ab",
               #"C#": "Db", "D#": "Eb", "F#": "Gb", "G#": "Ab", "A#": "Bb", "Bb": "A#", "Eb": "D#", "Ab": "G#",
#               "Cb": "B", "B#": "C", "E#": "F", "Fb": "E"}
major_intervals = [2, 2, 1, 2, 2, 2, 1]
degree_names = ["I", "II", "III", "IV", "V", "VI", "VII"]
notes_sharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
notes_flat = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# 調に基づいてスケールを取得する関数
def get_scale(root, use_sharp=True):
    if use_sharp:
        notes = notes_sharp
    else:
        notes = notes_flat
    
    start_index = notes.index(root)
    scale = [notes[start_index]]
    for interval in major_intervals:
        start_index = (start_index + interval) % 12
        scale.append(notes[start_index])
    
    return scale

# 調を解析してシャープを使うかフラットを使うかを判断する
def is_sharp_key(key):
    sharp_keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
    flat_keys = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb']
    if key in sharp_keys:
        return True
    elif key in flat_keys:
        return False
    elif 'b' in key:
        return False
    else:
        return True

# コードをディグリーネームに変換する関数
def chord_to_degree(chord, scale, use_sharp):
    chord_base = re.match(r'[A-G][#b]?', chord).group()
    chord_suffix = chord[len(chord_base):]
    
    if chord_base in scale:
        degree = scale.index(chord_base) + 1
        degree_name = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'][degree - 1]
        accidental = ''
        if use_sharp:
            if '#' in chord_base:
                accidental = '♯'
            elif 'b' in chord_base:
                accidental = '♭'
        else:
            if 'b' in chord_base:
                accidental = '♭'
            elif '#' in chord_base:
                accidental = '♯'
        return accidental + degree_name + chord_suffix
    return chord

# 入力されたコード進行をディグリーネームに変換する関数
def convert_chord_progression(chords, key):
    use_sharp = is_sharp_key(key)
    scale = get_scale(key, use_sharp)
    
    converted_chords = []
    for chord in chords:
        if 'on' in chord:
            base, slash = chord.split('on')
            base_converted = chord_to_degree(base, scale, use_sharp)
            slash_converted = chord_to_degree(slash, scale, use_sharp)
            converted_chords.append(f'{base_converted}/{slash_converted}')
        else:
            converted_chords.append(chord_to_degree(chord, scale, use_sharp))
    
    return converted_chords

url = 'https://gakufu.gakki.me/m/data/DT01794.html'
html = requests.get(url)
html.encoding = 'utf-8'
bs = BeautifulSoup(html.text, 'html.parser')

title = bs.find('h2', class_='tit').find('span').text.strip('「」')
artist = bs.find('h2', class_='tit').find('small').text
print('楽曲名: ' + title)
print('アーティスト: ' + artist)

key = 'E'
print('Key: ' + key)

#chords = [c.text for c in bs.find_all('span', class_='cd_fontpos')]
chords = ['AM7', 'C#m', 'AM7', 'BonC#', 'G#m', 'F#m7']
converted = convert_chord_progression(chords, key)
print(chords)
print(converted)
