from bs4 import BeautifulSoup
import re
import csv

# 10 10  10 10 10 10 10 10 10 10 10 10
# -3  5 -2 -1  4  0  1 -4 -6  2  3 -5
# A#, Bb, Gm
def ntn(note):
    # 音名と対応する数字を辞書に定義
    note_dict = {
        'C': 0, 'C#': -5, 'Db': -5,
        'D': 2, 'D#': -3, 'Eb': -3,
        'E': 4,  'F': -1, 'F#': -6,
        'Gb': -6, 'G': 1, 'G#': -4, 
        'Ab': -4, 'A': 3, 'A#': -2, 
        'Bb': -2,'B': 5
    }
    
    # 音名を大文字に変換し、辞書を使って対応する数字を返す
    return note_dict.get(note, note)

# CSVファイルの名前
csv_file_name = 'songdata.csv'

# CSVファイルに書き込むためのリストを初期化
data = [['label', 'sentence']]

for i in range(120):
    with open(r'songs\{}.html'.format(i), 'r', encoding='utf-8') as file:
        html = file.read()
    bs = BeautifulSoup(html, 'html.parser')

    title = bs.find('h1', class_='title').text
    artist = bs.find('h2', class_='subtitle').text
    key = bs.find('p', class_='key').text.strip('Key: ')
    chords = [c.text.strip('|>/--') for c in bs.find_all('span', class_='chord')]
    nchords = [re.sub(r'\(.*?\)', ' ', chord) for chord in chords if chord not in [' ', 'N.C.']]
    nchords = [chord for chord in nchords if chord.strip()]
    nchords = nchords[:61]
    # データをリストに追加
    data.append([ntn(key), nchords])

# CSVファイルにデータを書き込む
with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(data)