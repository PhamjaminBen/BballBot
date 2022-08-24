import sqlite3

#accesing the db
connection = sqlite3.connect('BballBot/nba_sql.db')
db_cursor = connection.cursor()