import sys
from bs4 import BeautifulSoup
import requests

pitcherURL = sys.argv[1]
pitcher_min_game_threshold = int(sys.argv[2])

page = requests.get(pitcherURL)
soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_IP = []
for row in rows:
    IP = row.find_all(attrs={"data-stat": "IP"})
    for td in IP:
        try:
            total_IP.append(float(td.get_text()))
        except ValueError:
            print(f"Warning: Could not convert '{td.get_text()}' to float")
            
recent_IP = total_IP[-pitcher_min_game_threshold:]
print(recent_IP)