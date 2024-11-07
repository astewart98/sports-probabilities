import sys
from bs4 import BeautifulSoup
import requests

rbURL = sys.argv[1]
game_threshold = int(sys.argv[2])

page = requests.get(rbURL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_rb_rec_yards = []
for row in rows:
    rb_rec_yards = row.find_all(attrs={"data-stat": "rec_yds"})
    total_rb_rec_yards.extend(int(td.get_text()) for td in rb_rec_yards)

recent_rb_rec_yards = total_rb_rec_yards[-game_threshold:] 

print(recent_rb_rec_yards)
