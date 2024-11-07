import sys
from bs4 import BeautifulSoup
import requests

team1URL = sys.argv[1]
team_min_game_threshold = int(sys.argv[2])

page = requests.get(team1URL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_SO = []
for row in rows:
    SO = row.find_all(attrs={"data-stat": "SO"})
    total_SO.extend(int(td.get_text()) for td in SO)

team_1_recent_SO = total_SO[-team_min_game_threshold:] 

print(team_1_recent_SO)