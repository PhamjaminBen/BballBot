#null round accounts for values that don't appear in the database
def nround(d,p):
  if type(d) not in [float,int]:
    return "Not Tracked"
  else:
    return round(d,p)
