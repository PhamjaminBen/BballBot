from BballBot.assets.player_lists import player_list,rostered_players
import difflib
from BballBot.assets.dbconnection import db_cursor,connection

db_cursor.execute("DROP TABLE IF EXISTS prev_teams")
connection.commit()
db_cursor.execute("CREATE TABLE prev_teams(name,team)")

for player in rostered_players:
  print(player)
  name = player[0]
  results = difflib.get_close_matches(name,player_list)
  if not not results:
    name = results[0]
    db_cursor.execute(f"Select tm from player_per_game where player_name = \"{name}\"")
    for team in set([x[0] for x in db_cursor.fetchall()]):
      db_cursor.execute(f"INSERT INTO prev_teams VALUES (\"{player[0]}\",\"{team}\")")
      connection.commit()

db_cursor.execute("CREATE INDEX name_index on prev_teams(name)")
connection.commit()