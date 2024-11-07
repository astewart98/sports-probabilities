import sys
from bs4 import BeautifulSoup
import requests
import re

teamURL = sys.argv[1]
game_threshold = int(sys.argv[2])

page = requests.get(teamURL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find_all('tr', id=re.compile(r'_opp'))

if not rows:
    print("No matching rows found with '_opp' in ID")
    sys.exit()

total_points_against = []
for row in rows:
    points_against = row.find_all(attrs={"data-stat": "pts_def"})
    for td in points_against:
        text = td.get_text().strip()
        if text.isdigit():  
            total_points_against.append(int(text))

team_recent_points_against = total_points_against[-game_threshold:]  

print(team_recent_points_against)