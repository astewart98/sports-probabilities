import sys
from bs4 import BeautifulSoup
import requests

te_wrURL = sys.argv[1]
game_threshold = int(sys.argv[2])

page = requests.get(te_wrURL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_te_wr_receptions = []
for row in rows:
    te_wr_receptions = row.find_all(attrs={"data-stat": "rec"})
    total_te_wr_receptions.extend(int(td.get_text()) for td in te_wr_receptions)

recent_te_wr_receptions = total_te_wr_receptions[-game_threshold:] 

print(recent_te_wr_receptions)
