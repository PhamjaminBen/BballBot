from ctypes import Union
import logging
from multiprocessing.sharedctypes import Value
import os
from re import L
import discord
# from keep_alive import keep_alive
# import nba_api
import requests
# from nba_api.stats.static import players
# from nba_api.stats.endpoints import commonplayerinfo
from discord.ui import View, Button
from discord.ext import commands
# import logging
# import requests
import time
from basketball_reference_web_scraper import client as bclient
# from basketball_reference_web_scraper.data import OutputType
import basketball_reference_web_scraper
from data_processing import stdict, calculate_stats, astdict
from bs4 import BeautifulSoup
import requests
import random
from dataclasses import dataclass
import sqlite3
import difflib

# HEADERS = headers = {
#             'x-rapidapi-host': "nba-stats4.p.rapidapi.com",
#             'x-rapidapi-key': "3a84732a7fmsh09a7778c123c61ap145571jsn4e31058e61d1"
#             }

sl = ["704377057529954397","732794738318639125","690009077694332973"]
logging.basicConfig(level=logging.INFO)

token = ''

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="-", intents = intents)

#accesing the db
connection = sqlite3.connect('nba_sql.db')
db_cursor = connection.cursor()
db_cursor.execute("SELECT player_name from player_per_game")
players = list({x[0] for x in db_cursor.fetchall()})

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "Westbrick construction simulator", type = "playing"))
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(m: discord.Message):
    if "lebron" in m.content.lower() and m.author.discriminator != "8178":
        await m.channel.send(m.content.replace("lebron","LeBum").replace("LeBron","LeBum").replace("Lebron","LeBum"))
    if "zion" in m.content.lower() and m.author.discriminator != "8178":
        await m.channel.send(m.content.replace("zion","ZiObese").replace("Zion","ZiObese"))
    if "curry" in m.content.lower() and m.author.discriminator != "8178":
        await m.channel.send(m.content.replace("Curry","CurFraud").replace("curry","CurFraud"))
    if "jokic" in m.content.lower() and m.author.discriminator != "8178":
        await m.channel.send("If you didn't know, he grew up in a serbian warzone, and his two brothers are buff and can beat you up!")


# @client.message_command(brief = "Gets the information of an active NBA player. Other aliases: \'ap\'", aliases = ['ap'])
# async def activeplayer(ctx,*name,year = 2022):
#     results = bclient.search(term = " ".join(name))
#     if len(results['players']) == 0:
#         await ctx.respond(f" **{' '.join(name)}** not found in basketball reference database")
#         return
#     if results['players'][0]['name'].lower() not in stdict[year].keys():
#         await ctx.respond(f" **{results['players'][0]['name']}** has no games played in the current nba season.")
#         return
#     player = stdict[year][results['players'][0]['name'].lower()]
#     await ctx.respond("**{}** is currently playing for the **{}** at the **{}** position.".format(player['name'],player['team'].name.replace("_"," ").title(),player['positions'][0].name.replace("_"," ").lower())) 


# @client.command(brief = "Gets career stats for a player")
# async def cstats(ctx,*name):
#     results = bclient.search(term = " ".join(name))
#     if len(results['players']) == 0:
#         await ctx.send(f" **{' '.join(name)}** not found in basketball reference database")
#         return
#     if results['players'][0]['name'].lower() not in stdict.keys():
#         await ctx.send(f" **{results['players'][0]['name']}** has no games played in the current nba season.")
#         return
#     url = "https://nba-stats4.p.rapidapi.com/players/"
#     querystring = {"page":"1","full_name":results['players'][0]['name'],"per_page":"50"}
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     if len(response.json()) == 0:
#         await ctx.send(f"Player **{' '.join(name)}** not found.")
#         return
#     await ctx.send(f"Getting career stats for {' '.join(name)}...")
#     time.sleep(1)
#     url = f"https://nba-stats4.p.rapidapi.com/per_game_career_regular_season/{response.json()[0]['id']}"
#     response = requests.request("GET", url, headers=HEADERS)
#     stats = response.json()
#     await ctx.send("In **{}** regular season games, **{}** has averages of **{}** Ppg, **{}** Apg, and **{}** Rpg".format(stats['gp'],results['players'][0]['name'],stats['pts_per_game'],stats['ast_per_game'],stats['reb_per_game']))


