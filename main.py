import os
import discord
from keep_alive import keep_alive
import nba_api
import requests
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from discord.ext import commands
import logging
import requests
import time
from basketball_reference_web_scraper import client as bclient
from basketball_reference_web_scraper.data import OutputType
import basketball_reference_web_scraper

HEADERS = headers = {
            'x-rapidapi-host': "nba-stats4.p.rapidapi.com",
            'x-rapidapi-key': "3a84732a7fmsh09a7778c123c61ap145571jsn4e31058e61d1"
            }

intents = discord.Intents.default()
intents.members = True

client = commands.Bot("-", case_insensitive = True, brief = "A bot that gets basketball statistic", strip_after_prefix = True,  intents=intents)


token = os.environ['TOKEN']

async def on_ready():
    await client.change_presence(activity = discord.Game(name = "Westbrick construction simulator", type = "playing"))
    print(f'{client.user} has connected to Discord!')


async def on_message(m):
    if "lebron" in m.content.lower() and m.author.discriminator != "8178":
        await m.channel.send(m.content.replace("lebron","LeBum").replace("LeBron","LeBum").replace("Lebron","LeBum"))

@client.command(brief = "Gets the information of an active NBA player. Other aliases: \'ap\'", aliases = ['ap'])
async def activeplayer(ctx,*name):
    try:
        player = stdict[" ".join(name).lower()]
    except KeyError:
        await ctx.send(f"**{' '.join(name)}** was not found, or has no games played this year")
        return
    await ctx.send("**{}** is currently playing for the **{}** at the **{}** position.".format(player['name'],player['team'].name.replace("_"," ").title(),player['positions'][0].name.replace("_"," ").lower())) 


@client.command(brief = "Gets player stats")
async def pstats(ctx,*name):
    url = "https://nba-stats4.p.rapidapi.com/players/"
    querystring = {"page":"1","full_name":" ".join(name),"per_page":"50"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    if len(response.json()) == 0:
        await ctx.send(f"Player **{' '.join(name)}** not found.")
        return
    await ctx.send(f"Getting stats for {' '.join(name)}...")
    time.sleep(1)
    url = f"https://nba-stats4.p.rapidapi.com/per_game_career_regular_season/{response.json()[0]['id']}"
    response = requests.request("GET", url, headers=HEADERS)
    stats = response.json()
    await ctx.send("In **{}** regular season games, **{}** has averages of **{}** Ppg, **{}** Apg, and **{}** Rpg".format(stats['gp']," ".join(name),stats['pts_per_game'],stats['ast_per_game'],stats['reb_per_game']))


@client.command(brief = "Gets player stats for the current year")
async def ystats(ctx,*name):
    try:
        player = stdict[" ".join(name).lower()]
    except KeyError:
        await ctx.send(f"**{' '.join(name)}** was not found, or has no games played this year")
        return
    g = player['games_played']
    await ctx.send("In **{}** regular season games this year, **{}** has averages of **{}** Ppg, **{}** Apg, and **{}** Rpg".format(player['games_played'],player['name'],round(player['points']/g,1),round(player['assists']/g,1),round(player['offensive_rebounds']/g +player['defensive_rebounds']/g,1)))

@client.command(brief = "Displays Standings for certain year")
async def standings(ctx,year = 2022):
    try:
        standings_ = bclient.standings(season_end_year = year)
        ret = f'Standings for the **{year}** NBA Season: \n**Eastern conference**:\n'

        for team in sorted(standings_[:15], key = lambda x: (x['wins'],-x['losses']), reverse = True):
            ret += "**{}**: Record: **{}-{}**\n".format(team['team'].name.replace("_"," "),team['wins'],team['losses'])
        ret += "\n**Western Conference**\n"

        for team in  sorted(standings_[15:], key = lambda x: (x['wins'],-x['losses']), reverse = True):
            ret += "**{}**: Record: **{}-{}**\n".format(team['team'].name.replace("_"," "),team['wins'],team['losses'])


        await ctx.send(ret)
    except AttributeError:
        await ctx.send("Standings for season not available")
    except basketball_reference_web_scraper.errors.InvalidSeason:
        await ctx.send("Standings for season not available")
    
@client.command()
async def t(ctx,num):
    stats = bclient.players_season_totals(season_end_year=2022)[int(num)]
    await ctx.send('\n'.join([f"{k}: {v}" for k,v in stats.items()]))
    print(stats)

#adding stats to database
stdict = {}
for k in bclient.players_season_totals(season_end_year=2022):
    stdict[k["name"].lower().replace(".","")] = k
    stdict[k["name"].lower().replace("\'","")] = k
    stdict[k["name"].lower()] = k

client.add_listener(on_ready)
client.add_listener(on_message)
keep_alive()
client.run(token)