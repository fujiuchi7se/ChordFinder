from bs4 import BeautifulSoup
import re
import csv

# 音名を対応する数字に変換する関数
def ntn(note):
    note_dict = {
        'C#': 0, 'Db': 0,'D': 1, 'D#': 0, 'Eb': 0,'E': 1, 'F': 0, 
        'G': 1, 'G#': 0, 'Ab': 0, 'A': 1, 'A#': 0, 'Bb': 0,'B': 1
    }
    return note_dict.get(note, note)

# コード進行を合計文字数が100文字以下になるように分割する関数
def split_chords(chords, max_length=50):
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
csv_file_name = 'train.csv'
data = [['label', 'sentence']]

for i in range(79):
    try:
        with open(r'songs/{}.html'.format(i), 'r', encoding='utf-8') as file:
            html = file.read()
    except FileNotFoundError:
        continue  # HTMLファイルが存在しない場合はスキップ
    bs = BeautifulSoup(html, 'html.parser')

    #title = bs.find('h1', class_='title').text
    #artist = bs.find('h2', class_='subtitle').text
    key = bs.find('p', class_='key').text.strip('Key: ')
    chords = [c.text.strip('|>/-↓=') for c in bs.find_all('span', class_='chord')]
    nchords = [re.sub(r'\(.*?\)', ' ', chord) for chord in chords if chord not in [' ', 'N.C.']]
    nchords = [chord.strip('() ') for chord in nchords if chord.strip()]

    chord_groups = split_chords(nchords)
    
    # 初めの2つのリストを格納
    for group in chord_groups[:4]:
        joined_chords = ' '.join(group)
        data.append([ntn(key), joined_chords])
        
# CSVファイルにデータを書き込む
with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(data)

# CSVファイルの名前
csv_file_name = 'validation.csv'
vdata = [['label', 'sentence']]
for i in range(80, 99):
    try:
        with open(r'songs/{}.html'.format(i), 'r', encoding='utf-8') as file:
            html = file.read()
    except FileNotFoundError:
        continue  # HTMLファイルが存在しない場合はスキップ
    bs = BeautifulSoup(html, 'html.parser')

    #title = bs.find('h1', class_='title').text
    #artist = bs.find('h2', class_='subtitle').text
    key = bs.find('p', class_='key').text.strip('Key: ')
    chords = [c.text.strip('|>/-↓=') for c in bs.find_all('span', class_='chord')]
    nchords = [re.sub(r'\(.*?\)', ' ', chord) for chord in chords if chord not in [' ', 'N.C.']]
    nchords = [chord.strip('() ') for chord in nchords if chord.strip()]

    chord_groups = split_chords(nchords)
    
    # 初めの2つのリストを格納
    for group in chord_groups[:4]:
        joined_chords = ' '.join(group)
        vdata.append([ntn(key), joined_chords])
        
# CSVファイルにデータを書き込む
with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(vdata)

# ■評価結果
# Accuracy: 0.9166666666666666
# Precision: 0.9171301446051168
# Recall: 0.9166666666666667

# ■RandomForest
# Accuracy: 0.85
# Precision: 0.8535353535353536
# Recall: 0.8500000000000001
# ■XGBoost
# Accuracy: 0.8666666666666667
# Precision: 0.8683035714285714
# Recall: 0.8666666666666667
# ■LightGBM
# Accuracy: 0.9333333333333333
# Precision: 0.9352678571428572
# Recall: 0.9333333333333333

# ■評価結果
# Accuracy: 0.8947368421052632
# Precision: 0.8944444444444444
# Recall: 0.8944444444444444

# ■RandomForest
# Accuracy: 0.8552631578947368
# Precision: 0.8595818815331011
# Recall: 0.8583333333333334
# ■XGBoost
# Accuracy: 0.8421052631578947
# Precision: 0.8421052631578947
# Recall: 0.8430555555555556
# ■LightGBM
# Accuracy: 0.881578947368421
# Precision: 0.8811503811503811
# Recall: 0.8819444444444444