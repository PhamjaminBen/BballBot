import difflib
from discord.ext import commands
import discord
from BballBot.assets.serverlist import sl
from BballBot.assets.player_lists import rostered_players,rostered_names,names_to_rostered_players
from BballBot.assets.dbconnection import db_cursor
import random

players_dict = dict()

class Poeltl(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.slash_command(guild_ids = sl,description = "Initiate Poeltl Game")
  async def poeltl(self,ctx: discord.ApplicationContext):
    pid = ctx.author.id
    if pid in players_dict:
      await ctx.respond("Game already in progress, use ``/guess quit`` to quit your previous game")
      return
    
    players_dict[ctx.author.id] = Game()
    await ctx.respond("Poeltl initiated!")
  

  @commands.command()
  async def poeltl(self,ctx: discord.ApplicationContext):
    pid = ctx.author.id
    if pid in players_dict:
      await ctx.send("Game already in progress, use ``/guess quit`` to quit your previous game")
      return
    
    players_dict[ctx.author.id] = Game()
    await ctx.send("Poeltl initiated!")
  

  @commands.slash_command(guild_ds = sl, description = "Make a poeltl guess")
  async def guess(self,
    ctx: discord.ApplicationContext,
    name: discord.Option(str,"Name of player")):

    pid = ctx.author.id
    if pid not in players_dict:
      await ctx.respond("Game not in progress. Use ``/poeltl`` to start a game")
      return
    
    if name.lower() == "quit":
      del players_dict[ctx.author.id]
      await ctx.respond("Poeltl terminated")
      return
    
    result = difflib.get_close_matches(name,rostered_names)

    if not result:
      await ctx.respond(f"``{name}`` is not currently rostered")
      return
    
    name = result[0]
    guess_result = players_dict[ctx.author.id].guess(names_to_rostered_players[name])
    await ctx.respond(guess_result)
    if players_dict[ctx.author.id].get_guess() == 9:
      del players_dict[ctx.author.id]
  

  @commands.command()
  async def guess(self,
    ctx: discord.ApplicationContext,
    *name: str):
    name = " ".join(["".join(word) for word in name])

    pid = ctx.author.id
    if pid not in players_dict:
      await ctx.send("Game not in progress. Use ``/poeltl`` to start a game")
      return
    
    if name.lower() == "quit":
      del players_dict[ctx.author.id]
      await ctx.send("Poeltl terminated")
      return
    
    result = difflib.get_close_matches(name,rostered_names)

    if not result:
      await ctx.send(f"``{name}`` is not currently rostered")
      return
    
    name = result[0]
    guess_result = players_dict[ctx.author.id].guess(names_to_rostered_players[name])
    await ctx.send(guess_result)
    if players_dict[ctx.author.id].get_guess() == 9:
      del players_dict[ctx.author.id]



class Game():
  def __init__(self) -> None:
    self._target = random.choice(rostered_players)
    while '-' in self._target:
      self._target = random.choice(rostered_players)

    self._guess = 1
    self._string = f"``{'Name'.center(25)}      Team    Conf     Div     Pos    Ht         Age      #       ``\n"
    db_cursor.execute(f"SELECT team FROM prev_teams where name = \"{self._target[0]}\";")
    self._prev_teams = {x[0] for x in db_cursor.fetchall()}

  def get_guess(self) -> int:
    return self._guess

  def guess(self, guess: tuple) -> str:
    guess_result = self._compare_players(guess)
    self._string += f"``{self._guess})" + guess_result[1] + "\n"
    self._guess += 1

    if guess_result[0]:
      self._string += f"Congrats!, you guessed the poeltl in **{self._guess-1}** guesses"
      self._guess = 9

    elif self._guess == 9:
      self._string += "``Sorry, the correct answer is:``\n"
      self._string += f"``  {self._compare_players(self._target)[1]}"
    
    return self._string

  

  def _compare_players(self, guess: tuple) -> tuple:
    correct = False

    retstr = f"{guess[0].center(25)}``"
    if self._target[0] == guess[0]: 
      retstr += "🟩"
      correct = True
    else: 
      retstr += "⬜"

    retstr += f" ``{guess[1]} ``"
    if self._target[1] == guess[1]:
      retstr += "🟩"
    elif guess[1] in self._prev_teams:
      retstr += "🟨"
    else:
      retstr += "⬜"

    retstr += f" ``{guess[2][:4]}``"
    retstr += "🟩" if self._target[2] == guess[2] else "⬜"

    retstr += f" ``{guess[3].center(4)}``"
    retstr += "🟩" if self._target[3] == guess[3] else "⬜"

    retstr += f" ``{guess[4].center(3)}``"
    if guess[4] == "-": retstr += "⬜"
    else:
      if guess[4] == self._target[4]: retstr += "🟩"
      elif set(guess[4].split('-')).intersection(set(self._target[4].split('-'))) != set(): retstr += "🟨"
      else: retstr += "⬜"

    retstr += f" ``{guess[5].center(4)}``"
    if guess[5] == "-": retstr += "⬜⏺️"
    else:
      gh,th = self._raw_height(guess[5]), self._raw_height(self._target[5])
      if gh == th: retstr += "🟩⏺️"
      else:
        if abs(gh-th) <= 2: retstr += "🟨"
        else: retstr += "⬜"
        retstr += "⬆️" if gh < th else "⬇️"
    
    retstr += f" ``{guess[6]}``"
    if guess[6] == "-": retstr += "⬜⏺️"
    else:
      ga,ta = int(guess[6]),int(self._target[6])
      if ga == ta: retstr += "🟩⏺️"
      else:
        if abs(ga-ta) <= 2: retstr += "🟨"
        else: retstr += "⬜"
        retstr += "⬆️" if ga < ta else "⬇️"
    
    retstr += f" ``{guess[7].ljust(2)}``"
    if guess[7] == "-": retstr += "⬜⏺️"
    else:
      gj,tj = int(guess[7]),int(self._target[7])
      if gj == tj: retstr += "🟩⏺️"
      else:
        if abs(gj-tj) <= 2: retstr += "🟨"
        else: retstr += "⬜"
        retstr += "⬆️" if gj < tj else "⬇️"

    return (correct,retstr)
  
  def _raw_height(self, h:str) -> int:
    h = h.split("-")
    return 12*int(h[0])+ int(h[1])
    
    

def setup(client):
  client.add_cog(Poeltl(client))