@client.slash_command(guild_ids = sl,description = "Shows the stats for a certain player and year")
async def stats2(
  ctx: discord.ApplicationContext,
  name: discord.Option(str,"Name of player"),
  year: discord.Option(int,"Start year of the season", default = 2021)
  ):
    #finding closest match to the player
    results = difflib.get_close_matches(name,players)

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
      title=f"Stats for {name}",
      colour = discord.Colour.orange(),
      url = f"https://www.basketball-reference.com/players/{data[0][0]}/{data[0]}.html")
    regular_embed.set_thumbnail(url = f"https://www.basketball-reference.com/req/202106291/images/players/{data[0]}.jpg")
    regular_embed.set_footer(text = "Stats provided by basketball-reference.com", icon_url = "https://d2p3bygnnzw9w3.cloudfront.net/req/202201141/logos/bbr-logo.svg")
    regular_embed.add_field(name = f"{year}-{year+1} Stats",
    value = f"Games Played: **{data[11]}**\nPpg: **{nround(data[2],1)}**\nApg: **{nround(data[3],1)}**\nRpg: **{nround(data[4],1)}**\nSpg: **{nround(data[5],1)}**\nBpg: **{nround(data[6],1)}**\nTOpg: **{nround(data[7],1)}**\nFG: **{nround(data[8]*100,1)}%**\n3P: **{nround(data[9]*100,1)}%**\nFT: **{nround(data[10]*100,1)}%**")
    await ctx.respond(embed=regular_embed)

    
@client.slash_command(guild_ids = sl,description = "Shows the stats for a certain player's career'")
async def cstats(
  ctx: discord.ApplicationContext,
  name: discord.Option(str,"Name of player")
  ):
    #finding closest match to the player
    results = difflib.get_close_matches(name,players)

    #if close match is not found, send error
    if len(results) == 0:
      e = discord.Embed(colour= discord.Colour.orange())
      e.add_field(name = "Error", value = f" **{name}** not found in database")
      await ctx.respond(embed = e)
      return

    #getting info for stats
    name = results[0]
    db_cursor.execute(f"""SELECT id,player_name,g,pts_per_g,ast_per_g,trb_per_g,stl_per_g,blk_per_g,
    tov_per_g,fg_pct,fg3_pct,ft_pct
    FROM player_career_per_game NATURAL JOIN players
    WHERE player_name = \"{name}\"""")
    data = db_cursor.fetchall()

    data = data[0]
    regular_embed = discord.Embed(
      title=f"Career stats for {name}",
      colour = discord.Colour.orange(),
      url = f"https://www.basketball-reference.com/players/{data[0][0]}/{data[0]}.html")
    regular_embed.set_thumbnail(url = f"https://www.basketball-reference.com/req/202106291/images/players/{data[0]}.jpg")
    regular_embed.set_footer(text = "Stats provided by basketball-reference.com", icon_url = "https://d2p3bygnnzw9w3.cloudfront.net/req/202201141/logos/bbr-logo.svg")
    regular_embed.add_field(name = f"Career Averages",
    value = f"Games Played: **{data[2]}**\nPpg: **{nround(data[3],1)}**\nApg: **{nround(data[4],1)}**\nRpg: **{nround(data[5],1)}**\nSpg: **{nround(data[6],1)}**\nBpg: **{nround(data[7],1)}**\nTOpg: **{nround(data[8],1)}**\nFG: **{nround(data[9]*100,1)}%**\n3P: **{nround(data[10]*100,1)}%**\nFT: **{nround(data[11]*100,1)}%**")
    await ctx.respond(embed=regular_embed)

#null round accounts for values that don't appear in the database
def nround(d,p):
  if type(d) not in [float,int]:
    return "Not Tracked"
  else:
    return round(d,p)

