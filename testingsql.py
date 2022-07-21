# "C:\Users\Ben\Documents\GitHub\BballBot\nba_sql.db"
from sre_constants import SUCCESS
from basketball_reference_web_scraper import client as bclient
import sqlite3
import difflib
connection = sqlite3.connect('nba_sql.db')
c = connection.cursor()
c.execute("SELECT player_name from player")
players = [x[0] for x in c.fetchall()]

def test():
    c.execute("SELECT city,nickname,w,l from team where conference = \"Western\" order by w desc")
    data = c.fetchall()
    print(data)
    for i,x in enumerate(data):
      print(f"**{i+1}. {x[0]} {x[1]}** Record: **{x[2]}-{x[3]}")


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



if __name__ == "__main__":
  test()