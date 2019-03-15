#!/usr/local/bin/python3
import re
from time import sleep
from random import randint
from requests import get
from bs4 import BeautifulSoup, NavigableString

# https://www.reddit.com/r/CFB/comments/4cr1en/when_begins_the_modern_era_of_football/
years_keep = list(range(1998, 2019))  # could also start at 1992

with open('data/team-names.txt') as tf:
	team_list = [line.rstrip('\n') for line in tf]

of = open('cfb-scraped.csv', 'w')
for team in team_list:
	sleep(randint(1,3))
	url = 'http://www.jhowell.net/cf/scores/%s.htm' % (team)
	print(url)
	response = get(url)
	#print(response.text[:1000])
	html_soup = BeautifulSoup(response.text, 'html.parser')
	type(html_soup)

	# loop on season/year
	seasons = html_soup.find_all('table')[1:]
	#print ("{} seasons".format(len(seasons)))
	for season in seasons:
		year=int(season.a.get('name'))
		if not year in years_keep:
			continue
		print ("%s - %s" % (team, year))
		team_wins=0
		team_losses=0
		for game in season.children:
			if isinstance(game, NavigableString):
				continue
			#print(game)
			if len(game.contents) < 6: continue
			date = game.contents[0].text
			#print(game.contents[1])
			home = game.contents[1].text
			if team.count('('):
				team1 = team[:team.find('(')].replace(" ", "") + re.search(r'\((.*?)\)',team).group(1)
			else:
				team1 = team
			team2 = game.contents[2].text
			if team2.count('(') > 1:   # Miami (Florida) (2-5)
				team2 = team2[team2.find('*')+1:team2.find('(')].replace(" ", "") + re.search(r'\((.*?)\)',team2).group(1)
			else:
				team2 = team2[team2.find('*')+1:team2.find('(')].replace(" ", "")
			score1 = game.contents[4].text
			score2 = game.contents[5].text
			neutral = 0
			if len(game.contents) > 6: neutral = 1
			bowl = 0
			if len(game.contents) > 7: bowl = 1
			if int(score1) >= int(score2):
				team_wins+=1
			else:
				team_losses+=1
			rec1=str(team_wins)+'-'+str(team_losses)
			if game.contents[2].text.count('(') > 1:   # Miami (Florida) (2-5)
				rec2=re.findall(r'\((.*?)\)', game.contents[2].text)[1]
			else:
				rec2=re.search(r'\((.*?)\)', game.contents[2].text).group(1)
			# home team listed first, if Neutral game, lexical order
			if home == "@" or (neutral==1 and team2 < team1):
				team1,team2=team2,team1
				score1,score2=score2,score1
				rec1,rec2=rec2,rec1
			month = date.split('/')[0]
			day = date.split('/')[1]
			of.write("{},{}-{}-{},{},{},{},{},{},{},{},{}\n".format(year,year,month,day,team1,team2,score1,score2,rec1,rec2,neutral,bowl))
of.close()

