from BballBot.assets.dbconnection import db_cursor, connection
from BballBot.assets.team_urls import team_abbr_list,team_url_list
from bs4 import BeautifulSoup
import requests


def add_current_players():
  db_cursor.execute("DROP TABLE IF EXISTS rostered_players")
  connection.commit()
  db_cursor.execute(
    """CREATE TABLE rostered_players(
      player_name,jersey,pos,height,weight,bithday,age,exp,school,team)""")
  connection.commit()

  for abbr,url in zip(team_abbr_list,team_url_list):
    print(abbr)
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find_all('table')[0]
    
    for row in table.tbody.find_all('tr'):
      data = [f"\"{col.text}\"" if col.text != "" else "\"-\"" for col in row.find_all('td')]
      datastr = ','.join(data)
      db_cursor.execute(f"INSERT INTO rostered_players VALUES ({datastr},\"{abbr}\");")
      connection.commit()

add_current_players()