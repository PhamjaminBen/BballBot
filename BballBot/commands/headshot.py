from discord.ext import commands
import discord
from BballBot.assets.serverlist import sl
from BballBot.assets.dbconnection import player_list, db_cursor
import difflib


class Headshot(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.slash_command(guild_ids = sl,description = "Shows the mugshot for a certain player")
  async def headshot(self,
  ctx:  discord.ApplicationCommand,
  name: discord.Option(str, "Name of the player")
  ):
  #finding closest match to the player
    results = difflib.get_close_matches(name,player_list)

    #if close match is not found, send error
    if len(results) == 0:
      e = discord.Embed(colour= discord.Colour.orange())
      e.add_field(name = "Error", value = f" **{name}** not found in database")
      await ctx.respond(embed = e)
      return
    
    player = results[0]
    db_cursor.execute(f"SELECT id FROM players WHERE player_name = \"{player}\";")
    e = discord.Embed(
      title = f"Headshot for {player}",
      colour = discord.Colour.orange())
    e.set_image(url = f"https://www.basketball-reference.com/req/202106291/images/players/{db_cursor.fetchall()[0][0]}.jpg")
    await ctx.respond(embed = e)

def setup(client):
  client.add_cog(Headshot(client))