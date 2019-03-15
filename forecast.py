import csv
import math

HFA = 65.0     # Home field advantage is worth 65 Elo points
K = 20.0       # The speed at which Elo ratings change
REVERT = 1/3.0 # Between seasons, a team retains 2/3 of its previous season's rating

# Some between-season reversions of unknown origin
REVERSIONS = { }

class Forecast:

    @staticmethod
    def forecast(games):
        """ Generates win probabilities in the my_prob1 field for each game based on Elo model """

        # Initialize team objects to maintain ratings
        teams = {}
        for row in [item for item in csv.DictReader(open("data/initial_elos.csv"))]:
            teams[row['team']] = {
                'name': row['team'],
                'season': None,
                'elo': float(row['elo'])
            }

        for game in games:
            if game['team1'] in teams:
                team1 = teams[game['team1']] 
            else:  # Non-IA teams elo=1100
                team1 = {
                'name': game['team1'],
                'season': None,
                'elo': 1100.0
                }
            if game['team2'] in teams:
                team2 = teams[game['team2']] 
            else:  # Non-IA teams elo=1100
                team2 = {
                'name': game['team2'],
                'season': None,
                'elo': 1100.0
                }

            # Revert teams at the start of seasons
            for team in [team1, team2]:
                if team['season'] and game['season'] != team['season']:
                    k = "%s%s" % (team['name'], game['season'])
                    if k in REVERSIONS:
                        team['elo'] = REVERSIONS[k]
                    else:
                        team['elo'] = 1505.0*REVERT + team['elo']*(1-REVERT)
                team['season'] = game['season']

            # Elo difference includes home field advantage
            elo_diff = team1['elo'] - team2['elo'] + (0 if game['neutral'] == 1 else HFA)

            # This is the most important piece, where we set my_prob1 to our forecasted probability
            #if game['elo_prob1'] != None:
            #    game['my_prob1'] = 1.0 / (math.pow(10.0, (-elo_diff/400.0)) + 1.0)
            game['elo_prob1'] = 1.0 / (math.pow(10.0, (-elo_diff/400.0)) + 1.0)

            # If game was played, maintain team Elo ratings
            if game['score1'] != None:

                # Margin of victory is used as a K multiplier
                pd = abs(game['score1'] - game['score2'])
                if game['score1'] == game['score2']:
                    game['result1'] = 0.5
                else:
                    game['result1'] = (1.0 if game['score1'] > game['score2'] else 0)
                mult = math.log(max(pd, 1) + 1.0) * (2.2 / (1.0 if game['result1'] == 0.5 else ((elo_diff if game['result1'] == 1.0 else -elo_diff) * 0.001 + 2.2)))

                # Elo shift based on K and the margin of victory multiplier
                shift = (K * mult) * (game['result1'] - game['elo_prob1'])

                game['elo1'] = team1['elo']
                game['elo2'] = team2['elo']
#                print ("{} {} {}({}) vs {}({}) -> {}-{}  elo1={} elo2={} elo_prob1={}\n".format(game['season'],game['date'],game['team1'],game['record1'],game['team2'],game['record2'],game['score1'],game['score2'],team1['elo'],team2['elo'],game['elo_prob1'] ))

                # Apply shift
                team1['elo'] += shift
                team2['elo'] -= shift
