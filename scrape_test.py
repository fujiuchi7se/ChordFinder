import requests
from bs4 import BeautifulSoup

ascale = ["C", "C♭", "C＃", "D", "D♭", "D＃", "E", "E♭", "E＃", "F", "F♭","F＃", "G", "G♭", "G＃", "A", "A♭", "A＃", "B", "B♭", "B＃"]
rscale = ["I", "♭I", "♯I", "II", "♭II", "♯II", "III", "♭III", "♯III", "IV", "♭IV","♯IV", "V", "♭V", "♯V", "VI", "♭VI", "♯VI", "VII", "♭VII", "♯VII"]

url = "https://gakufu.gakki.me/m/data/DT01794.html"
html = requests.get(url)
html.encoding = 'utf-8'
bs = BeautifulSoup(html.text, "html.parser")

title = bs.find("h2", class_="tit").find("span").text.strip("「」")
artist = bs.find('h2', class_='tit').find('small').text
print("楽曲名: " + title)
print("アーティスト: " + artist)

key = "E"
print("Key: " + key)

chords = [c.text for c in bs.find_all("span", class_="cd_fontpos")]
for i in chords:
    #for j in range(len(ascale)):
        print(i.replace("A", " "))
