from bs4 import BeautifulSoup
import re
import csv

# 音名を対応する数字に変換する関数
def ntn(note):
    note_dict = {
        'C': 0, 'C#': -5, 'Db': -5,
        'D': 2, 'D#': -3, 'Eb': -3,
        'E': 4,  'F': -1, 'F#': -6,
        'Gb': -6, 'G': 1, 'G#': -4, 
        'Ab': -4, 'A': 3, 'A#': -2, 
        'Bb': -2,'B': 5
    }
    return note_dict.get(note, note)

# コード進行を合計文字数が100文字以下になるように分割する関数
def split_chords(chords, max_length=30):
    groups = []
    current_group = []
    current_length = 0
    
    for chord in chords:
        chord_length = len(chord)
        if current_length + chord_length > max_length:
            if current_group:
                groups.append(current_group)
                current_group = []
                current_length = 0
        current_group.append(chord)
        current_length += chord_length
    
    # 最後のグループを追加
    if current_group:
        groups.append(current_group)
    
    return groups

# CSVファイルの名前
csv_file_name = 'songdata.csv'
data = [['label', 'sentence']]

for i in range(120):
    with open(r'songs/{}.html'.format(i), 'r', encoding='utf-8') as file:
        html = file.read()
    bs = BeautifulSoup(html, 'html.parser')

    #title = bs.find('h1', class_='title').text
    #artist = bs.find('h2', class_='subtitle').text
    key = bs.find('p', class_='key').text.strip('Key: ')
    chords = [c.text.strip('|>/--') for c in bs.find_all('span', class_='chord')]
    nchords = [re.sub(r'\(.*?\)', ' ', chord) for chord in chords if chord not in [' ', 'N.C.']]
    nchords = [chord.strip('()↓ ') for chord in nchords if chord.strip()]

    chord_groups = split_chords(nchords)
    
    # 初めの2つのリストを格納
    for group in chord_groups:
        data.append([ntn(key), group])

# CSVファイルにデータを書き込む
with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(data)
