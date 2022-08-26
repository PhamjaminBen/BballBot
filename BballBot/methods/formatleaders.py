import discord
def format_leaders(emb: discord.Embed, data: list):
  display_text = ""
  for i,(name,stat) in enumerate(data):
    if stat == "":
      emb.add_field(name = "Error", value = "Stat not tracked")
      return 
    display_text += f"``{str(i+1).zfill(2)}. {name.ljust(24)}: {round(float(stat),1)}``\n"
  
  if display_text == "":
    display_text = "Not tracked"
  emb.add_field(name = "Top 20", value = display_text)