@client.slash_command(guild_ids = sl,description = "Shows the stats for a certain player and year")
async def stats(
  ctx:  discord.ApplicationContext,
  name: discord.Option(str, "Name of the player")
  ):
    year = 2022
    results = bclient.search(term = name)
    if len(results['players']) == 0:
        e = discord.Embed(colour= discord.Colour.orange())
        e.add_field(name = "Error", value = f" **{name}** not found in basketball reference database")
        await ctx.respond(embed = e)
        return
    if results['players'][0]['name'].lower() not in stdict[year].keys():
        e = discord.Embed()
        e.add_field(name = "Error", value = f" **{results['players'][0]['name']}** has no games played in the {year-1}-{year} nba season.")
        e.color = discord.Colour.orange()
        await ctx.respond(embed = e)
        return
    
    #getting info for normal stats
    player = stdict[year][results['players'][0]['name'].lower()]
    stats = calculate_stats(player)
    regular_embed = discord.Embed(title=f"Stats for {player['name']}")
    regular_embed.colour = discord.Colour.orange()
    regular_embed.url = f"https://www.basketball-reference.com/players/{player['slug'][0]}/{player['slug']}.html"
    player_pic = BeautifulSoup(requests.get(regular_embed.url).content,'html5lib').findAll('img')[1]['src']
    regular_embed.set_thumbnail(url=player_pic)
    print(player_pic[:-3])
    regular_embed.add_field(name = f"{year-1}-{year} Stats",
    value = "Games Played: **{}**\nPpg: **{}**\nApg: **{}**\nRpg: **{}**\nSpg: **{}**\nBpg: **{}**\nTOpg: **{}**\nFpg: **{}**\nFG: **{}%**\n3P: **{}%**\nFT: **{}%**".format(player['games_played'],stats['ppg'],stats['apg'],stats['rpg'],stats['spg'],stats['bpg'],stats['topg'],stats['fpg'],stats['fgp'],stats['3pp'],stats['ftp']),inline= False)
    regular_embed.set_footer(text = "Stats provided by basketball-reference.com", icon_url = "https://d2p3bygnnzw9w3.cloudfront.net/req/202201141/logos/bbr-logo.svg")

    #getting info for advanced stats
    player1 = astdict[year][results['players'][0]['name'].lower()]
    advanced_embed = discord.Embed(title=f"Advanced Stats for {player1['name']}")
    advanced_embed.colour = discord.Colour.orange()
    advanced_embed.url = f"https://www.basketball-reference.com/players/{player1['slug'][0]}/{player1['slug']}.html"
    advanced_embed.set_thumbnail(url=player_pic)
    advanced_embed.set_footer(text = "Stats provided by basketball-reference.com", icon_url = "https://d2p3bygnnzw9w3.cloudfront.net/req/202201141/logos/bbr-logo.svg")
    advanced_embed.add_field(name = "2021-2022 Stats",
    value = "\n".join([f"{k.replace('_',' ')}: **{v}**" for k,v in player1.items()][5:]))

    #initializing buttons
    button1 = Button(label = "Regular", style = discord.ButtonStyle.blurple)
    button2 = Button(label = "Advanced", style = discord.ButtonStyle.gray)

    async def regular_callback(interaction: discord.Interaction):
        await interaction.message.edit(embed = regular_embed)
    async def advanced_callback(interaction: discord.Interaction):
        await interaction.message.edit(embed = advanced_embed)
    
    button1.callback = regular_callback
    button2.callback = advanced_callback
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    await ctx.respond(embed=regular_embed, view = view)



@client.slash_command(guild_ids = sl,description = "Shows the mugshot for a certain player")
async def mugshot(
  ctx:  discord.ApplicationCommand,
  name: discord.Option(str, "Name of the player")
  ):
  results = bclient.search(term = name)
  if len(results['players']) == 0:
      e = discord.Embed()
      e.add_field(name = "Error", value = f" **{name}** not found in basketball reference database")
      e.color = discord.Colour.orange()
      await ctx.respond(embed = e)
      return
  
  player = results['players'][0]
  e = discord.Embed()
  e.title = f"Mugshot for {player['name']}"
  e.colour = discord.Colour.orange()
  e.url = f"https://www.basketball-reference.com/players/{player['identifier'][0]}/{player['identifier']}.html"
  e.set_image(url = BeautifulSoup(requests.get(e.url).content,'html5lib').findAll('img')[1]['src'])
  await ctx.respond(embed = e)

# @client.slash_command(guild_ids = sl,description = "Displays standings for a certain year")
# async def standings(
#   ctx:  discord.ApplicationContext,
#   year: discord.Option(int,"Year of the standings",default = 2022)
#   ):
#   try:
#       year = int(year)
#       standings_ = bclient.standings(season_end_year = year)
#       e = ''

#       for i,team in enumerate(sorted(standings_[:15], key = lambda x: (x['wins'],-x['losses']), reverse = True)):
#           e += f"**{i+1}. {team['team'].name.replace('_',' ').title()}** Record: **{team['wins']}-{team['losses']}**\n"

#       w = ""
#       for i,team in  enumerate(sorted(standings_[15:], key = lambda x: (x['wins'],-x['losses']), reverse = True)):
#           w += f"**{i+1}. {team['team'].name.replace('_',' ').title()}** Record: **{team['wins']}-{team['losses']}**\n"

#       eastern = discord.Embed(title = f'Standings for the **{year-1}-{year}** NBA Season')
#       eastern.add_field(name = "Eastern Conference", value = e)
#       eastern.colour = discord.Colour.orange()
#       eastern.url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

#       western = discord.Embed(title = f'Standings for the **{year-1}-{year}** NBA Season')
#       western.add_field(name = "Western Conference", value = w)
#       western.colour = discord.Colour.orange()
#       western.url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

#       #initializing buttons
#       button1 = Button(label = "Eastern", style = discord.ButtonStyle.blurple)
#       button2 = Button(label = "Western", style = discord.ButtonStyle.gray)

#       async def regular_callback(interaction: discord.Interaction):
#           await interaction.message.edit(embed = eastern)
#       async def advanced_callback(interaction: discord.Interaction):
#           await interaction.message.edit(embed = western)
      
