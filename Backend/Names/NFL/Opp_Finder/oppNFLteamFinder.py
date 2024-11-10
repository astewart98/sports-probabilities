import json

team_names_path = 'Backend/Names/NFL/Team_Names/teamCodes.json'
qb_names_path = 'Backend/Names/NFL/QB_Names/qbNames.json'
rb_names_path = 'Backend/Names/NFL/RB_Names/rbNames.json'
wr_names_path = 'Backend/Names/NFL/WR_Names/wrNames.json'
te_names_path = 'Backend/Names/NFL/TE_Names/teNames.json'
schedule_path = 'Backend/Schedules/NFL/nflSchedule.json'

def find_team_url_from_player(player_name, position):
    if position == 'qb':
        with open(qb_names_path, 'r') as f:
            players = json.load(f)
    elif position == 'rb':
        with open(rb_names_path, 'r') as f:
            players = json.load(f)
    elif position == 'wr':
        with open(wr_names_path, 'r') as f:
            players = json.load(f)
    elif position == 'te':
        with open(te_names_path, 'r') as f:
            players = json.load(f)

    # Find the team's URL segment from the pitcher's name
    for player in players:
        if player['player_name'] == player_name:
            return player['player_team']
    
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
        
        # Find the opposing team based on the team URL
        for game in schedule:
            if game['Away Team'] == player_team_url:
                return game['Home Team']
            elif game['Home Team'] == player_team_url:
                return game['Away Team']
        
        return None
    
    else:
        # Find the player's team abbreviation from the player's name
        player_team_abbreviation = find_team_url_from_player(player_name, position)
        if player_team_abbreviation is None:
            return None
        
        with open(team_names_path, 'r') as f:
            team_names = json.load(f)
        
        player_team_url = None
        for team_name, team_info in team_names.items():
            if team_info['fp_abbreviation'] == player_team_abbreviation:
                player_team_url = team_info['url_segment']
                break
        
        if player_team_url is None:
            return None
        
        with open(schedule_path, 'r') as f:
            schedule = json.load(f)
        
        # Find the opposing team based on the team URL
        for game in schedule:
            if game['Away Team'] == player_team_url:
                return game['Home Team']
            elif game['Home Team'] == player_team_url:
                return game['Away Team']
        
        return None

# Example usage
if __name__ == "__main__":
    result_team = find_opposing_team("Steelers", "team")
    print(f"Opposing team for Steelers: {result_team}")

    result_player = find_opposing_team("CeeDee Lamb", "wr")
    print(f"Opposing team for Jared Goff: {result_player}")
