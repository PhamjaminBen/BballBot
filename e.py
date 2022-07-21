# "C:\Users\Ben\Documents\GitHub\BballBot\nba_sql.db"
import sqlite3

connection = sqlite3.connect('nba_sql.db')

cursor = connection.cursor()

cursor.execute("select * from player limit 10")

results = cursor.fetchall()
print(results)
cursor.execute("select * from team")
print()
results = cursor.fetchall()
print(results)