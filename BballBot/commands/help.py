import discord
from discord.ext import commands


class Help(commands.Cog):
  def __init__(self,client) -> None:
    self.client = client

  @commands.command()
  async def help(self,
  ctx: discord.ApplicationContext):

    overview_text = """
    Further questions? Message `xb3#4118` directly.
    All seasons are identified by their starting season. For example, if you wanted leaders for the 1999-2000 season, you would type: `-leaders 1999`
    """

    chat_commands_text = """
    Most of BballBot's commands are chat commands, which are identified by the prefix: `-`

    `-cstats [player]` displays the career stats of any NBA player
    `-headshot [player]` displays the headshot of any NBA player
    `-help` displays help text and command info
    `-leaders [season]` displays the leaders in Pts,Reb,Ast,Blk,Stl, and Min for the specified season
    `-poeltl` initates a game of poeltl
    `-guess [player]` submits a guess for the poeltl game
    `-roster [team]` displays the current the roster of any NBA team (Can be identified by name,city or abbreviation)
    `-shotselection [player]` displays shot selection data for any active NBA player in the 2021-2022 season
    `-standings` displays the current standings
    """

    slash_commands_text = """
    Some of BballBot's commands require extra variables, and thus only have slash functionality

    `/stats [player] [year]` displays stats for an NBA player from any season
    """

    embed = discord.Embed(color = discord.Color.orange(),
      title= "Commands and Help for BballBot",
      description= overview_text)\
      .add_field(name="Chat Commands", value = chat_commands_text)\
      .add_field(name="Slash Commands", value = slash_commands_text)
    await ctx.send(embed = embed)

def setup(client):
  client.add_cog(Help(client))

