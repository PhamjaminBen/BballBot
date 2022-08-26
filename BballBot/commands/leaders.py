from discord.ext import commands
from discord.ui import View, Select
import discord
from BballBot.assets.dbconnection import db_cursor
from BballBot.methods.formatleaders import format_leaders
from BballBot.assets.serverlist import sl


class Leaders(commands.Cog):
  def __init__(self,client) -> None:
    self.client = client
  
  @commands.slash_command(guild_ids = sl,description = "Get leaders")
  async def leaders(
    self,
    ctx: discord.ApplicationContext,
    year: discord.Option(int,"Year of the stats", default = 2021)
    ):

    options = [
      discord.SelectOption(label="Points", description="Points", emoji ="💯",default=True),
      discord.SelectOption(label="Rebounds", description="Rebounds", emoji ="🏀"),
      discord.SelectOption(label="Assists", description="Assists", emoji ="🤝"),
      discord.SelectOption(label="Blocks", description="Blocks", emoji = "🛡️"),
      discord.SelectOption(label="Steals", description="Steals", emoji = "💰"),
      discord.SelectOption(label="Minutes", description="Minutes", emoji = "🏃🏼‍♂️")
      # discord.SelectOption(label="Double Doubles", description="Double Doubles", emoji = "2️⃣"),
      # discord.SelectOption(label="Triple Doubles", description="Triple Doubles", emoji = "3️⃣")
    ]
    
    if year < 1949 or year > 2021:
      e = discord.Embed(colour= discord.Colour.orange())
      e.add_field(name = "Error", value = f"No data for the year **{year}-{year+1}**")
      await ctx.respond(embed = e)
      return

    db_cursor.execute(f"SELECT player_name, pts FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY pts DESC LIMIT 20;")
    data = db_cursor.fetchall();
    points_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Points per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(points_embed,data)

    db_cursor.execute(f"SELECT player_name, trb FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY trb DESC LIMIT 20;")
    data = db_cursor.fetchall();
    rebounds_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Rebounds per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(rebounds_embed,data)
    
    db_cursor.execute(f"SELECT player_name, ast FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY ast DESC LIMIT 20;")
    data = db_cursor.fetchall();
    assists_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Assists per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(assists_embed,data)

    db_cursor.execute(f"SELECT player_name, blk FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY blk DESC LIMIT 20;")
    data = db_cursor.fetchall();
    blocks_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Blocks per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(blocks_embed,data)

    db_cursor.execute(f"SELECT player_name, stl FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY stl DESC LIMIT 20;")
    data = db_cursor.fetchall();
    steals_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Steals per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(steals_embed,data)

    db_cursor.execute(f"SELECT player_name, mp FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY mp DESC LIMIT 20;")
    data = db_cursor.fetchall();
    minutes_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Minutes per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(minutes_embed,data)

    # db_cursor.execute("SELECT player_name, dd2 FROM player NATURAL JOIN player_general_traditional_total ORDER BY dd2 DESC LIMIT 20;")
    # data = db_cursor.fetchall();
    # dd2_embed = discord.Embed(
    #   colour = discord.Colour.orange(),
    #   title = f"Double Double leaders for the {year}-{year+1} Season",
    #   url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
    #   )
    # format_leaders(dd2_embed,data)

    # db_cursor.execute("SELECT player_name, td3 FROM player NATURAL JOIN player_general_traditional_total ORDER BY td3 DESC LIMIT 20;")
    # data = db_cursor.fetchall();
    # td3_embed = discord.Embed(
    #   colour = discord.Colour.orange(),
    #   title = f"Triple Double leaders for the {year-1}-{year} Season",
    #   url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
    #   )
    # format_leaders(td3_embed,data)
    
    
    async def callback(interaction: discord.Interaction):
      selected = select.values[0]
      if selected == "Points":
        await interaction.message.edit(embed = points_embed)
      elif selected == "Rebounds":
        await interaction.message.edit(embed = rebounds_embed)
      elif selected == "Assists":
        await interaction.message.edit(embed = assists_embed)
      elif selected == "Blocks":
        await interaction.message.edit(embed = blocks_embed)
      elif selected == "Steals":
        await interaction.message.edit(embed = steals_embed)
      elif selected == "Minutes":
        await interaction.message.edit(embed = minutes_embed)
      # elif selected == "Double Doubles":
      #   await interaction.message.edit(embed = dd2_embed)
      # elif selected == "Triple Doubles":
      #   await interaction.message.edit(embed = td3_embed)

    
    select = Select(options = options)
    select.callback = callback
    view = View()
    view.add_item(select)
    await ctx.respond(embed = points_embed, view = view)


  @commands.command()
  async def leaders(
    self,
    ctx: discord.ApplicationContext,
    year: str
    ):
    options = [
      discord.SelectOption(label="Points", description="Points", emoji ="💯",default=True),
      discord.SelectOption(label="Rebounds", description="Rebounds", emoji ="🏀"),
      discord.SelectOption(label="Assists", description="Assists", emoji ="🤝"),
      discord.SelectOption(label="Blocks", description="Blocks", emoji = "🛡️"),
      discord.SelectOption(label="Steals", description="Steals", emoji = "💰"),
      discord.SelectOption(label="Minutes", description="Minutes", emoji = "🏃🏼‍♂️")
      # discord.SelectOption(label="Double Doubles", description="Double Doubles", emoji = "2️⃣"),
      # discord.SelectOption(label="Triple Doubles", description="Triple Doubles", emoji = "3️⃣")
    ]

    if not year.isdigit():
      await ctx.send(f"``{year}`` is not a valid year")
      return
    
    year = int(year)

    if year < 1949 or year > 2021:
      ctx.send(f"Leaders not tracked for year ``{year}``")
      return

    db_cursor.execute(f"SELECT player_name, pts FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY pts DESC LIMIT 20;")
    data = db_cursor.fetchall();
    points_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Points per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(points_embed,data)

    db_cursor.execute(f"SELECT player_name, trb FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY trb DESC LIMIT 20;")
    data = db_cursor.fetchall();
    rebounds_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Rebounds per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(rebounds_embed,data)
    
    db_cursor.execute(f"SELECT player_name, ast FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY ast DESC LIMIT 20;")
    data = db_cursor.fetchall();
    assists_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Assists per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(assists_embed,data)

    db_cursor.execute(f"SELECT player_name, blk FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY blk DESC LIMIT 20;")
    data = db_cursor.fetchall();
    blocks_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Blocks per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(blocks_embed,data)

    db_cursor.execute(f"SELECT player_name, stl FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY stl DESC LIMIT 20;")
    data = db_cursor.fetchall();
    steals_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Steals per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(steals_embed,data)

    db_cursor.execute(f"SELECT player_name, mp FROM player_per_game WHERE g >= 58 AND year = {year} ORDER BY mp DESC LIMIT 20;")
    data = db_cursor.fetchall();
    minutes_embed = discord.Embed(
      colour = discord.Colour.orange(),
      title = f"Minutes per game leaders for the {year}-{year+1} Season",
      url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
      )
    format_leaders(minutes_embed,data)

    # db_cursor.execute("SELECT player_name, dd2 FROM player NATURAL JOIN player_general_traditional_total ORDER BY dd2 DESC LIMIT 20;")
    # data = db_cursor.fetchall();
    # dd2_embed = discord.Embed(
    #   colour = discord.Colour.orange(),
    #   title = f"Double Double leaders for the {year}-{year+1} Season",
    #   url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
    #   )
    # format_leaders(dd2_embed,data)

    # db_cursor.execute("SELECT player_name, td3 FROM player NATURAL JOIN player_general_traditional_total ORDER BY td3 DESC LIMIT 20;")
    # data = db_cursor.fetchall();
    # td3_embed = discord.Embed(
    #   colour = discord.Colour.orange(),
    #   title = f"Triple Double leaders for the {year-1}-{year} Season",
    #   url   = f"https://www.basketball-reference.com/leagues/NBA_{year+1}_per_game.html"
    #   )
    # format_leaders(td3_embed,data)
    
    
    async def callback(interaction: discord.Interaction):
      selected = select.values[0]
      if selected == "Points":
        await interaction.message.edit(embed = points_embed)
      elif selected == "Rebounds":
        await interaction.message.edit(embed = rebounds_embed)
      elif selected == "Assists":
        await interaction.message.edit(embed = assists_embed)
      elif selected == "Blocks":
        await interaction.message.edit(embed = blocks_embed)
      elif selected == "Steals":
        await interaction.message.edit(embed = steals_embed)
      elif selected == "Minutes":
        await interaction.message.edit(embed = minutes_embed)
      # elif selected == "Double Doubles":
      #   await interaction.message.edit(embed = dd2_embed)
      # elif selected == "Triple Doubles":
      #   await interaction.message.edit(embed = td3_embed)

    
    select = Select(options = options)
    select.callback = callback
    view = View()
    view.add_item(select)
    await ctx.send(embed = points_embed, view = view)


def setup(client):
  client.add_cog(Leaders(client))