NCAA College Football Scraper
==============================
If you just want the data (1998-2018), just grab cfb-clean.csv or cfb-elo.csv (if you also want ELO data).

To Scrape and clean college football scores for as far back as 19XX, do the following:
You need the following metadata files:
/data/team-names.txt
/data/initial_elos.csv

Edit the scraper for the seasons you want:
years_keep = list(range(1998, 2019))

Run the data scraper:
$ ./jhowell.net-scraper.py
You should end up with a file cfb-scraped.csv.  Replace all occurrances of "TexasA&M" with "TexasAM" (this is the only manual step)

Run the data cleaner:
$ ./jhowell.net-cleaner.py cfb-scraped.csv cfb-clean.csv

You should end up with a little more than half the number of lines of the original scraped file (since scraping gets almost all games twice)
$ wc -l cfb-scraped.csv
   30935 cfb-scraped.csv
$ wc -l cfb-clean.csv
   16605 cfb-clean.csv

Optional: Calculate ELO for teams/games:
$ ./calc-elo.py cfb-clean.csv cfb-elo.csv

Many thanks to Jim Howell, http://www.jhowell.net/ who collected and maintains the data.  Also thanks to this project https://github.com/fivethirtyeight/nfl-elo-game, which code I modified to generate the ELO scores.
