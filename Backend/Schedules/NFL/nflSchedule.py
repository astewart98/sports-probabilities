import json
from bs4 import BeautifulSoup
import requests

def update_schedule(file_path='Backend/Schedules/NFL/nflSchedule.json'):
    """
    Fetch the MLB schedule, extract team and pitcher information, and save it to a JSON file.
    
    Parameters:
    - file_path: The path where the JSON file will be saved.
    """

    url = 'https://www.fantasypros.com/nfl/schedule.php'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Fetch the HTML content from the website
    table = soup.find('table', {'class': 'table table-bordered'})

    href_pairs = []

    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        away_team = tds[0].find_all('a')[0]['href'] if tds[0].find_all('a') else None
        home_team = tds[0].find_all('a')[1]['href'] if len(tds[0].find_all('a')) > 1 else None
        if away_team and home_team:
            href_pairs.append({
                'Away Team': away_team, 
                'Home Team': home_team, 
            })
            
    # Save the href pairs to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(href_pairs, json_file, indent=4)

# Allow the script to be run standalone
if __name__ == "__main__":
    update_schedule()