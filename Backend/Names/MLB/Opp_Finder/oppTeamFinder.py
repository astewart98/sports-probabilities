import json

team_names_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/MLB/Team_Names/teamCodes.json'
pitcher_names_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/MLB/Pitcher_Names/pitcherNames.json'
schedule_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Schedules/MLB/mlbSchedule.json'

def find_team_url_from_pitcher(pitcher_name):
    with open(pitcher_names_path, 'r') as f:
        pitchers = json.load(f)
    
    # Find the team's URL segment from the pitcher's name
    for pitcher in pitchers:
        if pitcher['player_name'] == pitcher_name:
            return pitcher['player_team']
    
    return None

def find_opposing_team(player_name, position):
    if position == 'team':
        with open(team_names_path, 'r') as f:
            team_names = json.load(f)
        
        # Find the team's URL segment from team name
        player_team_url = team_names.get(player_name, {}).get('url_segment')
        if player_team_url is None:
            return None
        
        with open(schedule_path, 'r') as f:
            schedule = json.load(f)
        
        # Find the opposing team based on the players team URL
        for game in schedule:
            if game['Away Team'] == player_team_url:
                return game['Home Team']
            elif game['Home Team'] == player_team_url:
                return game['Away Team']
        
        return None
    
    elif position == 'pitcher':
        # Find the team's URL from the pitcher's name
        player_team_url = find_team_url_from_pitcher(player_name)
        if player_team_url is None:
            return None
        
        with open(schedule_path, 'r') as f:
            schedule = json.load(f)
        
        # Find the opposing team based on the players team URL
        for game in schedule:
            if game['Away Team'] == player_team_url:
                return game['Home Team']
            elif game['Home Team'] == player_team_url:
                return game['Away Team']
        
        return None
    
    return None

# Example usage
if __name__ == "__main__":
    result_team = find_opposing_team("Tigers", "team")
    print(f"Opposing team for Tigers: {result_team}")
    
    result_pitcher = find_opposing_team("Tarik Skubal", "pitcher")
    print(f"Opposing team for Tarik Skubal: {result_pitcher}")
