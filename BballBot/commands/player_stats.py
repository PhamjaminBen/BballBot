from discord.ext import commands
from discord.ui import View,Button
import discord
import difflib
from BballBot.assets.dbconnection import db_cursor
from BballBot.assets.player_lists import player_list
from BballBot.assets.serverlist import sl
from BballBot.methods.nround import nround

class PlayerStats(commands.Cog):
  def __init__(self, client):
    self.client = client

  
  @commands.slash_command(guild_ids = sl,description = "Shows the stats for a certain player and year")
  async def stats(
    self,
    ctx: discord.ApplicationContext,
    name: discord.Option(str,"Name of player"),
    year: discord.Option(int,"Start year of the season", default = 2021)
    ):
      #finding closest match to the player
      results = difflib.get_close_matches(name,player_list)

      #if close match is not found, send error
      if len(results) == 0:
        e = discord.Embed(colour= discord.Colour.orange())
        e.add_field(name = "Error", value = f" **{name}** not found in database")
        await ctx.respond(embed = e)
        return
      
      #getting info for stats
      name = results[0]
      db_cursor.execute(f"""SELECT id,player_name,pts,ast,trb,stl,blk,tov, fgp,fg3p,ftp,g
      FROM player_per_game
      WHERE player_name = \"{name}\" and year = {year};""")
      data = db_cursor.fetchall()

      #if no data is found four that year, send error
      if len(data) == 0:
        e = discord.Embed(colour= discord.Colour.orange())
        e.add_field(name = "Error", value = f" **{name}** does not have data for the year **{year}-{year+1}**")
        await ctx.respond(embed = e)
        return
      
      #parsing data and cleaning it up for display
      data = data[0]
      regular_embed = discord.Embed(
        title=f"{name} Stats",
        colour = discord.Colour.orange(),
        url = f"https://www.basketball-reference.com/players/{data[0][0]}/{data[0]}.html")
      regular_embed.set_thumbnail(url = f"https://www.basketball-reference.com/req/202106291/images/players/{data[0]}.jpg")
      regular_embed.set_footer(text = "Source: basketball-reference.com")
      regular_embed.add_field(name = f"{year}-{year+1} Stats",
      value = f"""`GP  | {data[11]}`
        `Ppg | {nround(data[2],1)}`
        `Apg | {nround(data[3],1)}`
        `Rpg | {nround(data[4],1)}`
        `Spg | {nround(data[5],1)}`
        `Bpg | {nround(data[6],1)}`
        `TOpg| {nround(data[7],1)}`
        `FG  | {nround(data[8]*100,1)}%`
        `3P  | {nround(data[9]*100,1)}%`
        `FT  | {nround(data[10]*100,1)}%`""")
      await ctx.respond(embed=regular_embed)
  

  @commands.slash_command(guild_ids = sl,description = "Shows the stats for a certain player's career'")
  async def cstats(self,
  ctx: discord.ApplicationContext,
  name: discord.Option(str,"Name of player")
  ):
    #finding closest match to the player
    results = difflib.get_close_matches(name,player_list)

    #if close match is not found, send error
    if len(results) == 0:
      e = discord.Embed(colour= discord.Colour.orange())
      e.add_field(name = "Error", value = f" **{name}** not found in database")
      await ctx.respond(embed = e)
      return

    #getting info for stats
    name = results[0]
    db_cursor.execute(f"""SELECT id,player_name,pts_per_g,ast_per_g,trb_per_g,stl_per_g,blk_per_g,
    tov_per_g,fg_pct,fg3_pct,ft_pct,g
    FROM player_career_per_game NATURAL JOIN players
    WHERE player_name = \"{name}\"""")
    data = db_cursor.fetchall()

    data = data[0]
    regular_embed = discord.Embed(
      title=f"{name} Career",
      colour = discord.Colour.orange(),
      url = f"https://www.basketball-reference.com/players/{data[0][0]}/{data[0]}.html")
    regular_embed.set_thumbnail(url = f"https://www.basketball-reference.com/req/202106291/images/players/{data[0]}.jpg")
    regular_embed.set_footer(text = "Source: basketball-reference.com")
    regular_embed.add_field(name = f"Career Averages",
    value = f"""`GP  | {data[11]}`
        `Ppg | {nround(data[2],1)}`
        `Apg | {nround(data[3],1)}`
        `Rpg | {nround(data[4],1)}`
        `Spg | {nround(data[5],1)}`
        `Bpg | {nround(data[6],1)}`
        `TOpg| {nround(data[7],1)}`
        `FG  | {nround(data[8]*100,1)}%`
        `3P  | {nround(data[9]*100,1)}%`
        `FT  | {nround(data[10]*100,1)}%`""")

    await ctx.respond(embed=regular_embed)
  

  @commands.command()
  async def cstats(self,
  ctx: discord.ApplicationContext,
  *name: tuple
  ):
    name = " ".join(["".join(word) for word in name])
    #finding closest match to the player
    results = difflib.get_close_matches(name,player_list)

    #if close match is not found, send error
    if len(results) == 0:
      e = discord.Embed(colour= discord.Colour.orange())
      e.add_field(name = "Error", value = f" **{name}** not found in database")
      await ctx.send(embed = e)
      return

    #getting info for stats
    name = results[0]
    db_cursor.execute(f"""SELECT id,player_name,pts_per_g,ast_per_g,trb_per_g,stl_per_g,blk_per_g,
    tov_per_g,fg_pct,fg3_pct,ft_pct,g
    FROM player_career_per_game NATURAL JOIN players
    WHERE player_name = \"{name}\"""")
    data = db_cursor.fetchall()

    data = data[0]
    regular_embed = discord.Embed(
      title=f"{name} Career",
      colour = discord.Colour.orange(),
      url = f"https://www.basketball-reference.com/players/{data[0][0]}/{data[0]}.html")
    regular_embed.set_thumbnail(url = f"https://www.basketball-reference.com/req/202106291/images/players/{data[0]}.jpg")
    regular_embed.set_footer(text = "Source: basketball-reference.com")
    regular_embed.add_field(name = f"Career Averages",
    value = f"""`GP  | {data[11]}`
        `Ppg | {nround(data[2],1)}`
        `Apg | {nround(data[3],1)}`
        `Rpg | {nround(data[4],1)}`
        `Spg | {nround(data[5],1)}`
        `Bpg | {nround(data[6],1)}`
        `TOpg| {nround(data[7],1)}`
        `FG  | {nround(data[8]*100,1)}%`
        `3P  | {nround(data[9]*100,1)}%`
        `FT  | {nround(data[10]*100,1)}%`""")

    await ctx.send(embed=regular_embed)


def setup(client):
    client.add_cog(PlayerStats(client))