import sqlite3

connection = sqlite3.connect('BballBot/nba_sql.db')
db_cursor = connection.cursor()

db_cursor.execute("""
  SELECT player_name,team,conference,division,pos,height,age,jersey 
  FROM rostered_players,team 
  WHERE rostered_players.team = team.abbreviation""")
rostered_players = db_cursor.fetchall()
rostered_names = [x[0] for x in rostered_players]
names_to_rostered_players = {x[0]:x for x in rostered_players}

db_cursor.execute("SELECT player_name from player_per_game") 
player_list = list({x[0] for x in db_cursor.fetchall()})
