import sys
from bs4 import BeautifulSoup
import requests

pitcherURL = sys.argv[1]
pitcher_min_game_threshold = int(sys.argv[2])

page = requests.get(pitcherURL)
soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_hits_allow = []
for row in rows:
    hits_allow = row.find_all(attrs={"data-stat": "H"})
    for td in hits_allow:
        try:
            total_hits_allow.append(int(td.get_text()))
        except ValueError:
            print(f"Warning: Could not convert '{td.get_text()}' to int")
            
recent_hits_allow = total_hits_allow[-pitcher_min_game_threshold:]
print(recent_hits_allow)