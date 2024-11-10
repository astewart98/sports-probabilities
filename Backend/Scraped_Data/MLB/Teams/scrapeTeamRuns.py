import sys
from bs4 import BeautifulSoup
import requests

team1URL = sys.argv[1]
team_min_game_threshold = int(sys.argv[2])

page = requests.get(team1URL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_runs = []
for row in rows:
    runs = row.find_all(attrs={"data-stat": "R"})
    total_runs.extend(int(td.get_text()) for td in runs)

team_1_recent_runs = total_runs[-team_min_game_threshold:] 

print(team_1_recent_runs)