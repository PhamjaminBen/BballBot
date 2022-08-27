import discord
from discord.ext import commands
from BballBot.assets.dbconnection import db_cursor
from BballBot.assets.teams.aliases import team_aliases
from BballBot.assets.teams.colors import team_colors
from BballBot.assets.teams.logos import team_logos

class Roster(commands.Cog):
  def __init__(self, client) -> None:
    self.client = client
  
  
  @commands.command()
  async def roster(self,
  ctx: discord.ApplicationContext,
  team: str):
    if team.upper() not in team_aliases:
      await ctx.send(f"`{team}` is not a valid abbreviation, location, or team name")
      return
    
    team = team_aliases[team.upper()]
    db_cursor.execute(f"SELECT player_name, jersey, pos,exp from rostered_players where team  = \"{team}\";")

    
    data = db_cursor.fetchall()
    max_len = max([len(x[0]) for x in data])
    text = f"`#  Pos {'Name'.ljust(max_len)}`\n"
    for name,jersey,pos,exp in data:
      text += f" `{jersey.ljust(2)} {pos.center(3)} {name.ljust(max_len)}`\n"
    e = discord.Embed(color= discord.Colour.from_rgb(*team_colors[team]),)\
      .add_field(name = f"2022-2023 {team} Roster", value = text)\
      .set_thumbnail(url = team_logos[team])
    await ctx.send(embed = e)

def setup(client):
  client.add_cog(Roster(client))