import json
from bs4 import BeautifulSoup
import requests

def update_schedule(file_path='/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Schedules/MLB/mlbSchedule.json'):
    """
    Fetch the MLB schedule, extract team and pitcher information, and save it to a JSON file.
    
    Parameters:
    - file_path: The path where the JSON file will be saved.
    """
    
    url = 'https://www.fantasypros.com/mlb/schedules/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Fetch the HTML content from the website
    table = soup.find('table', {'class': 'table table-full table-condensed'})

    href_pairs = []

    capture_data = False
    left_counter = 0

    for tr in table.find_all('tr'):
        if 'left' in tr.get('class', []):
            left_counter += 1
            if left_counter == 2:
                capture_data = True
            elif left_counter == 3:
                capture_data = False
                break
        elif capture_data:
            tds = tr.find_all('td')
            if len(tds) >= 6:
                away_team = tds[0].find('a')['href'] if tds[0].find('a') else None
                home_team = tds[1].find('a')['href'] if tds[1].find('a') else None
                
                away_pitcher = "TBD"
                home_pitcher = "TBD"
                
                away_pitcher_td = tds[3]
                away_pitcher_tag = away_pitcher_td.find('a', class_='fp-player-link')
                if away_pitcher_tag and 'fp-player-name' in away_pitcher_tag.attrs:
                    away_pitcher = away_pitcher_tag['fp-player-name']

                home_pitcher_td = tds[5]
                home_pitcher_tag = home_pitcher_td.find('a', class_='fp-player-link')
                if home_pitcher_tag and 'fp-player-name' in home_pitcher_tag.attrs:
                    home_pitcher = home_pitcher_tag['fp-player-name']

                if away_team and home_team:
                    href_pairs.append({
                        'Away Team': away_team, 
                        'Home Team': home_team, 
                        'Away Pitcher': away_pitcher, 
                        'Home Pitcher': home_pitcher
                    })

    # Save the href pairs to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(href_pairs, json_file, indent=4)

# Allow the script to be run standalone
if __name__ == "__main__":
    update_schedule()