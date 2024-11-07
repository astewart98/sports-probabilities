import sys
from bs4 import BeautifulSoup
import requests

batterURL = sys.argv[1]
batter_min_game_threshold = int(sys.argv[2])

page = requests.get(batterURL)
soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_hits = []
for row in rows:
    hits = row.find_all(attrs={"data-stat": "H"})
    total_hits.extend(int(td.get_text()) for td in hits)

recent_hits = total_hits[-batter_min_game_threshold:]

print(recent_hits)