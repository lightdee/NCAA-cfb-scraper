#!/usr/local/bin/python3
import sys
from util import *
from forecast import *

if len(sys.argv) < 3:
    print ("use: {} games.csv output_elo.csv".format(sys.argv[0]))
    sys.exit(1)

# Read historical games from CSV
games = Util.read_games(sys.argv[1])

# Forecast every game
Forecast.forecast(games)

with open(sys.argv[2], 'w') as elof:
    elof.write("season,date,team1,team2,score1,score2,record1,record2,neutral,playoff,elo1,elo2,elo_prob1\n")
    for game in games:
        elof.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(game['season'],game['date'],game['team1'],game['team2'],game['score1'],game['score2'],game['record1'],game['record2'],game['neutral'],game['playoff'],game['elo1'],game['elo2'],game['elo_prob1'] ))
