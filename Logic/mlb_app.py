from flask import Blueprint, request, render_template, redirect, url_for
import subprocess
import os
import sys
import importlib
import json
import base64

mlb_bp = Blueprint('mlb_bp', __name__, url_prefix='/mlb')

# Extract todays schedule
mlb_schedule_script = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Schedules/MLB/mlbSchedule.py'
subprocess.run(['python3', mlb_schedule_script])

sys.path.append(os.path.join(os.getcwd(), 'Backend', 'Names', 'MLB', 'Opp_Finder'))
sys.path.append(os.path.join(os.getcwd(), 'Backend', 'Scraped_Data', 'MLB', 'URLgenerator'))

import oppPitcherFinder
import oppTeamFinder

# Extract data from HTML
def handle_mlb_logic(request):
    form_data = {
        'player_name': request.form.get('playername').title(),
        'year': request.form.get('year'),
        'position': request.form.get('position').strip().lower(),
        'over_under': request.form.get('overunder').lower(),
        'percent_threshold': request.form.get('mlb_percent_threshold'),
        'opp_pitcher_hits_threshold': request.form.get('opp_pitcher_hits_threshold'),
        'batter_min_game_threshold': request.form.get('batter_min_game_threshold'),
        'pitcher_min_game_threshold': request.form.get('pitcher_min_game_threshold'),
        'team_min_game_threshold': request.form.get('team_min_game_threshold')
    }

    module = None
    module_name = None
    script_path = ''
    opp_player_name = ''

    player_name = form_data['player_name']
    year = form_data['year']
    position = form_data['position']
    over_under = form_data['over_under']
    percent_threshold= form_data['percent_threshold']
    opp_pitcher_hits_threshold = form_data['opp_pitcher_hits_threshold']
    batter_min_game_threshold = form_data['batter_min_game_threshold']
    pitcher_min_game_threshold = form_data['pitcher_min_game_threshold']
    team_min_game_threshold = form_data['team_min_game_threshold']

    if position == 'batter':
        module_name = 'urlGeneratorBatterPitcher'
        script_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Calculations/MLB/calculateBatter.py'
        image_script_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/MLB/Photos/scrapeBatterPitcherPhoto.py'
    elif position == 'pitcher':
        module_name = 'urlGeneratorBatterPitcher'
        team_module_name = 'urlGeneratorTeam'
        script_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Calculations/MLB/calculatePitcher.py'
        image_script_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/MLB/Photos/scrapeBatterPitcherPhoto.py'
        team_module = importlib.import_module(team_module_name)
    elif position == 'team':
        module_name = 'urlGeneratorTeam'
        script_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Calculations/MLB/calculateTeam.py'
        image_script_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/MLB/Photos/scrapeTeamLogo.py'
        team_names_path = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Names/MLB/Team_Names/teamCodes.json'
    else:
        return render_template('Bet_program2.html', result="Error: Invalid position")
    if module_name:
        module = importlib.import_module(module_name)
    else:
        return render_template('Bet_program2.html', result="Error: Invalid position")
    
    # Generate the player's full URL and find the opposing player/team
    if position == 'batter':
        batter_full_url = module.generate_player_url(player_name, year, position)
        opp_player_name = oppPitcherFinder.find_opposing_pitcher(player_name)
        opp_pitcher_full_url = module.generate_player_url(opp_player_name, year, 'pitcher')
        player_image = subprocess.run(
            ['python3', image_script_path, batter_full_url],
            capture_output=True,
        ).stdout
        player_result = subprocess.run(
            ['python3', script_path, batter_full_url, opp_pitcher_full_url, over_under, percent_threshold, opp_pitcher_hits_threshold, 
             batter_min_game_threshold, pitcher_min_game_threshold],
            capture_output=True,
            text=True
        ).stdout
    elif position == 'pitcher':
        pitcher_full_url = module.generate_player_url(player_name, year, position)
        opp_player_name = oppTeamFinder.find_opposing_team(player_name, position)
        opp_team_full_url = team_module.generate_player_url(opp_player_name, 'team')
        player_image = subprocess.run(
            ['python3', image_script_path, pitcher_full_url],
            capture_output=True,
        ).stdout
        player_result = subprocess.run(
            ['python3', script_path, pitcher_full_url, opp_team_full_url, over_under, percent_threshold, pitcher_min_game_threshold, team_min_game_threshold],
            capture_output=True,
            text=True
        ).stdout
    elif position == 'team':
        team_full_url = module.generate_player_url(player_name, year)
        opp_player_name = oppTeamFinder.find_opposing_team(player_name, position)
        opp_team_full_url = module.generate_player_url(opp_player_name, position)
        opp_team_nickname = None
        with open(team_names_path, 'r') as file:
            team_names = json.load(file)
        for team, data in team_names.items():
            if data.get('url_segment') == opp_player_name:
                opp_team_nickname = team
        opp_team_nickname = opp_team_nickname
        player_image = subprocess.run(
            ['python3', image_script_path, team_full_url],
            capture_output=True,
        ).stdout
        player_result = subprocess.run(
            ['python3', script_path, team_full_url, opp_team_full_url, over_under, percent_threshold, team_min_game_threshold],
            capture_output=True,
            text=True
        ).stdout
        print(opp_team_nickname)

    # Encode the player_result to send to HTML
    encoded_result = base64.b64encode(player_result.encode('utf-8')).decode('utf-8')
    # Redirect to the results page with result
    if position == 'team':
        return redirect(url_for('mlb_bp.display_results', result=encoded_result, player_name=player_name, opp_team_nickname=opp_team_nickname, over_under=over_under, position=position, player_image=player_image))
    else:
        return redirect(url_for('mlb_bp.display_results', result=encoded_result, player_name=player_name, over_under=over_under, position=position, player_image=player_image))
    
