import sys
from bs4 import BeautifulSoup
import requests

qbURL = sys.argv[1]
game_threshold = int(sys.argv[2])

page = requests.get(qbURL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_qb_rush_yards = []
for row in rows:
    qb_rush_yards = row.find_all(attrs={"data-stat": "rush_yds"})
    total_qb_rush_yards.extend(int(td.get_text()) for td in qb_rush_yards)

recent_qb_rush_yards = total_qb_rush_yards[-game_threshold:] 

print(recent_qb_rush_yards)