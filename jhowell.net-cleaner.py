#!/usr/local/bin/python3
import re
import sys
import csv
import datetime

if len(sys.argv) < 3:
	print ("use: {} input_file output_file".format(sys.argv[0]))
	sys.exit(1)

with open(sys.argv[1]) as df:
	game_list = [line.rstrip('\n').split(',') for line in df]
#	game_list = sorted(game_list, key = lambda x: (x[1],x[2],x[3],x[4]))
for line in game_list:
    d=datetime.datetime.strptime(line[1],'%Y-%m-%d')
    line[1] = d.isoformat().partition('T')[0]
game_list = sorted(game_list, key = lambda x: (x[1],x[2],x[3]))

with open(sys.argv[2], 'w') as cf:
	i=0
	cf.write("season,date,team1,team2,score1,score2,record1,record2,neutral,playoff\n")
	while i<len(game_list)-1:
		game1 = game_list[i]
		if game1[6]=="non-IA" or game1[7]=="non-IA":
			i+=1
			cf.write("{},{},{},{},{},{},{},{},{},{}\n".format(game1[0],game1[1],game1[2],game1[3],game1[4],game1[5],game1[6],game1[7],game1[8],game1[9]))
			continue
		game2 = game_list[i+1]
		# same game, remove one, use record-to-date instead of final record
		if game1[0]==game2[0] and game1[1]==game2[1] and game1[2]==game2[2] and game1[3]==game2[3]:
			i+=2
			team1_rec1= sum([int(x) for x in game1[6].split('-')])
			team1_rec2= sum([int(x) for x in game2[6].split('-')])
			team1_rec= game2[6] if (team1_rec1 > team1_rec2) else game1[6]
			team2_rec1= sum([int(x) for x in game1[7].split('-')])
			team2_rec2= sum([int(x) for x in game2[7].split('-')])
			team2_rec = game2[7] if (team2_rec1 > team2_rec2) else game1[7]
		else:	# no match, just write the record as-is
			i+=1
			team1_rec= game1[6]
			team2_rec= game1[7]
		d=datetime.datetime.strptime(game1[1],'%Y-%m-%d')
		if d.month == 1:	# Jan games belong to last season
			game1[0] = d.year-1
		cf.write("{},{},{},{},{},{},{},{},{},{}\n".format(game1[0],game1[1],game1[2],game1[3],game1[4],game1[5],team1_rec,team2_rec,game1[8],game1[9]))
