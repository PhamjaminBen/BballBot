from discord.ext import commands
from discord.ui import View, Button
import discord
from BballBot.assets.dbconnection import db_cursor

class Standings(commands.Cog):
  def __init__(self, client) -> None:
    self.client = client
  
  @commands.command()
  async def standings(self,
    ctx:  discord.ApplicationContext):
    db_cursor.execute("SELECT abbreviation,w,l from team where conference = \"Eastern\" order by w desc")
    east_text = ""
    for i,x in enumerate(db_cursor.fetchall()):
      east_text += f"`{str(i+1).zfill(2)}. {str(x[0]).zfill(2)} | Record: {str(x[1]).zfill(2)}-{str(x[2]).zfill(2)}`\n"

    db_cursor.execute("SELECT abbreviation,w,l from team where conference = \"Western\" order by w desc")
    west_text = ""
    for i,x in enumerate(db_cursor.fetchall()):
      west_text += f"`{str(i+1).zfill(2)}. {str(x[0]).zfill(2)} | Record: {str(x[1]).zfill(2)}-{str(x[2]).zfill(2)}`\n"

    east_embed = discord.Embed(
      title = f"Standings for the **2021-2022** NBA Season",
      color = discord.Colour.orange(),
      url = "https://www.basketball-reference.com/leagues/NBA_2021_standings.html" )
    east_embed.add_field(name = "Team", value = east_text)

    west_embed = discord.Embed(
      title = f"Standings for the **2021-2022** NBA Season",
      color = discord.Colour.orange(),
      url = "https://www.basketball-reference.com/leagues/NBA_2021_standings.html" )
    west_embed.add_field(name = "Team", value = west_text)

    
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
    await ctx.send(embed = east_embed, view = view)

def setup(client):
  client.add_cog(Standings(client))