import sys
from bs4 import BeautifulSoup
import requests

pitcherURL = sys.argv[1]
pitcher_min_game_threshold = int(sys.argv[2])

page = requests.get(pitcherURL)
soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_SO = []
for row in rows:
    SO = row.find_all(attrs={"data-stat": "SO"})
    for td in SO:
        try:
            total_SO.append(int(td.get_text()))
        except ValueError:
            print(f"Warning: Could not convert '{td.get_text()}' to int")
            
recent_SOs = total_SO[-pitcher_min_game_threshold:]
print(recent_SOs)