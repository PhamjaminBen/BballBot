import logging
import discord
from discord.ext import commands
import tkn

sl = ["704377057529954397","732794738318639125","690009077694332973"]
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="-", intents = intents)

client.load_extension("commands.poeltl")
client.load_extension("commands.player_stats")
client.load_extension("commands.headshot")
client.load_extension("commands.shotselection")
client.load_extension("commands.standings")
client.load_extension("commands.leaders")
client.load_extension("commands.roster")

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "Westbrick construction simulator", type = "playing"))
    print(f'{client.user} has connected to Discord!')

client.run(tkn.token)