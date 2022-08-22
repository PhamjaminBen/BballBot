import discord
def format_leaders(emb: discord.Embed, data: list):
  display_text = ""
  for i,(name,ppg) in enumerate(data):
    display_text += f"**{i+1}. {name}:** {round(ppg,1)}\n"
  emb.add_field(name = "Top 20", value = display_text)