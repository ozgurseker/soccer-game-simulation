import pandas as pd
import numpy as np 
import os


os.chdir(r"C:\Users\oseker16\Documents\vs studio\soccer research\explanatory analysis")


season_file_names = list()
seasons = list()
leagues_inSeason = list()
all_leagues = list()
leagues = list()


for i in range(11):
    fy = 2018 - i
    ey = 2019 - i
    season = (str(fy) + "-" + str(ey))
    seasons.append(season)
    if i < 2: season_file_names.append("all-euro-data-" + season + ".xlsx")
    else: season_file_names.append("all-euro-data-" + season + ".xls")
    
for i in range(len(seasons)): 
    dfs = pd.ExcelFile(season_file_names[i])
    leagues = dfs.sheet_names
    leagues_inSeason.append(leagues)


def all_seasons_for_league(lig):
    frames = [ pd.read_excel(s, lig) for s in season_file_names ]
    return pd.concat(frames)

def all_leagues_for_season(season):
    frames = [ pd.read_excel(season_file_names[seasons.index(season)], lig) for lig in leagues ]
    return pd.concat(frames)
         
data_bySeasons = list() #indexed with seasons 
data_byLeagues = list() #indexed with leagues

for s in seasons:
    data_bySeasons.append(all_leagues_for_season(s))

for l in leagues:
    data_byLeagues.append(all_seasons_for_league(l))

for i in range(len(data_byLeagues)):
    name = "lig" + leagues[i] + ".csv"
    data_byLeagues[i].to_csv(name)

for i in range(len(seasons)):
    name = "sezon" + seasons[i] + ".csv"
    data_byLeagues[i].to_csv(name)




