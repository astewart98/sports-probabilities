import sys
from bs4 import BeautifulSoup
import requests

team1URL = sys.argv[1]
team_min_game_threshold = int(sys.argv[2])

page = requests.get(team1URL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_walks = []
for row in rows:
    walks = row.find_all(attrs={"data-stat": "BB"})
    total_walks.extend(int(td.get_text()) for td in walks)

team_1_recent_walks = total_walks[-team_min_game_threshold:] 

print(team_1_recent_walks)