import requests
from bs4 import BeautifulSoup

url = "https://www.ufret.jp/song.php?data=156149"
html = requests.get(url)
##html.encoding = 'utf-8'
bs = BeautifulSoup(html.text, "html.parser")

title = bs.find("span", class_="show_name")
artist = bs.find("span", class_="show_artist")
chords = [c.text for c in bs.find_all("rt")]

print("楽曲名: " + title.get_text(strip=True))
print("アーティスト: " + artist.get_text(strip=True))
print(chords)