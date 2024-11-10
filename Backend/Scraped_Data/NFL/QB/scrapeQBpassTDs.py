import sys
from bs4 import BeautifulSoup
import requests

qbURL = sys.argv[1]
game_threshold = int(sys.argv[2])

page = requests.get(qbURL)

soup = BeautifulSoup(page.text, 'html.parser')

# Fetch the HTML content from the website
rows = soup.find('tbody').find_all('tr', id=True)

total_pass_tds = []
for row in rows:
    pass_tds = row.find_all(attrs={"data-stat": "pass_td"})
    total_pass_tds.extend(int(td.get_text()) for td in pass_tds)

recent_pass_tds = total_pass_tds[-game_threshold:] 

print(recent_pass_tds)