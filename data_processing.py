from basketball_reference_web_scraper import client as bclient
from collections import defaultdict
import mysql.connector

db = mysql.connector.connect(
  host = "localhost",
  user = "root",
  passwd = "server343s"
)

#adding stats to database
stdict = defaultdict(dict)
for year in range(2022,2023):
    print(year)
    for k in bclient.players_season_totals(season_end_year=year):
        stdict[year][k["name"].lower()] = k

astdict = defaultdict(dict)
for year in range(2022,2023):
    print(year)
    for k in bclient.players_advanced_season_totals(season_end_year=year):
        astdict[year][k["name"].lower()] = k


def calculate_stats(player:dict) -> dict:
    '''
    Takes raw player data as an input and returns calculated statistics
    '''
    ret = {}
    g = player['games_played']
    ret['ppg'] = round(player['points']/g,1)
    ret['apg'] = round(player['assists']/g,1)
    ret['rpg'] = round(player['offensive_rebounds']/g +player['defensive_rebounds']/g,1)
    ret['spg'] = round(player['steals']/g,1)
    ret['bpg'] = round(player['blocks']/g,1)
    ret['topg'] = round(player['turnovers']/g,1)
    ret['fpg'] = round(player['personal_fouls']/g,1)
    if player['attempted_field_goals'] == 0:
        ret['fgp'] = 0.0
    else:
        ret['fgp'] = round(100*(player['made_field_goals']/player['attempted_field_goals']),1)
    if player['attempted_three_point_field_goals'] == 0:
        ret['3pp'] = 0.0
    else:
        ret['3pp'] = round(100*(player['made_three_point_field_goals']/player['attempted_three_point_field_goals']),1)
    if player['attempted_free_throws'] == 0:
        ret['ftp'] = 0.0
    else:
        ret['ftp'] = round(100*(player['made_free_throws']/player['attempted_free_throws']),1)

    return ret
