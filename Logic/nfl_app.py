from flask import Blueprint, request, render_template, redirect, url_for
import subprocess
import os
import sys
import importlib
import json
import base64

nfl_bp = Blueprint('nfl_bp', __name__, url_prefix='/nfl')

# Extract todays schedule
nfl_schedule_script = 'Backend/Schedules/nfl/nflSchedule.py'
subprocess.run(['python3', nfl_schedule_script])

sys.path.append('Backend/Names/NFL/Opp_Finder')
from oppNFLteamFinder import find_opposing_team
sys.path.append('Backend/Scraped_Data/NFL/_URLgenerator')
from urlGeneratorNFLplayer import generate_nfl_player_url
from urlGeneratorNFLteam import generate_team_url

# Extract data from HTML
def handle_nfl_logic(request):
    form_data = {
        'player_name': request.form.get('playername'),
        'year': request.form.get('year'),
        'position': request.form.get('position').strip().lower(),
        'over_under': request.form.get('overunder').lower(),
        'percent_threshold': request.form.get('nfl_percent_threshold'),
        'game_threshold': request.form.get('game_threshold'),
    }

    script_path = ''
    opp_player_name = ''

    player_name = form_data['player_name']
    year = form_data['year']
    position = form_data['position']
    over_under = form_data['over_under']
    percent_threshold= form_data['percent_threshold']
    game_threshold = form_data['game_threshold']

    if position == 'qb':
        script_path = 'Backend/Calculations/NFL/calculateQB.py'
        image_script_path = 'Backend/Scraped_Data/NFL/_Photos/scrapePlayerPhoto.py'
    elif position == 'rb':
        script_path = 'Backend/Calculations/NFL/calculateRB.py'
        image_script_path = 'Backend/Scraped_Data/NFL/_Photos/scrapePlayerPhoto.py'
    elif position == 'team':
        script_path = 'Backend/Calculations/NFL/calculateTeam.py'
        image_script_path = 'Backend/Scraped_Data/NFL/_Photos/scrapeTeamLogo.py'
        team_names_path = 'Backend/Names/NFL/Team_Names/teamCodes.json'
    elif position == 'te':
        script_path = 'Backend/Calculations/NFL/calculateTEWR.py'
        image_script_path = 'Backend/Scraped_Data/NFL/_Photos/scrapePlayerPhoto.py'
    elif position == 'wr':
        script_path = 'Backend/Calculations/NFL/calculateTEWR.py'
        image_script_path = 'Backend/Scraped_Data/NFL/_Photos/scrapePlayerPhoto.py'
    else:
        return render_template('Bet_program2.html', result="Error: Invalid position")
    
    # Generate the player's full URL and find the opposing player/team
    if position == 'qb':
        qb_full_url = generate_nfl_player_url(player_name, year, position)
        opp_player_name = find_opposing_team(player_name, position)
        opp_team_full_url = generate_team_url(opp_player_name, year)
        player_image = subprocess.run(
            ['python3', image_script_path, qb_full_url],
            capture_output=True,
        ).stdout
        player_result = subprocess.run(
            ['python3', script_path, qb_full_url, opp_team_full_url, over_under, percent_threshold, game_threshold],
            capture_output=True,
            text=True
        ).stdout
    elif position == 'rb':
        rb_full_url = generate_nfl_player_url(player_name, year, position)
        opp_player_name = find_opposing_team(player_name, position)
        opp_team_full_url = generate_team_url(opp_player_name, year)
        player_image = subprocess.run(
            ['python3', image_script_path, rb_full_url],
            capture_output=True,
        ).stdout
        player_result = subprocess.run(
            ['python3', script_path, rb_full_url, opp_team_full_url, over_under, percent_threshold, game_threshold],
            capture_output=True,
            text=True
        ).stdout
    elif position == 'team':
        team_full_url = generate_team_url(player_name, year)
        opp_player_name = find_opposing_team(player_name, position)
        opp_team_full_url = generate_team_url(opp_player_name, year)
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
            ['python3', script_path, team_full_url, opp_team_full_url, over_under, percent_threshold, game_threshold],
            capture_output=True,
            text=True
        ).stdout
    elif position == 'te':
        te_full_url = generate_nfl_player_url(player_name, year, position)
        opp_player_name = find_opposing_team(player_name, position)
        opp_team_full_url = generate_team_url(opp_player_name, year)
        player_image = subprocess.run(
            ['python3', image_script_path, te_full_url],
            capture_output=True,
        ).stdout
        player_result = subprocess.run(
            ['python3', script_path, te_full_url, opp_team_full_url, over_under, percent_threshold, game_threshold],
            capture_output=True,
            text=True
        ).stdout
    elif position == 'wr':
        wr_full_url = generate_nfl_player_url(player_name, year, position)
        opp_player_name = find_opposing_team(player_name, position)
        opp_team_full_url = generate_team_url(opp_player_name, year)
        player_image = subprocess.run(
            ['python3', image_script_path, wr_full_url],
            capture_output=True,
        ).stdout
        player_result = subprocess.run(
            ['python3', script_path, wr_full_url, opp_team_full_url, over_under, percent_threshold, game_threshold],
            capture_output=True,
            text=True
        ).stdout
    print(f"Opp Team: {opp_player_name}")

    # Encode the player_result to send to HTML
    encoded_result = base64.b64encode(player_result.encode('utf-8')).decode('utf-8')
    # Redirect to the results page with result
    if position == 'team':
        return redirect(url_for('nfl_bp.display_results', result=encoded_result, player_name=player_name, opp_team_nickname=opp_team_nickname, over_under=over_under, position=position, player_image=player_image))
    else:
        return redirect(url_for('nfl_bp.display_results', result=encoded_result, player_name=player_name, over_under=over_under, position=position, player_image=player_image))
    
