from email.policy import default
from BballBot.assets.dbconnection import db_cursor,connection
from collections import defaultdict
from bs4 import BeautifulSoup
import requests

def add_career_stats():
  db_cursor.execute("SELECT id from player_per_game")
  for i,(player,) in enumerate(set(db_cursor.fetchall())):
    if player[-1] == 'b':
      continue
    try:
      print(player,i)
      url = f"https://www.basketball-reference.com/players/{player[0]}/{player}.html"
      data = requests.get(url).text
      soup = BeautifulSoup(data, 'html.parser')
      tables = soup.find_all('table', id = "per_game")
      stats = defaultdict(float)
      for column in tables[0].tfoot.find_all('tr')[0].find_all('td'):
        try:
          num = float(column.text)
          stats[column.get('data-stat')] = num
        except:
          pass
    
      str1,str2 = '',''
      for k,v in stats.items():
        str1 += k+','
        str2 += str(v)+','
      str1 = str1[:-1]
      str2 = str2[:-1]
      db_cursor.execute(f"INSERT INTO player_career_per_game(id,{str1}) VALUES(\"{player}\",{str2})")
      connection.commit()
    except Exception as e:
      print(e.text)

add_career_stats()