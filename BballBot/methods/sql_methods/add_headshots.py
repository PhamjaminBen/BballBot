from BballBot.assets.dbconnection import db_cursor, player_list
from basketball_reference_web_scraper import client

def add_headshots():
  for player in player_list:
    try:
      print(player)
      id = client.search(term  = player)['players'][0]['identifier']
      pic = f"https://www.basketball-reference.com/req/202106291/images/players/{id}.jpg"
      db_cursor.execute(f"""UPDATE player
      SET mugshot = \"{pic}\" 
      WHERE player_name = \"{player}\";
      """)
      db_cursor.execute(f"select * from player where player_name = \"{player}\"")
      print(db_cursor.fetchall())
    except IndexError:
      print(player,"fail")
    
  db_cursor.execute("SELECT * from player limit 10")

add_headshots()