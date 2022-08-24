import logging
import discord
from discord.ext import commands

sl = ["704377057529954397","732794738318639125","690009077694332973"]
logging.basicConfig(level=logging.INFO)

token = 'OTM2Njg5NTEyNzExNTk4MTIx.GwvpS3.5aIig7TX9lEqQ32-hE5t1wVEQgkMmuu2iTaDE0'

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="-", intents = intents)

client.load_extension("commands.poeltl")
client.load_extension("commands.player_stats")
client.load_extension("commands.headshot")
client.load_extension("commands.shotselection")
client.load_extension("commands.standings")
client.load_extension("commands.leaders")

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
    if "metu" in m.content.lower() and m.author.discriminator != "8178":
        await m.channel.send("ChiMickey Metu")
    if "chimezie" in m.content.lower() and m.author.discriminator != "8178":
        await m.channel.send("ChiMickey Metu")
    if "mezie" in m.content.lower() and m.author.discriminator != "8178":
        await m.channel.send("ChiMickey Metu")

client.run(token)