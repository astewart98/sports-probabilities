from bs4 import BeautifulSoup
import requests
import json
import sys

file_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/MLB/Pitcher_Names/pitcherNames.json'

year = sys.argv[1]
url = f'https://www.fantasypros.com/mlb/stats/pitchers.php?range={year}&page=ALL'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

players_with_teams = []

# Search HTML for player data
player_rows = soup.find_all('td', class_='player-label player-label-report-page')

for row in player_rows:
    player_link = row.find('a', class_='fp-player-link')
    if player_link:
        player_name = player_link.text.strip()
        player_team = 'Unknown'

    small_tag = row.find('small')
    if small_tag:
        team_link = small_tag.find('a', href=True)
        if team_link and '/mlb/teams/' in team_link['href']:
            player_team = team_link['href'].strip()
        players_with_teams.append({
            "player_name": player_name,
            "player_team": player_team
        })

# Write the data to a JSON file
try:
    with open(file_path, 'w') as json_file:
        json.dump(players_with_teams, json_file, indent=4)
    print(f"Data successfully written to {file_path}")

except Exception as e:
    print(f"An error occurred: {e}")
