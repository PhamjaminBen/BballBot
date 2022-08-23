from sqlite3 import dbapi2
from BballBot.assets.dbconnection import db_cursor,connection

def win_loss_calculation():
  db_cursor.execute("UPDATE team SET w = (SELECT COUNT(*) FROM Game WHERE team_id_winner = team_id);")
  db_cursor.execute("UPDATE team SET l = (SELECT COUNT(*) FROM Game WHERE team_id_loser = team_id);")
  connection.commit()

win_loss_calculation()