import subprocess
import sys
import requests
import string
from bs4 import BeautifulSoup

batter_names_script = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/MLB/Batter_Names/batterNames.py'
pitcher_names_script = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/MLB/Pitcher_Names/pitcherNames.py'

# Checks URL for table (meaning correct player found)
def check_url_for_table(full_url):
    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            if table:
                return True
    except Exception as e:
        print(f"Error checking URL: {e}")
    return False

# Removes suffixes
def remove_suffix(name):
    suffixes = ["Jr.", "Sr.", "I", "II", "III"]
    name_parts = name.split()
    if name_parts[-1] in suffixes:
        name_parts = name_parts[:-1]
    return ' '.join(name_parts)

def generate_player_url(player_name, year, position):
    if player_name:
        if position == 'batter':
            subprocess.run(['python3', batter_names_script, year])
        elif position == 'pitcher':
            subprocess.run(['python3', pitcher_names_script, year])
        player_name = remove_suffix(player_name)
        player_name = ''.join(char for char in player_name if char not in string.punctuation)
        names = player_name.split()

        # Extract the first and last name
        if len(names) > 1:
            first_name = names[0]
            last_name = ''.join(names[1:])
        # Handle rare cases with only one name part
        else:
            first_name = names[0]
            last_name = ''

        # Extracts specific amount of letters from both names
        first_name = first_name[:2]
        last_name = last_name[:5]

        player_id = (last_name + first_name)
    else:
        player_id = ""

    if position == 'batter':
        position_code = 'b'
    elif position == 'pitcher':
        position_code = 'p'
    else:
        position_code = ''

    # Generate URL and check its validity
    base_url = "https://www.baseball-reference.com/players/gl.fcgi"
    historic_player_value = 1

    while True:
        full_url = f"{base_url}?id={player_id}{historic_player_value:02d}&t={position_code}&year={year}"
        print(full_url)
        
        if check_url_for_table(full_url):
            return full_url
        
        # If player not found, increase historic_player_value
        historic_player_value += 1

        if historic_player_value > 8:
            print(f"Max attempts reached for {player_name}. No valid URL found.")
            return None

        
if __name__ == '__main__':
    player_name = sys.argv[1]
    year = sys.argv[2]
    position = sys.argv[3]

    result = generate_player_url(player_name, year, position)
    print(result)
