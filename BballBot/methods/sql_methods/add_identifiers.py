from BballBot.assets.dbconnection import connection,db_cursor,player_list
from basketball_reference_web_scraper import client

def add_identifiers():
  for player in player_list:
    try:
      id = client.search(term  = player)['players'][0]['identifier']
      db_cursor.execute(f"""UPDATE player
      SET bbref_id = \"{id}\"
      WHERE player_name = \"{player}\";
      """)
      connection.commit()
    except Exception as e:
      print("FAILED",player,e)

add_identifiers()