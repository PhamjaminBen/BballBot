import discord
from discord.ext import commands
from BballBot.assets.dbconnection import db_cursor
from BballBot.assets.serverlist import sl
from BballBot.assets.team_aliases import team_aliases

class Roster(commands.Cog):
  def __init__(self, client) -> None:
    self.client = client
  

  @commands.slash_command(guild_ids = sl, description = "Get current roster for a team")
  async def roster(self,
  ctx: discord.ApplicationContext,
  team: discord.Option(str, "Abbreviation, location or name of team: (ex \"SAC\",\"Sacramento\", or \"Kings\")")):
    if team.upper() not in team_aliases:
      await ctx.respond(f"``{team}`` is not a valid abbreviation, location, or team name")
      return
    
    team = team_aliases[team.upper()]
    db_cursor.execute(f"SELECT player_name, jersey, pos,exp from rostered_players where team  = \"{team}\";")

    
    data = db_cursor.fetchall()
    max_len = max([len(x[0]) for x in data])
    text = f"``#  Pos {'Name'.ljust(max_len)} Exp``\n"
    for name,jersey,pos,exp in data:
      text += f" ``{jersey.ljust(2)} {pos.center(3)} {name.ljust(max_len)} {exp.ljust(2)} ``\n"
    print(len(text),text)
    e = discord.Embed(colour= discord.Colour.orange())
    e.add_field(name = f"2022-2023 {team} Roster", value = text)
    await ctx.respond(embed = e)
  
  @commands.command()
  async def roster(self,
  ctx: discord.ApplicationContext,
  team: str):
    if team.upper() not in team_aliases:
      await ctx.send(f"``{team}`` is not a valid abbreviation, location, or team name")
      return
    
    team = team_aliases[team.upper()]
    db_cursor.execute(f"SELECT player_name, jersey, pos,exp from rostered_players where team  = \"{team}\";")

    
    data = db_cursor.fetchall()
    max_len = max([len(x[0]) for x in data])
    text = f"``#  Pos {'Name'.ljust(max_len)} Exp``\n"
    for name,jersey,pos,exp in data:
      text += f" ``{jersey.ljust(2)} {pos.center(3)} {name.ljust(max_len)} {exp.ljust(2)} ``\n"
    print(len(text),text)
    e = discord.Embed(colour= discord.Colour.orange())
    e.add_field(name = f"2022-2023 {team} Roster", value = text)
    await ctx.send(embed = e)

def setup(client):
  client.add_cog(Roster(client))