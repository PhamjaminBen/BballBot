from BballBot.assets.dbconnection import db_cursor

def per_game_calculation():
  db_cursor.execute("""
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

per_game_calculation()