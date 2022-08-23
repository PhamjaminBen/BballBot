from BballBot.assets.dbconnection import db_cursor,connection

def add_advanced():
  ids = set()
  while True:
    raw = input()
    if raw == "b":
      break
    raw = raw.split(",")[1:]
    if raw[-1] in ids:
      
      continue
    else:
      ids.add(raw[-1])
    
    formatter(raw)
    raw = ','.join(raw)
    print()
    db_cursor.execute(f"INSERT INTO player_per_game VALUES ({raw},1949)")
    connection.commit()
  
  db_cursor.execute("SELECT * FROM player_per_game limit 20;")
  print(db_cursor.fetchall())

def formatter(data: list):
  for i in range(len(data)):
    try:
      float(data[i])
    except:
      data[i] = "\""+data[i]+"\""

add_advanced()