#       button1.callback = regular_callback
#       button2.callback = advanced_callback
#       view = View()
#       view.add_item(button1)
#       view.add_item(button2)
#       await ctx.respond(embed = eastern, view = view)
#   except IndexError:
#       await ctx.respond("Standings for season not available")
#   except ValueError:
#       await ctx.respond("Standings for season not available")
#   except basketball_reference_web_scraper.errors.InvalidSeason:
#       await ctx.respond("Standings for season not available")

@client.slash_command(guild_ids = sl,description = "Displays standings for a certain year")
async def standings2(ctx:  discord.ApplicationContext):
    db_cursor.execute("SELECT city,nickname,w,l from team where conference = \"Eastern\" order by w desc")
    east_text = ""
    for i,x in enumerate(db_cursor.fetchall()):
      east_text += f"**{i+1}. {x[0]} {x[1]}** Record: **{x[2]}-{x[3]}**\n"

    db_cursor.execute("SELECT city,nickname,w,l from team where conference = \"Western\" order by w desc")
    west_text = ""
    for i,x in enumerate(db_cursor.fetchall()):
      west_text += f"**{i+1}. {x[0]} {x[1]}** Record: **{x[2]}-{x[3]}**\n"

    east_embed = discord.Embed(
      title = f"Standings for the **2021-2022** NBA Season",
      color = discord.Colour.orange(),
      url = "https://www.basketball-reference.com/leagues/NBA_2021_standings.html" )
    east_embed.add_field(name = "Eastern Conference", value = east_text)

    west_embed = discord.Embed(
      title = f"Standings for the **2021-2022** NBA Season",
      color = discord.Colour.orange(),
      url = "https://www.basketball-reference.com/leagues/NBA_2021_standings.html" )
    west_embed.add_field(name = "Western Conference", value = west_text)

    
    #initializing buttons
    button1 = Button(label = "Eastern", style = discord.ButtonStyle.blurple)
    button2 = Button(label = "Western", style = discord.ButtonStyle.gray)

    async def east_callback(interaction: discord.Interaction):
        await interaction.message.edit(embed = east_embed)
    async def west_callback(interaction: discord.Interaction):
        await interaction.message.edit(embed = west_embed)
    
    button1.callback = east_callback
    button2.callback = west_callback
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    await ctx.respond(embed = east_embed, view = view)

# @client.slash_command(guild_ids = sl,description = "Search for a player")
# async def search(
#   ctx:  discord.ApplicationContext,
#   name: discord.Option(str, "Name of the player")
#   ):
#     year = 2022
#     results = bclient.search(term = name)
#     print(results)
#     if len(results['players']) == 0:
#         await ctx.respond(f" **{name}** not found in basketball reference database")
#         return
#     player = results['players'][0]
#     thing = discord.Embed()
#     thing.title = player['name']
#     thing.colour = discord.Colour.orange()
#     thing.set_footer(text = "curfraud needs to retire and become a family man")
#     thing.url = f"https://www.basketball-reference.com/players/{player['identifier'][0]}/{player['identifier']}.html"
#     thing.set_image(url = BeautifulSoup(requests.get(thing.url).content,'html5lib').findAll('img')[1]['src'])

#     if results['players'][0]['name'].lower() in stdict[year].keys():
#         player = stdict[year][results['players'][0]['name'].lower()]
#         thing.add_field(name = "Currently Active",
#          value = "**{}** is currently playing for the **{}** at the **{}** position.".format(player['name'],player['team'].name.replace("_"," ").title(),player['positions'][0].name.replace("_"," ").lower())) 
    
#     await ctx.respond(embed = thing)

@client.slash_command(guild_ids = sl,description = "Get leaders")
async def leaders(
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
  
  if year < 2000 or year > 2021:
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

  
  select = discord.ui.Select(options = options)
  select.callback = callback
  view = discord.ui.View()
  view.add_item(select)
  await ctx.respond(embed = points_embed, view = view)

  
def format_leaders(emb: discord.Embed, data: list):
  display_text = ""
  for i,(name,ppg) in enumerate(data):
    display_text += f"**{i+1}. {name}:** {round(ppg,1)}\n"
  emb.add_field(name = "Top 20", value = display_text)

@client.slash_command(guild_ids = sl,description = "Play poeltl")
async def poeltl(ctx: discord.ApplicationContext):
  player = random.choice(list(stdict[2022].items()))
  print(player)
  await ctx.respond(f"You guessed the poeltl: {player[0]} in 1 try: {ctx.author.name}")

@dataclass
class Player:
  name:       str
  team:       str
  conference: str
  division:   str
  position:   str
  height:     int
  age:        int
  number:     int

@client.message_command(guild_ids = ["704377057529954397"])
async def test(ctx,message):
  await ctx.send("eughh")

client.run(token)