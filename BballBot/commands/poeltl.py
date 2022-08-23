from discord.ext import commands
import discord
from BballBot.assets.serverlist import sl

players_dict = dict()

class Poeltl(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.slash_command(guild_ids = sl,description = "Initiate Poeltl Game")
  async def poeltl(self,ctx: discord.ApplicationContext):
    pid = ctx.author.id
    if pid in players_dict:
      await ctx.respond("Game already in progress")
    
    players_dict[ctx.author.id] = Game()
  
  @commands.slash_command(guild_ds = sl, description = "Make a poeltl guess")
  async def guess(self,
    ctx: discord.ApplicationContext,
    name: discord.Option(str,"Name of player")):
    pid = ctx.author.id
    if pid not in players_dict:
      await ctx.respond("Game not in progress. Use ``/poeltl`` to start a game")


class Game():
  def __init__(self) -> None:
    pass


def setup(client):
  client.add_cog(Poeltl(client))