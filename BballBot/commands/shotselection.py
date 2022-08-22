from discord.ext import commands
import discord
from BballBot.assets.dbconnection import db_cursor,player_list
from BballBot.assets.serverlist import sl
import difflib


class ShotSelection(commands.Cog):
  def __init__(self,client) -> None:
    self.client = client

  @commands.slash_command(guild_ids = sl,description = "Shows the shot selection for a certain player during the 2021-2022 season")
  async def shotselection(self,
  ctx:  discord.ApplicationCommand,
  name: discord.Option(str, "Name of the player")
  ) -> None:
    #finding closest match to the player
    results = difflib.get_close_matches(name,player_list)

    #if close match is not found, send error
    if len(results) == 0:
      e = discord.Embed(colour= discord.Colour.orange())
      e.add_field(name = "Error", value = f" **{name}** not found in database")
      await ctx.respond(embed = e)
      return
    
    player = results[0]
    db_cursor.execute(f"SELECT bbref_id FROM player WHERE player_name = \"{player}\";")

    data = db_cursor.fetchall()
    if not data:
      e = discord.Embed(colour= discord.Colour.orange())
      e.add_field(name = "Error", value = f" **{name}** does not have games in the 2021-2022 season")
      await ctx.respond(embed = e)
      return
    
    player_id = data[0][0]


    e = discord.Embed(
      title = f"2021-2022 Shot selection for {player}",
      colour = discord.Colour.orange(),
      url = f"https://www.basketball-reference.com/players/{player_id[0]}/{player_id}/shooting/2022"
    )
    e.set_thumbnail(url = f"https://www.basketball-reference.com/req/202106291/images/players/{player_id}.jpg")

    db_cursor.execute(f"select COUNT(*), SUM(shot_made_flag), shot_zone_basic from player NATURAL JOIN shot_chart_detail WHERE player_name = \"{player}\" GROUP BY shot_zone_basic;")
    data = db_cursor.fetchall()
    e.add_field(name="By Shot Type", value="\n".join([f"**{zone}:** {made}/{amt} fg | {round(made*100/amt,1)}%" for amt,made,zone in data]))

    db_cursor.execute(f"select COUNT(*), SUM(shot_made_flag), shot_zone_range from player NATURAL JOIN shot_chart_detail WHERE player_name = \"{player}\" GROUP BY shot_zone_range;")
    data = db_cursor.fetchall()
    e.add_field(name="By Shot Distance", value="\n".join([f"**{zone}:** {made}/{amt} fg | {round(made*100/amt,1)}%" for amt,made,zone in data]),inline=True)

    await ctx.respond(embed = e)


def setup(client):
  client.add_cog(ShotSelection(client))