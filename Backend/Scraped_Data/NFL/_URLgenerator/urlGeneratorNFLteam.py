import json

def load_team_codes(file_path='Backend/Names/NFL/Team_Names/teamCodes.json'):
    with open(file_path, 'r') as file:
        team_codes = json.load(file)
    return team_codes

def get_abbreviation(team_code, team_codes):
    # Checks if input is a team name or URL segment
    for team_name, info in team_codes.items():
        if team_name == team_code or info['url_segment'] == team_code:
            return info['pfr_abbreviation'].lower()
    return team_name

def generate_team_url(team_code, year):
    team_codes = load_team_codes()

    team_id = get_abbreviation(team_code, team_codes)
    
    if not team_id:
        return f"Error: Team code '{team_code}' not found in team codes."

    # Generate URL
    base_url = "https://www.pro-football-reference.com/teams/"
    full_url = f"{base_url}{team_id}/{year}/gamelog"

    return full_url

# Example usage
if __name__ == "__main__":
    team_code = "/nfl/teams/las-vegas-raiders.php"
    year = "2024"
    result = generate_team_url(team_code, year)
    print(result)
