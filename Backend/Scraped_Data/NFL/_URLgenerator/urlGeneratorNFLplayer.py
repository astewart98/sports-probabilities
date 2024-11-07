import subprocess
import sys
import requests
import string
from bs4 import BeautifulSoup

qb_names_script = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/NFL/QB_Names/qbNames.py'
rb_names_script = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/NFL/RB_Names/rbNames.py'
wr_names_script = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/NFL/WR_Names/wrNames.py'
te_names_script = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/NFL/TE_Names/teNames.py'

# Removes suffixes
def remove_suffix(name):
    suffixes = ["Jr.", "Sr.", "I", "II", "III"]
    name_parts = name.split()
    if name_parts[-1] in suffixes:
        name_parts = name_parts[:-1]  # Remove the suffix
    return ' '.join(name_parts)

# Checks URL for table (meaning correct player found)
def check_for_proper_url(full_url, position, year):
    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table')
            if table:
                posID = soup.find('div', {'id': 'meta'})
                ps = posID.find_all('p') if posID else []
                
                for paragraph in ps:
                    pos_text = paragraph.get_text(separator=' ', strip=True)

                    # Check if URL position matches position input
                    if 'Position' in pos_text:
                        position_parts = pos_text.split(':')
                        if len(position_parts) > 1:
                            # Get the first word after "Position:"
                            posResult = position_parts[1].strip().split()[0].lower()
                            print(f'Position Result: {posResult}')

                            # Check if the position matches
                            if posResult == position.lower():
                                return True
                            else:
                                print("Position not found, checking for draft link...")
                                break

                # If position not found, check year drafted (if rookie status)
                draft_links = soup.find_all('a', string=lambda text: 'NFL Draft' in text if text else False)
                if draft_links:
                    for draft_link in draft_links:
                        draft_text = draft_link.get_text()
                        if draft_text == f'{year} NFL Draft':
                            return True
                else:
                    print('Draft link not found.')

    except Exception as e:
        print(f"Error checking URL: {e}")
    
    return False

def generate_nfl_player_url(player_name, year, position):
    if player_name == "Amon-Ra St. Brown":
        player_id = "StxxAm"
    elif player_name:
        if position == 'qb':
            subprocess.run(['python3', qb_names_script, year])
        elif position == 'rb':
            subprocess.run(['python3', rb_names_script, year])
        elif position == 'wr':
            subprocess.run(['python3', wr_names_script, year])
        elif position == 'te':
            subprocess.run(['python3', te_names_script, year])
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
        last_name = last_name[:4]
        # If last name is too short, add x's
        if len(last_name) < 4:
            last_name += 'x' * (4 - len(last_name))
        player_id = (last_name + first_name)
    else:
        player_id = ""

    # Generate URL and check its validity
    base_url = "https://www.pro-football-reference.com/players/A/"
    historic_player_value = 0

    while True:
        full_url = f"{base_url}{player_id}{historic_player_value:02d}/gamelog/{year}"
        print(full_url)
        
        if check_for_proper_url(full_url, position, year):
            return full_url
        
        # If player not found, increase historic_player_value
        historic_player_value += 1

        if historic_player_value > 10:
            print(f"Max attempts reached for {player_name}. No valid URL found.")
            return None

        
if __name__ == '__main__':
    player_name = sys.argv[1]
    year = sys.argv[2]
    position = sys.argv[3]

    result = generate_nfl_player_url(player_name, year, position)
    print(result)
