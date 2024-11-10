import sys
from bs4 import BeautifulSoup
import requests

rbURL = sys.argv[1]
game_threshold = int(sys.argv[2])

page = requests.get(rbURL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_rb_rush_attempts = []
for row in rows:
    rb_rush_attempts = row.find_all(attrs={"data-stat": "rush_att"})
    total_rb_rush_attempts.extend(int(td.get_text()) for td in rb_rush_attempts)

recent_rb_rush_attempts = total_rb_rush_attempts[-game_threshold:] 

print(recent_rb_rush_attempts)
