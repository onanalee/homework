import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta


# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')


songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
for song in songs:

    #title     #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.albumtitle.ellipsis
    #artist    #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
    #rank      #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number > span
    rank = song.select_one('td.number').text[0:2].strip()
    song_name = song.select_one('td.info > a.albumtitle.ellipsis').text
    artist = song.select_one('td.info > a.artist.ellipsis').text

    print(rank, song_name, artist)
    doc = {
        'rank': rank,
        'title': song_name,
        'artist': artist
    }
    db.songs.insert_one(doc)

