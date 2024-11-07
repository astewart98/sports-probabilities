from bs4 import BeautifulSoup
import requests
import json
import sys

file_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/NFL/RB_Names/rbNames.json'

year = sys.argv[1]
url = f'https://www.fantasypros.com/nfl/stats/rb.php?year={year}'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

players_with_teams = []

# Search HTML for player data
player_rows = soup.find_all('td', class_='player-label player-label-report-page')

for row in player_rows:    
    player_link = row.find('a', class_='player-name')
    if player_link:
        player_name = player_link.text.strip()
        player_team = 'Unknown'
        
        full_text = row.get_text(strip=True)
        if '(' in full_text and ')' in full_text:
            player_team = full_text.split('(')[-1].strip(')')
        players_with_teams.append({
            "player_name": player_name,
            "player_team": player_team
        })
    else:
        print("Player link not found!")

# Write the data to a JSON file
try:
    with open(file_path, 'w') as json_file:
        json.dump(players_with_teams, json_file, indent=4)
    print(f"Data successfully written to {file_path}")

except Exception as e:
    print(f"An error occurred: {e}")
