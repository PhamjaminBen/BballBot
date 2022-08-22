import sqlite3

#accesing the db
connection = sqlite3.connect('BballBot/nba_sql.db')
db_cursor = connection.cursor()
db_cursor.execute("SELECT player_name from player_per_game")
player_list = list({x[0] for x in db_cursor.fetchall()})