from discord.ext import commands
import discord
from BballBot.assets.serverlist import sl


class Poeltl(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.slash_command(guild_ids = sl,description = "Play poeltl")
  async def poeltl(self,ctx: discord.ApplicationContext):
    player = "bruh"
    await ctx.respond(f"You guessed the poeltl: {player[0]} in 1 try: {ctx.author.name}")

def setup(client):
  client.add_cog(Poeltl(client))