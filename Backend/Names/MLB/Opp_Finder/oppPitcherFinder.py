import json

batter_names_path = 'Backend/Names/MLB/Batter_Names/batterNames.json'
schedule_path = 'Backend/Schedules/MLB/mlbSchedule.json'

def find_opposing_pitcher(player_name):
    with open(batter_names_path, 'r') as f:
        batter_names = json.load(f)
    
    # Find the player's team URL
    player_team_url = None
    for player in batter_names:
        if player['player_name'] == player_name:
            player_team_url = player['player_team']
            break
    
    if player_team_url is None:
        return None

    with open(schedule_path, 'r') as f:
        schedule = json.load(f)

    # Find the opposing pitcher based on the players team URL
    for game in schedule:
        if game['Away Team'] == player_team_url:
            return game['Home Pitcher']
        elif game['Home Team'] == player_team_url:
            return game['Away Pitcher']

    return None

# Example usage
if __name__ == "__main__":
    player_name = "Javier Baez"
    position = "batter"
    result = find_opposing_pitcher(player_name, position)
    print(result)
