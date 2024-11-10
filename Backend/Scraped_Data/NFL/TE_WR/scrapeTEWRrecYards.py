import sys
from bs4 import BeautifulSoup
import requests

te_wrURL = sys.argv[1]
game_threshold = int(sys.argv[2])

page = requests.get(te_wrURL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_te_wr_rec_yards = []
for row in rows:
    te_wr_rec_yards = row.find_all(attrs={"data-stat": "rec_yds"})
    total_te_wr_rec_yards.extend(int(td.get_text()) for td in te_wr_rec_yards)

recent_te_wr_rec_yards = total_te_wr_rec_yards[-game_threshold:] 

print(recent_te_wr_rec_yards)