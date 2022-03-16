import logging
from multiprocessing.sharedctypes import Value
import os
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

# HEADERS = headers = {
#             'x-rapidapi-host': "nba-stats4.p.rapidapi.com",
#             'x-rapidapi-key': "3a84732a7fmsh09a7778c123c61ap145571jsn4e31058e61d1"
#             }

sl = ["704377057529954397","949595930523471942","732794738318639125"]
logging.basicConfig(level=logging.INFO)

token = 'OTM2Njg5NTEyNzExNTk4MTIx.YfQ2Fg.og_mynJAYsMTf8xAZQhhIv1zW6w'

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="-", intents = intents)

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
async def stats(
  ctx:  discord.ApplicationContext,
  name: discord.Option(str, "Name of the player")
  ):
    year = 2022
    results = bclient.search(term = name)
    if len(results['players']) == 0:
        e = discord.Embed()
        e.add_field(name = "Error", value = f" **{name}** not found in basketball reference database")
        e.color = discord.Colour.orange()
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

@client.slash_command(guild_ids = sl,description = "Displays standings for a certain year")
async def standings(
  ctx:  discord.ApplicationContext,
  year: discord.Option(int,"Year of the standings",default = 2022)
  ):
  try:
      year = int(year)
      standings_ = bclient.standings(season_end_year = year)
      e = ''

      for i,team in enumerate(sorted(standings_[:15], key = lambda x: (x['wins'],-x['losses']), reverse = True)):
          e += f"**{i+1}. {team['team'].name.replace('_',' ').title()}** Record: **{team['wins']}-{team['losses']}**\n"

      w = ""
      for i,team in  enumerate(sorted(standings_[15:], key = lambda x: (x['wins'],-x['losses']), reverse = True)):
          w += f"**{i+1}. {team['team'].name.replace('_',' ').title()}** Record: **{team['wins']}-{team['losses']}**\n"

      eastern = discord.Embed(title = f'Standings for the **{year-1}-{year}** NBA Season')
      eastern.add_field(name = "Eastern Conference", value = e)
      eastern.colour = discord.Colour.orange()
      eastern.url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

      western = discord.Embed(title = f'Standings for the **{year-1}-{year}** NBA Season')
      western.add_field(name = "Western Conference", value = w)
      western.colour = discord.Colour.orange()
      western.url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

      #initializing buttons
      button1 = Button(label = "Eastern", style = discord.ButtonStyle.blurple)
      button2 = Button(label = "Western", style = discord.ButtonStyle.gray)

      async def regular_callback(interaction: discord.Interaction):
          await interaction.message.edit(embed = eastern)
      async def advanced_callback(interaction: discord.Interaction):
          await interaction.message.edit(embed = western)
      
      button1.callback = regular_callback
      button2.callback = advanced_callback
      view = View()
      view.add_item(button1)
      view.add_item(button2)
      await ctx.respond(embed = eastern, view = view)
  except IndexError:
      await ctx.respond("Standings for season not available")
  except ValueError:
      await ctx.respond("Standings for season not available")
  except basketball_reference_web_scraper.errors.InvalidSeason:
      await ctx.respond("Standings for season not available")


@client.slash_command(guild_ids = sl,description = "Search for a player")
async def search(
  ctx:  discord.ApplicationContext,
  name: discord.Option(str, "Name of the player")
  ):
    year = 2022
    results = bclient.search(term = name)
    print(results)
    if len(results['players']) == 0:
        await ctx.respond(f" **{name}** not found in basketball reference database")
        return
    player = results['players'][0]
    thing = discord.Embed()
    thing.title = player['name']
    thing.colour = discord.Colour.orange()
    thing.set_footer(text = "curfraud needs to retire and become a family man")
    thing.url = f"https://www.basketball-reference.com/players/{player['identifier'][0]}/{player['identifier']}.html"
    thing.set_image(url = BeautifulSoup(requests.get(thing.url).content,'html5lib').findAll('img')[1]['src'])

    if results['players'][0]['name'].lower() in stdict[year].keys():
        player = stdict[year][results['players'][0]['name'].lower()]
        thing.add_field(name = "Currently Active",
         value = "**{}** is currently playing for the **{}** at the **{}** position.".format(player['name'],player['team'].name.replace("_"," ").title(),player['positions'][0].name.replace("_"," ").lower())) 
    
    await ctx.respond(embed = thing)

@client.slash_command(guild_ids = sl,description = "Get leaders")
async def leaders(
  ctx: discord.ApplicationContext,
  year: discord.Option(int,"Year of the stats", default = 2022)
  ):
  options = [
    discord.SelectOption(label="Points", description="Points", emoji="💯"),
    discord.SelectOption(label="Rebounds", description="Rebounds", emoji="🏀"),
    discord.SelectOption(label="Assists", description="Assists", emoji="🤝"),
  ]

  r = requests.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html").text
  try: t_data = BeautifulSoup(r,"html5lib").find("table").tbody.find_all("tr")
  except: 
    await ctx.respond(f"No data for the season {year}")
    return
  raw = {}
  for row in t_data:
      td = row.find_all("td")
      try:
        raw[td[0].text] = float(td[-1].text)
      except IndexError:
        pass
  
  data = sorted(raw.items(), key = lambda x: -x[1])

  e = discord.Embed(
    colour = discord.Colour.orange(),
    title = f"Point per game leaders for the {year-1}-{year} Season",
    url   = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    )
  
  print("\n".join(['{:<30}'.format(player) + f': **{ppg}**' for player,ppg in data[:20]]))
  e.set_footer(text = "A * indicates a hall of fame player")
  e.add_field(name = "Top 20", value= "\n".join(['{:<30}'.format(player) + f': **{ppg}**' for player,ppg in data[:20]]),inline=False)
  
  async def c(interaction: discord.Interaction):
    await interaction.message.edit("bruh")
  s = discord.ui.Select(placeholder="test",options = options)
  s.callback = c
  v = discord.ui.View()
  v.add_item(s)
  await ctx.respond(embed = e, view = v)
  


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