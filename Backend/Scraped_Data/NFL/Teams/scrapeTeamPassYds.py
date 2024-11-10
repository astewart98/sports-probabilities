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

total_pass_yds = []
for row in rows:
    pass_yds = row.find_all(attrs={"data-stat": "pass_yds"})
    for td in pass_yds:
        text = td.get_text().strip()
        if text.isdigit():  
            total_pass_yds.append(int(text))

team_recent_pass_yds = total_pass_yds[-game_threshold:]  

print(team_recent_pass_yds)