@mlb_bp.route('/results')
def display_results():
    encoded_result = request.args.get('result', None)
    player_name = request.args.get('player_name', '')
    opp_team_nickname = request.args.get('opp_team_nickname', '')
    over_under = request.args.get('over_under', '').capitalize()
    position = request.args.get('position', '').strip().lower()
    player_image = request.args.get('player_image', '')

    print(f"Encoded Player Result: {encoded_result}")
    print(f"Player Name: {player_name}")
    print(f"Over/Under: {over_under}")
    print(f"Position: {position}")
    print(f"Player Image: {player_image}")

    try:
        player_result = base64.b64decode(encoded_result).decode('utf-8')
        results = json.loads(player_result)
    except (base64.binascii.Error, json.JSONDecodeError) as e:
        results = {"error": "Failed to decode JSON", "details": str(e)}

    print(f"Results: {results}")

    statistics_mapping = {
        'batter': {
            'Hits': {'name': 'Hits', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                     'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''}
        },
        'pitcher': {
            'Strikeouts': {'name': 'Strikeouts', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                           'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'Hits': {'name': 'Hits', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                     'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'Walks': {'name': 'Walks', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                      'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''}
        },
        'team': {
            'Individual Runs': {'name': 'Individual Runs', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                                 'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'Total Runs': {'name': 'Total Runs', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                           'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'Moneyline': {'name': 'Moneyline', 'winner_percentage': 0, 'winner': ''}
        }
    }

    stats = statistics_mapping.get(position, {})

    for key, value in results.items():
        if key in stats:
            if key == 'Moneyline':
                stats[key]['winner_percentage'] = value.get('winner_percentage', 'Not Found')
                stats[key]['winner'] = value.get('winner', 'Not Found')
            else:
                stats[key]['percentage'] = value.get('percentage', 'Not Found')
                stats[key]['variable'] = value.get('final_variable', 'Not Found')

                for i in range(1, 5):
                    stats[key][f'percentage{i}'] = value.get(f'percentage{i}', 'Not Found')
                    stats[key][f'variable{i}'] = value.get(f'final_variable{i}', 'Not Found')

            print(f"Processed {key}: {stats[key]}")

    # Define variables
    if position == 'batter':
        stat100_name = stats.get('Hits', {}).get('name', '')
        stat100_percentage = stats.get('Hits', {}).get('percentage', '')
        stat100_variable = stats.get('Hits', {}).get('variable', '')
        stat101_percentage = stats.get('Hits', {}).get('percentage1', '')
        stat101_variable = stats.get('Hits', {}).get('variable1', '')
        stat102_percentage = stats.get('Hits', {}).get('percentage2', '')
        stat102_variable = stats.get('Hits', {}).get('variable2', '')
        stat103_percentage = stats.get('Hits', {}).get('percentage3', '')
        stat103_variable = stats.get('Hits', {}).get('variable3', '')
        stat104_percentage = stats.get('Hits', {}).get('percentage4', '')
        stat104_variable = stats.get('Hits', {}).get('variable4', '')
        context = {
            'stat100_name': stat100_name,
            'stat100_percentage': stat100_percentage,
            'stat100_variable': stat100_variable,
            'stat101_percentage': stat101_percentage,
            'stat101_variable': stat101_variable,
            'stat102_percentage': stat102_percentage,
            'stat102_variable': stat102_variable,
            'stat103_percentage': stat103_percentage,
            'stat103_variable': stat103_variable,
            'stat104_percentage': stat104_percentage,
            'stat104_variable': stat104_variable,
            'player_name': player_name,
            'over_under': over_under,
            'position': position,
            'player_image': player_image
        }

    elif position == 'pitcher':
        stat100_name = stats.get('Strikeouts', {}).get('name', '')
        stat100_percentage = stats.get('Strikeouts', {}).get('percentage', '')
        stat100_variable = stats.get('Strikeouts', {}).get('variable', '')
        stat101_percentage = stats.get('Strikeouts', {}).get('percentage1', '')
        stat101_variable = stats.get('Strikeouts', {}).get('variable1', '')
        stat102_percentage = stats.get('Strikeouts', {}).get('percentage2', '')
        stat102_variable = stats.get('Strikeouts', {}).get('variable2', '')
        stat103_percentage = stats.get('Strikeouts', {}).get('percentage3', '')
        stat103_variable = stats.get('Strikeouts', {}).get('variable3', '')
        stat104_percentage = stats.get('Strikeouts', {}).get('percentage4', '')
        stat104_variable = stats.get('Strikeouts', {}).get('variable4', '')
        stat200_name = stats.get('Hits', {}).get('name', '')
        stat200_percentage = stats.get('Hits', {}).get('percentage', '')
        stat200_variable = stats.get('Hits', {}).get('variable', '')
        stat201_percentage = stats.get('Hits', {}).get('percentage1', '')
        stat201_variable = stats.get('Hits', {}).get('variable1', '')
        stat202_percentage = stats.get('Hits', {}).get('percentage2', '')
        stat202_variable = stats.get('Hits', {}).get('variable2', '')
        stat203_percentage = stats.get('Hits', {}).get('percentage3', '')
        stat203_variable = stats.get('Hits', {}).get('variable3', '')
        stat204_percentage = stats.get('Hits', {}).get('percentage4', '')
        stat204_variable = stats.get('Hits', {}).get('variable4', '')
        stat300_name = stats.get('Walks', {}).get('name', '')
        stat300_percentage = stats.get('Walks', {}).get('percentage', '')
        stat300_variable = stats.get('Walks', {}).get('variable', '')
        stat301_percentage = stats.get('Walks', {}).get('percentage1', '')
        stat301_variable = stats.get('Walks', {}).get('variable1', '')
        stat302_percentage = stats.get('Walks', {}).get('percentage2', '')
        stat302_variable = stats.get('Walks', {}).get('variable2', '')
        stat303_percentage = stats.get('Walks', {}).get('percentage3', '')
        stat303_variable = stats.get('Walks', {}).get('variable3', '')
        stat304_percentage = stats.get('Walks', {}).get('percentage4', '')
        stat304_variable = stats.get('Walks', {}).get('variable4', '')
        context = {
            'stat100_name': stat100_name,
            'stat100_percentage': stat100_percentage,
            'stat100_variable': stat100_variable,
            'stat101_percentage': stat101_percentage,
            'stat101_variable': stat101_variable,
            'stat102_percentage': stat102_percentage,
            'stat102_variable': stat102_variable,
            'stat103_percentage': stat103_percentage,
            'stat103_variable': stat103_variable,
            'stat104_percentage': stat104_percentage,
            'stat104_variable': stat104_variable,
            'stat200_name': stat200_name,
            'stat200_percentage': stat200_percentage,
            'stat200_variable': stat200_variable,
            'stat201_percentage': stat201_percentage,
            'stat201_variable': stat201_variable,
            'stat202_percentage': stat202_percentage,
            'stat202_variable': stat202_variable,
            'stat203_percentage': stat203_percentage,
            'stat203_variable': stat203_variable,
            'stat204_percentage': stat204_percentage,
            'stat204_variable': stat204_variable,
            'stat300_name': stat300_name,
            'stat300_percentage': stat300_percentage,
            'stat300_variable': stat300_variable,
            'stat301_percentage': stat301_percentage,
            'stat301_variable': stat301_variable,
            'stat302_percentage': stat302_percentage,
            'stat302_variable': stat302_variable,
            'stat303_percentage': stat303_percentage,
            'stat303_variable': stat303_variable,
            'stat304_percentage': stat304_percentage,
            'stat304_variable': stat304_variable,
            'player_name': player_name,
            'over_under': over_under,
            'position': position,
            'player_image': player_image
        }

    elif position == 'team':
        stat100_name = stats.get('Individual Runs', {}).get('name', '')
        stat100_percentage = stats.get('Individual Runs', {}).get('percentage', '')
        stat100_variable = stats.get('Individual Runs', {}).get('variable', '')
        stat101_percentage = stats.get('Individual Runs', {}).get('percentage1', '')
        stat101_variable = stats.get('Individual Runs', {}).get('variable1', '')
        stat102_percentage = stats.get('Individual Runs', {}).get('percentage2', '')
        stat102_variable = stats.get('Individual Runs', {}).get('variable2', '')
        stat103_percentage = stats.get('Individual Runs', {}).get('percentage3', '')
        stat103_variable = stats.get('Individual Runs', {}).get('variable3', '')
        stat104_percentage = stats.get('Individual Runs', {}).get('percentage4', '')
        stat104_variable = stats.get('Individual Runs', {}).get('variable4', '')
        stat200_name = stats.get('Total Runs', {}).get('name', '')
        stat200_percentage = stats.get('Total Runs', {}).get('percentage', '')
        stat200_variable = stats.get('Total Runs', {}).get('variable', '')
        stat201_percentage = stats.get('Total Runs', {}).get('percentage1', '')
        stat201_variable = stats.get('Total Runs', {}).get('variable1', '')
        stat202_percentage = stats.get('Total Runs', {}).get('percentage2', '')
        stat202_variable = stats.get('Total Runs', {}).get('variable2', '')
        stat203_percentage = stats.get('Total Runs', {}).get('percentage3', '')
        stat203_variable = stats.get('Total Runs', {}).get('variable3', '')
        stat204_percentage = stats.get('Total Runs', {}).get('percentage4', '')
        stat204_variable = stats.get('Total Runs', {}).get('variable4', '')
        stat300_name = stats.get('Moneyline', {}).get('name', '')
        stat300_percentage = stats.get('Moneyline', {}).get('winner_percentage', '')
        stat300_variable = stats.get('Moneyline', {}).get('winner', '')
        if stat300_variable == "Primary Team":
            stat300_variable = player_name
        elif stat300_variable == "Opposing Team":
            stat300_variable = opp_team_nickname
        stat301_percentage = ''
        stat301_variable = ''
        stat302_percentage = ''
        stat302_variable = ''
        stat303_percentage = ''
        stat303_variable = ''
        stat304_percentage = ''
        stat304_variable = ''
        context = {
            'stat100_name': stat100_name,
            'stat100_percentage': stat100_percentage,
            'stat100_variable': stat100_variable,
            'stat101_percentage': stat101_percentage,
            'stat101_variable': stat101_variable,
            'stat102_percentage': stat102_percentage,
            'stat102_variable': stat102_variable,
            'stat103_percentage': stat103_percentage,
            'stat103_variable': stat103_variable,
            'stat104_percentage': stat104_percentage,
            'stat104_variable': stat104_variable,
            'stat200_name': stat200_name,
            'stat200_percentage': stat200_percentage,
            'stat200_variable': stat200_variable,
            'stat201_percentage': stat201_percentage,
            'stat201_variable': stat201_variable,
            'stat202_percentage': stat202_percentage,
            'stat202_variable': stat202_variable,
            'stat203_percentage': stat203_percentage,
            'stat203_variable': stat203_variable,
            'stat204_percentage': stat204_percentage,
            'stat204_variable': stat204_variable,
            'stat300_name': stat300_name,
            'stat300_percentage': stat300_percentage,
            'stat300_variable': stat300_variable,
            'stat301_percentage': stat301_percentage,
            'stat301_variable': stat301_variable,
            'stat302_percentage': stat302_percentage,
            'stat302_variable': stat302_variable,
            'stat303_percentage': stat303_percentage,
            'stat303_variable': stat303_variable,
            'stat304_percentage': stat304_percentage,
            'stat304_variable': stat304_variable,
            'player_name': player_name,
            'over_under': over_under,
            'position': position,
            'team_image': player_image
        }

    return render_template('results.html', **context)