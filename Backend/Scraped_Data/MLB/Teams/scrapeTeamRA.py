import sys
import re
from bs4 import BeautifulSoup
import requests

team1URL = sys.argv[1]
team_min_game_threshold = int(sys.argv[2])

page = requests.get(team1URL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_runs_allow = []
for row in rows:
    runs_allow = row.find_all(attrs={"data-stat": "game_result"})
    for runs in runs_allow:
        text = runs.get_text()
        match = re.search(r'-(\d+)', text)
        if match:
            scrape_runs_allow = int(match.group(1))
            total_runs_allow.append(scrape_runs_allow)

team_1_recent_runs_allow = total_runs_allow[-team_min_game_threshold:] 

print(team_1_recent_runs_allow)