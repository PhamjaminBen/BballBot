from dataclasses import dataclass

@dataclass
class Player:
  name:       str
  conference: str
  division:   str
  position:   str
  height:     int
  age:        int
  number:     int

sc30 = Player("Steph","Western","Pacific","PG",75,33,30)
print(sc30.conference)
