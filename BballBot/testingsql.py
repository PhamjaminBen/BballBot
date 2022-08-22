# "C:\Users\Ben\Documents\GitHub\BballBot\nba_sql.db"
from basketball_reference_web_scraper import client as bclient
import sqlite3
import difflib
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
connection = sqlite3.connect('nba_sql.db')
c = connection.cursor()
c.execute("SELECT player_name from player")
players = [x[0] for x in c.fetchall()]



def per_game_calculation():
  c.execute("""
  UPDATE player_general_traditional_total
  SET ppg = pts/gp,
      rpg = reb/gp,
      apg = ast/gp,
      topg = tov/gp,
      spg = stl/gp,
      bpg = blk/gp,
      pfpg = pf/gp,
      mpg = min/gp
  """)

def add_mugshots():
  for player in players:
    try:
      print(player)
      id = bclient.search(term  = player)['players'][0]['identifier']
      pic = f"https://www.basketball-reference.com/req/202106291/images/players/{id}.jpg"
      c.execute(f"""UPDATE player
      SET mugshot = \"{pic}\" 
      WHERE player_name = \"{player}\";
      """)
      c.execute(f"select * from player where player_name = \"{player}\"")
      print(c.fetchall())
    except IndexError:
      print(player,"fail")
    
  c.execute("SELECT * from player limit 10")
  print(c.fetchall())

def add_identifiers():
  for player in players:
    try:
      id = bclient.search(term  = player)['players'][0]['identifier']
      c.execute(f"""UPDATE player
      SET bbref_id = \"{id}\"
      WHERE player_name = \"{player}\";
      """)
      connection.commit()
    except Exception as e:
      print("FAILED",player,e)

def win_loss_calculation():
  c.execute("UPDATE team SET w = (SELECT COUNT(*) FROM Game WHERE team_id_winner = team_id);")
  c.execute("UPDATE team SET l = (SELECT COUNT(*) FROM Game WHERE team_id_loser = team_id);")
  connection.commit()

def add_advanced():
  ids = set()
  while True:
    raw = input()
    if raw == "b":
      break
    raw = raw.split(",")[1:]
    if raw[-1] in ids:
      
      continue
    else:
      ids.add(raw[-1])
    
    formatter(raw)
    raw = ','.join(raw)
    print()
    c.execute(f"INSERT INTO player_per_game VALUES ({raw},1949)")
    connection.commit()
  
  c.execute("SELECT * FROM player_per_game limit 20;")
  print(c.fetchall())

def formatter(data: list):
  for i in range(len(data)):
    try:
      float(data[i])
    except:
      data[i] = "\""+data[i]+"\""


def test():
  c.execute("SELECT id from player_per_game")
  for i,(player,) in enumerate(set(c.fetchall())):
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
      c.execute(f"INSERT INTO player_career_per_game(id,{str1}) VALUES(\"{player}\",{str2})")
      connection.commit()
    except Exception as e:
      print(e.text)
  # del stats['age']
  # for x,y in stats.items():
  #   if x not in ['g','gs']:
  #     stats[x] = y/len(years)
  #     if 'pct' in x:
  #       stats[x] = round(stats[x],3)
  #     else:
  #       stats[x] = round(stats[x],1)
  
  # print(stats,len(years))

if __name__ == "__main__":
  test()