@nfl_bp.route('/results')
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
        'qb': {
            'PassTDs': {'name': "Passing TD's", 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                           'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'PassYards': {'name': 'Passing Yards', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                     'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'RushYards': {'name': 'Rushing Yards', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                      'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''}
        },
        'rb': {
            'RushYds': {'name': 'Rushing Yards', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                           'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'RushAtt': {'name': 'Rushes', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                     'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'RecYds': {'name': 'Receiving Yards', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                      'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''}
        },
        'team': {
            'IndivPoints': {'name': 'Individual Points', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                                 'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'TotPoints': {'name': 'Total Points', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                           'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'Moneyline': {'name': 'Moneyline', 'winner_percentage': 0, 'winner': ''}
        },
        'te': {
            'RecYds': {'name': 'Receiving Yards', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                           'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'Receptions': {'name': 'Receptions', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                     'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''}
        },
        'wr': {
            'RecYds': {'name': 'Receiving Yards', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                           'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''},
            'Receptions': {'name': 'Receptions', 'percentage': 0, 'variable': '', 'percentage1': 0, 'variable1': '', 'percentage2': 0, 'variable2': '',
                     'percentage3': 0, 'variable3': '', 'percentage4': 0, 'variable4': ''}
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
    if position == 'qb':
        stat100_name = stats.get("PassTDs", {}).get('name', '')
        stat100_percentage = stats.get("PassTDs", {}).get('percentage', '')
        stat100_variable = stats.get("PassTDs", {}).get('variable', '')
        stat101_percentage = stats.get("PassTDs", {}).get('percentage1', '')
        stat101_variable = stats.get("PassTDs", {}).get('variable1', '')
        stat102_percentage = stats.get("PassTDs", {}).get('percentage2', '')
        stat102_variable = stats.get("PassTDs", {}).get('variable2', '')
        stat103_percentage = stats.get("PassTDs", {}).get('percentage3', '')
        stat103_variable = stats.get("PassTDs", {}).get('variable3', '')
        stat104_percentage = stats.get("PassTDs", {}).get('percentage4', '')
        stat104_variable = stats.get("PassTDs", {}).get('variable4', '')
        stat200_name = stats.get('PassYards', {}).get('name', '')
        stat200_percentage = stats.get('PassYards', {}).get('percentage', '')
        stat200_variable = stats.get('PassYards', {}).get('variable', '')
        stat201_percentage = stats.get('PassYards', {}).get('percentage1', '')
        stat201_variable = stats.get('PassYards', {}).get('variable1', '')
        stat202_percentage = stats.get('PassYards', {}).get('percentage2', '')
        stat202_variable = stats.get('PassYards', {}).get('variable2', '')
        stat203_percentage = stats.get('PassYards', {}).get('percentage3', '')
        stat203_variable = stats.get('PassYards', {}).get('variable3', '')
        stat204_percentage = stats.get('PassYards', {}).get('percentage4', '')
        stat204_variable = stats.get('PassYards', {}).get('variable4', '')
        stat300_name = stats.get('RushYards', {}).get('name', '')
        stat300_percentage = stats.get('RushYards', {}).get('percentage', '')
        stat300_variable = stats.get('RushYards', {}).get('variable', '')
        stat301_percentage = stats.get('RushYards', {}).get('percentage1', '')
        stat301_variable = stats.get('RushYards', {}).get('variable1', '')
        stat302_percentage = stats.get('RushYards', {}).get('percentage2', '')
        stat302_variable = stats.get('RushYards', {}).get('variable2', '')
        stat303_percentage = stats.get('RushYards', {}).get('percentage3', '')
        stat303_variable = stats.get('RushYards', {}).get('variable3', '')
        stat304_percentage = stats.get('RushYards', {}).get('percentage4', '')
        stat304_variable = stats.get('RushYards', {}).get('variable4', '')
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

    elif position == 'rb':
        stat100_name = stats.get('RushYds', {}).get('name', '')
        stat100_percentage = stats.get('RushYds', {}).get('percentage', '')
        stat100_variable = stats.get('RushYds', {}).get('variable', '')
        stat101_percentage = stats.get('RushYds', {}).get('percentage1', '')
        stat101_variable = stats.get('RushYds', {}).get('variable1', '')
        stat102_percentage = stats.get('RushYds', {}).get('percentage2', '')
        stat102_variable = stats.get('RushYds', {}).get('variable2', '')
        stat103_percentage = stats.get('RushYds', {}).get('percentage3', '')
        stat103_variable = stats.get('RushYds', {}).get('variable3', '')
        stat104_percentage = stats.get('RushYds', {}).get('percentage4', '')
        stat104_variable = stats.get('RushYds', {}).get('variable4', '')
        stat200_name = stats.get('RushAtt', {}).get('name', '')
        stat200_percentage = stats.get('RushAtt', {}).get('percentage', '')
        stat200_variable = stats.get('RushAtt', {}).get('variable', '')
        stat201_percentage = stats.get('RushAtt', {}).get('percentage1', '')
        stat201_variable = stats.get('RushAtt', {}).get('variable1', '')
        stat202_percentage = stats.get('RushAtt', {}).get('percentage2', '')
        stat202_variable = stats.get('RushAtt', {}).get('variable2', '')
        stat203_percentage = stats.get('RushAtt', {}).get('percentage3', '')
        stat203_variable = stats.get('RushAtt', {}).get('variable3', '')
        stat204_percentage = stats.get('RushAtt', {}).get('percentage4', '')
        stat204_variable = stats.get('RushAtt', {}).get('variable4', '')
        stat300_name = stats.get('RecYds', {}).get('name', '')
        stat300_percentage = stats.get('RecYds', {}).get('percentage', '')
        stat300_variable = stats.get('RecYds', {}).get('variable', '')
        stat301_percentage = stats.get('RecYds', {}).get('percentage1', '')
        stat301_variable = stats.get('RecYds', {}).get('variable1', '')
        stat302_percentage = stats.get('RecYds', {}).get('percentage2', '')
        stat302_variable = stats.get('RecYds', {}).get('variable2', '')
        stat303_percentage = stats.get('RecYds', {}).get('percentage3', '')
        stat303_variable = stats.get('RecYds', {}).get('variable3', '')
        stat304_percentage = stats.get('RecYds', {}).get('percentage4', '')
        stat304_variable = stats.get('RecYds', {}).get('variable4', '')
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
        stat100_name = stats.get('IndivPoints', {}).get('name', '')
        stat100_percentage = stats.get('IndivPoints', {}).get('percentage', '')
        stat100_variable = stats.get('IndivPoints', {}).get('variable', '')
        stat101_percentage = stats.get('IndivPoints', {}).get('percentage1', '')
        stat101_variable = stats.get('IndivPoints', {}).get('variable1', '')
        stat102_percentage = stats.get('IndivPoints', {}).get('percentage2', '')
        stat102_variable = stats.get('IndivPoints', {}).get('variable2', '')
        stat103_percentage = stats.get('IndivPoints', {}).get('percentage3', '')
        stat103_variable = stats.get('IndivPoints', {}).get('variable3', '')
        stat104_percentage = stats.get('IndivPoints', {}).get('percentage4', '')
        stat104_variable = stats.get('IndivPoints', {}).get('variable4', '')
        stat200_name = stats.get('TotPoints', {}).get('name', '')
        stat200_percentage = stats.get('TotPoints', {}).get('percentage', '')
        stat200_variable = stats.get('TotPoints', {}).get('variable', '')
        stat201_percentage = stats.get('TotPoints', {}).get('percentage1', '')
        stat201_variable = stats.get('TotPoints', {}).get('variable1', '')
        stat202_percentage = stats.get('TotPoints', {}).get('percentage2', '')
        stat202_variable = stats.get('TotPoints', {}).get('variable2', '')
        stat203_percentage = stats.get('TotPoints', {}).get('percentage3', '')
        stat203_variable = stats.get('TotPoints', {}).get('variable3', '')
        stat204_percentage = stats.get('TotPoints', {}).get('percentage4', '')
        stat204_variable = stats.get('TotPoints', {}).get('variable4', '')
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

    elif position == 'te':
        stat100_name = stats.get('RecYds', {}).get('name', '')
        stat100_percentage = stats.get('RecYds', {}).get('percentage', '')
        stat100_variable = stats.get('RecYds', {}).get('variable', '')
        stat101_percentage = stats.get('RecYds', {}).get('percentage1', '')
        stat101_variable = stats.get('RecYds', {}).get('variable1', '')
        stat102_percentage = stats.get('RecYds', {}).get('percentage2', '')
        stat102_variable = stats.get('RecYds', {}).get('variable2', '')
        stat103_percentage = stats.get('RecYds', {}).get('percentage3', '')
        stat103_variable = stats.get('RecYds', {}).get('variable3', '')
        stat104_percentage = stats.get('RecYds', {}).get('percentage4', '')
        stat104_variable = stats.get('RecYds', {}).get('variable4', '')
        stat200_name = stats.get('Receptions', {}).get('name', '')
        stat200_percentage = stats.get('Receptions', {}).get('percentage', '')
        stat200_variable = stats.get('Receptions', {}).get('variable', '')
        stat201_percentage = stats.get('Receptions', {}).get('percentage1', '')
        stat201_variable = stats.get('Receptions', {}).get('variable1', '')
        stat202_percentage = stats.get('Receptions', {}).get('percentage2', '')
        stat202_variable = stats.get('Receptions', {}).get('variable2', '')
        stat203_percentage = stats.get('Receptions', {}).get('percentage3', '')
        stat203_variable = stats.get('Receptions', {}).get('variable3', '')
        stat204_percentage = stats.get('Receptions', {}).get('percentage4', '')
        stat204_variable = stats.get('Receptions', {}).get('variable4', '')
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
            'player_name': player_name,
            'over_under': over_under,
            'position': position,
            'player_image': player_image
        }

    elif position == 'wr':
        stat100_name = stats.get('RecYds', {}).get('name', '')
        stat100_percentage = stats.get('RecYds', {}).get('percentage', '')
        stat100_variable = stats.get('RecYds', {}).get('variable', '')
        stat101_percentage = stats.get('RecYds', {}).get('percentage1', '')
        stat101_variable = stats.get('RecYds', {}).get('variable1', '')
        stat102_percentage = stats.get('RecYds', {}).get('percentage2', '')
        stat102_variable = stats.get('RecYds', {}).get('variable2', '')
        stat103_percentage = stats.get('RecYds', {}).get('percentage3', '')
        stat103_variable = stats.get('RecYds', {}).get('variable3', '')
        stat104_percentage = stats.get('RecYds', {}).get('percentage4', '')
        stat104_variable = stats.get('RecYds', {}).get('variable4', '')
        stat200_name = stats.get('Receptions', {}).get('name', '')
        stat200_percentage = stats.get('Receptions', {}).get('percentage', '')
        stat200_variable = stats.get('Receptions', {}).get('variable', '')
        stat201_percentage = stats.get('Receptions', {}).get('percentage1', '')
        stat201_variable = stats.get('Receptions', {}).get('variable1', '')
        stat202_percentage = stats.get('Receptions', {}).get('percentage2', '')
        stat202_variable = stats.get('Receptions', {}).get('variable2', '')
        stat203_percentage = stats.get('Receptions', {}).get('percentage3', '')
        stat203_variable = stats.get('Receptions', {}).get('variable3', '')
        stat204_percentage = stats.get('Receptions', {}).get('percentage4', '')
        stat204_variable = stats.get('Receptions', {}).get('variable4', '')
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
            'player_name': player_name,
            'over_under': over_under,
            'position': position,
            'player_image': player_image
        }

    return render_template('results.html', **context)