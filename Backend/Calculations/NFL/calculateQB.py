import subprocess
import ast
import sys
import math
import json

def calculate_qb_data(primary_full_url, opp_full_url, over_under, percent_threshold, game_threshold):
    script_path_qb_pass_tds = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/NFL/QB/scrapeQBpassTDs.py'
    script_path_qb_pass_yds = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/NFL/QB/scrapeQBpassYards.py'
    script_path_qb_rush_yds = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/NFL/QB/scrapeQBrushYards.py'
    script_path_team_pass_tds = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/NFL/Teams/scrapeTeamPassTDs.py'
    script_path_team_pass_yds = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/NFL/Teams/scrapeTeamPassYds.py'
    script_path_team_rush_yds = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/NFL/Teams/scrapeTeamRushYds.py'

    result_qb_pass_tds, result_qb_pass_yds, result_qb_rush_yds, result_team_pass_tds, result_team_pass_yds, result_team_rush_yds = [], [], [], [], [], []

    result_qb_pass_tds = subprocess.run(['python3', script_path_qb_pass_tds, primary_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_qb_pass_yds = subprocess.run(['python3', script_path_qb_pass_yds, primary_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_qb_rush_yds = subprocess.run(['python3', script_path_qb_rush_yds, primary_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_pass_tds = subprocess.run(['python3', script_path_team_pass_tds, opp_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_pass_yds = subprocess.run(['python3', script_path_team_pass_yds, opp_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_rush_yds = subprocess.run(['python3', script_path_team_rush_yds, opp_full_url, game_threshold], capture_output=True, text=True).stdout.strip()

    # Convert results to lists
    try:
        if result_qb_pass_tds:
            result_qb_pass_tds = ast.literal_eval(result_qb_pass_tds)
        if result_qb_pass_yds:
            result_qb_pass_yds = ast.literal_eval(result_qb_pass_yds)
        if result_qb_rush_yds:
            result_qb_rush_yds = ast.literal_eval(result_qb_rush_yds)
        if result_team_pass_tds:
            result_team_pass_tds = ast.literal_eval(result_team_pass_tds)
        if result_team_pass_yds:
            result_team_pass_yds = ast.literal_eval(result_team_pass_yds)
        if result_team_rush_yds:
            result_team_rush_yds = ast.literal_eval(result_team_rush_yds)

        # Finds length of returned QB and team lists
        qb_pass_tds_length = len(result_qb_pass_tds)
        qb_pass_yds_length = len(result_qb_pass_yds)
        qb_rush_yds_length = len(result_qb_rush_yds)
        team_pass_tds_length = len(result_team_pass_tds)
        team_pass_yds_length = len(result_team_pass_yds)
        team_rush_yds_length = len(result_team_rush_yds)
        # Finding position number that is percent_threshold the way through the list (70% through list of 10 is the 7th position (0-9 #'s))
        team_pass_tds_index = int(team_pass_tds_length * percent_threshold)
        team_pass_yds_index = int(team_pass_yds_length * percent_threshold)
        team_rush_yds_index = int(team_rush_yds_length * percent_threshold)
        qb_pass_tds_index = int(qb_pass_tds_length * percent_threshold)
        qb_pass_yds_index = int(qb_pass_yds_length * percent_threshold)
        qb_rush_yds_index = int(qb_rush_yds_length * percent_threshold)

        # Change HTML percentage input to float and a decimal
        percent_threshold = (float(percent_threshold)) / 100

        # Calculate Over probabilities for all stat categories
        if over_under == 'over':
            # Over Passing TDs

            # Sorting list of team pass TDs allowed (largest to smallest)
            team_pass_tds_sorted = sorted(result_team_pass_tds, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_pass_tds_over_variable = team_pass_tds_sorted[team_pass_tds_index]
            # Repaeats previous steps for QB
            qb_pass_tds_sorted = sorted(result_qb_pass_tds, reverse=True)
            qb_pass_tds_over_variable = qb_pass_tds_sorted[qb_pass_tds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_pass_tds_over_variable = math.floor(min(team_pass_tds_over_variable, qb_pass_tds_over_variable))

            def calculate_pass_tds_over_percentage(stat_number):
                # Finds # of times QB pass TDs greater than or equal to the final_over_variable
                qb_pass_tds_over_count = sum(1 for TDs in result_qb_pass_tds if TDs >= (final_pass_tds_over_variable + stat_number))
                # Finds % times QB pass TDs greater than or equal to the final_over_variable out of qb_pass_tds_length
                qb_pass_tds_over_percentage = (qb_pass_tds_over_count / qb_pass_tds_length) if qb_pass_tds_length else 0
                qb_pass_tds_over_percentage = (qb_pass_tds_over_percentage * 100)
                return qb_pass_tds_over_percentage
            
            # Final result for prime probability
            if final_pass_tds_over_variable - .5 > 0:
                qb_pass_tds_over_percentage = calculate_pass_tds_over_percentage(0)
                qb_pass_tds_percentage = f"{qb_pass_tds_over_percentage:.1f}%"
                final_pass_tds_variable = f"o{final_pass_tds_over_variable - .5}"
            else:
                final_pass_tds_variable = ''
                qb_pass_tds_percentage = ''

            # Final result for prime probability -2
            if final_pass_tds_over_variable - 2.5 > 0:
                qb_pass_tds_over_percentage = calculate_pass_tds_over_percentage(-2)
                qb_pass_tds_percentage1 = f"{qb_pass_tds_over_percentage:.1f}%"
                final_pass_tds_variable1 = f"o{final_pass_tds_over_variable - 2.5}"
            else:
                final_pass_tds_variable1 = ''
                qb_pass_tds_percentage1 = ''

            # Final result for prime probability -1
            if final_pass_tds_over_variable - 1.5 > 0:
                qb_pass_tds_over_percentage = calculate_pass_tds_over_percentage(-1)
                qb_pass_tds_percentage2 = f"{qb_pass_tds_over_percentage:.1f}%"
                final_pass_tds_variable2 = f"o{final_pass_tds_over_variable - 1.5}"
            else:
                final_pass_tds_variable2 = ''
                qb_pass_tds_percentage2 = ''

            # Final result for prime probability +1
            if final_pass_tds_over_variable + .5 > 0:
                qb_pass_tds_over_percentage = calculate_pass_tds_over_percentage(1)
                qb_pass_tds_percentage3 = f"{qb_pass_tds_over_percentage:.1f}%"
                final_pass_tds_variable3 = f"o{final_pass_tds_over_variable + .5}"
            else:
                final_pass_tds_variable3 = ''
                qb_pass_tds_percentage3 = ''

            # Final result for prime probability +2
            if final_pass_tds_over_variable + 1.5 > 0:
                qb_pass_tds_over_percentage = calculate_pass_tds_over_percentage(2)
                qb_pass_tds_percentage4 = f"{qb_pass_tds_over_percentage:.1f}%"
                final_pass_tds_variable4 = f"o{final_pass_tds_over_variable + 1.5}"
            else:
                final_pass_tds_variable4 = ''
                qb_pass_tds_percentage4 = ''

            # Over Pass Yards
            
            # Sorting list of team pass YDs allowed (largest to smallest)
            team_pass_yds_sorted = sorted(result_team_pass_yds, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_pass_yds_over_variable = team_pass_yds_sorted[team_pass_yds_index]
            # Repaeats previous steps for QB
            qb_pass_yds_sorted = sorted(result_qb_pass_yds, reverse=True)
            qb_pass_yds_over_variable = qb_pass_yds_sorted[qb_pass_yds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            min_pass_yds_over_variable = math.floor(min(team_pass_yds_over_variable, qb_pass_yds_over_variable))
            final_pass_yds_over_variable = math.floor(min_pass_yds_over_variable / 25) * 25

            def calculate_pass_yds_over_percentage(stat_number):
                # Finds # of times QB pass YDs greater than or equal to the final_over_variable
                qb_pass_yds_over_count = sum(1 for pass_yards in result_qb_pass_yds if pass_yards >= (final_pass_yds_over_variable + stat_number))
                # Finds % times QB pass YDs greater than or equal to the final_over_variable out of qb_pass_yds_length
                qb_pass_yds_over_percentage = (qb_pass_yds_over_count / qb_pass_yds_length) if qb_pass_yds_length else 0
                qb_pass_yds_over_percentage = (qb_pass_yds_over_percentage * 100)
                return qb_pass_yds_over_percentage
            
            # Final result for prime probability
            if final_pass_yds_over_variable - .5 > 0:
                qb_pass_yds_over_percentage = calculate_pass_yds_over_percentage(0)
                qb_pass_yds_percentage = f"{qb_pass_yds_over_percentage:.1f}%"
                final_pass_yds_variable = f"o{final_pass_yds_over_variable - .5}"
            else:
                final_pass_yds_variable = ''
                qb_pass_yds_percentage = ''

            # Final result for prime probability -2
            if final_pass_yds_over_variable - 50.5 > 0:
                qb_pass_yds_over_percentage = calculate_pass_yds_over_percentage(-50)
                qb_pass_yds_percentage1 = f"{qb_pass_yds_over_percentage:.1f}%"
                final_pass_yds_variable1 = f"o{final_pass_yds_over_variable - 50.5}"
            else:
                final_pass_yds_variable1 = ''
                qb_pass_yds_percentage1 = ''

            # Final result for prime probability -1
            if final_pass_yds_over_variable - 25.5 > 0:
                qb_pass_yds_over_percentage = calculate_pass_yds_over_percentage(-25)
                qb_pass_yds_percentage2 = f"{qb_pass_yds_over_percentage:.1f}%"
                final_pass_yds_variable2 = f"o{final_pass_yds_over_variable - 25.5}"
            else:
                final_pass_yds_variable2 = ''
                qb_pass_yds_percentage2 = ''

            # Final result for prime probability +1
            if final_pass_yds_over_variable + 24.5 > 0:
                qb_pass_yds_over_percentage = calculate_pass_yds_over_percentage(25)
                qb_pass_yds_percentage3 = f"{qb_pass_yds_over_percentage:.1f}%"
                final_pass_yds_variable3 = f"o{final_pass_yds_over_variable + 24.5}"
            else:
                final_pass_yds_variable3 = ''
                qb_pass_yds_percentage3 = ''

            # Final result for prime probability +2
            if final_pass_yds_over_variable + 49.5 > 0:
                qb_pass_yds_over_percentage = calculate_pass_yds_over_percentage(50)
                qb_pass_yds_percentage4 = f"{qb_pass_yds_over_percentage:.1f}%"
                final_pass_yds_variable4 = f"o{final_pass_yds_over_variable + 49.5}"
            else:
                final_pass_yds_variable4 = ''
                qb_pass_yds_percentage4 = ''

            # Over Rush Yards

            # Sorting list of team rush YDs allowed (largest to smallest)
            team_rush_yds_sorted = sorted(result_team_rush_yds, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_rush_yds_over_variable = team_rush_yds_sorted[team_rush_yds_index]
            # Repaeats previous steps for QB
            qb_rush_yds_sorted = sorted(result_qb_rush_yds, reverse=True)
            qb_rush_yds_over_variable = qb_rush_yds_sorted[qb_rush_yds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            min_rush_yds_over_variable = math.floor(min(team_rush_yds_over_variable, qb_rush_yds_over_variable))
            if min_rush_yds_over_variable < 25:
                final_rush_yds_over_variable = 25
            else:
                final_rush_yds_over_variable = math.floor(min_rush_yds_over_variable / 10) * 10

            def calculate_rush_yds_over_percentage(stat_number):
                # Finds # of times QB rush YDs greater than or equal to the final_over_variable
                qb_rush_yds_over_count = sum(1 for rush_yards in result_qb_rush_yds if rush_yards >= (final_rush_yds_over_variable + stat_number))
                # Finds % times QB rush YDs greater than or equal to the final_over_variable out of qb_rush_yds_length
                qb_rush_yds_over_percentage = (qb_rush_yds_over_count / qb_rush_yds_length) if qb_rush_yds_length else 0
                qb_rush_yds_over_percentage = (qb_rush_yds_over_percentage * 100)
                return qb_rush_yds_over_percentage
            
            # Final result for prime probability
            if final_rush_yds_over_variable - .5 > 0:
                qb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(0)
                qb_rush_yds_percentage = f"{qb_rush_yds_over_percentage:.1f}%"
                final_rush_yds_variable = f"o{final_rush_yds_over_variable - .5}"
                if qb_rush_yds_over_percentage < (percent_threshold * 100):
                    final_rush_yds_variable = ''
                    qb_rush_yds_percentage = ''
            else:
                final_rush_yds_variable = ''
                qb_rush_yds_percentage = ''

            # Final result for prime probability -2
            if final_rush_yds_over_variable - 20.5 > 0:
                qb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(-20)
                qb_rush_yds_percentage1 = f"{qb_rush_yds_over_percentage:.1f}%"
                final_rush_yds_variable1 = f"o{final_rush_yds_over_variable - 20.5}"
                
            else:
                final_rush_yds_variable1 = ''
                qb_rush_yds_percentage1 = ''

            # Final result for prime probability -1
            if final_rush_yds_over_variable - 10.5 > 0:
                qb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(-10)
                qb_rush_yds_percentage2 = f"{qb_rush_yds_over_percentage:.1f}%"
                final_rush_yds_variable2 = f"o{final_rush_yds_over_variable - 10.5}"
                
            else:
                final_rush_yds_variable2 = ''
                qb_rush_yds_percentage2 = ''

            # Final result for prime probability +1
            if final_rush_yds_over_variable + 9.5 > 0:
                if final_rush_yds_over_variable == 25:
                    qb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(15)
                    final_rush_yds_variable3 = f"o{final_rush_yds_over_variable + 14.5}"
                else:
                    qb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(10)
                    final_rush_yds_variable3 = f"o{final_rush_yds_over_variable + 9.5}"
                qb_rush_yds_percentage3 = f"{qb_rush_yds_over_percentage:.1f}%"
            else:
                final_rush_yds_variable3 = ''
                qb_rush_yds_percentage3 = ''

            # Final result for prime probability +2
            if final_rush_yds_over_variable + 19.5 > 0:
                if final_rush_yds_over_variable == 25:
                    qb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(25)
                    final_rush_yds_variable4 = f"o{final_rush_yds_over_variable + 24.5}"
                else:
                    qb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(20)
                    final_rush_yds_variable4 = f"o{final_rush_yds_over_variable + 19.5}"
                qb_rush_yds_percentage4 = f"{qb_rush_yds_over_percentage:.1f}%"
            else:
                final_rush_yds_variable4 = ''
                qb_rush_yds_percentage4 = ''

        # Calculate UNDER probabilities for all stat categories
        elif over_under == 'under':
            # under Passing TDs

            # Sorting list of team pass TDs allowed (smallest to largest)
            team_pass_tds_sorted = sorted(result_team_pass_tds, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_pass_tds_under_variable = team_pass_tds_sorted[team_pass_tds_index]
            # Repaeats previous steps for QB
            qb_pass_tds_sorted = sorted(result_qb_pass_tds, reverse=False)
            qb_pass_tds_under_variable = qb_pass_tds_sorted[qb_pass_tds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_pass_tds_under_variable = math.ceil(max(team_pass_tds_under_variable, qb_pass_tds_under_variable))

            def calculate_pass_tds_under_percentage(stat_number):
                # Finds # of times QB pass TDs less than or equal to the final_under_variable
                qb_pass_tds_under_count = sum(1 for TDs in result_qb_pass_tds if TDs <= (final_pass_tds_under_variable + stat_number))
                # Finds % times QB pass TDs less than or equal to the final_under_variable out of qb_pass_tds_length
                qb_pass_tds_under_percentage = (qb_pass_tds_under_count / qb_pass_tds_length) if qb_pass_tds_length else 0
                qb_pass_tds_under_percentage = (qb_pass_tds_under_percentage * 100)
                return qb_pass_tds_under_percentage
            
            # Final result for prime probability
            if final_pass_tds_under_variable + .5 > 0:
                qb_pass_tds_under_percentage = calculate_pass_tds_under_percentage(0)
                qb_pass_tds_percentage = f"{qb_pass_tds_under_percentage:.1f}%"
                final_pass_tds_variable = f"u{final_pass_tds_under_variable + .5}"
            else:
                final_pass_tds_variable = ''
                qb_pass_tds_percentage = ''

            # Final result for prime probability -2
            if final_pass_tds_under_variable - 1.5 > 0:
                qb_pass_tds_under_percentage = calculate_pass_tds_under_percentage(-2)
                qb_pass_tds_percentage1 = f"{qb_pass_tds_under_percentage:.1f}%"
                final_pass_tds_variable1 = f"u{final_pass_tds_under_variable - 1.5}"
            else:
                final_pass_tds_variable1 = ''
                qb_pass_tds_percentage1 = ''

            # Final result for prime probability -1
            if final_pass_tds_under_variable - .5 > 0:
                qb_pass_tds_under_percentage = calculate_pass_tds_under_percentage(-1)
                qb_pass_tds_percentage2 = f"{qb_pass_tds_under_percentage:.1f}%"
                final_pass_tds_variable2 = f"u{final_pass_tds_under_variable - .5}"
            else:
                final_pass_tds_variable2 = ''
                qb_pass_tds_percentage2 = ''

            # Final result for prime probability +1
            if final_pass_tds_under_variable + 1.5 > 0:
                qb_pass_tds_under_percentage = calculate_pass_tds_under_percentage(1)
                qb_pass_tds_percentage3 = f"{qb_pass_tds_under_percentage:.1f}%"
                final_pass_tds_variable3 = f"u{final_pass_tds_under_variable + 1.5}"
            else:
                final_pass_tds_variable3 = ''
                qb_pass_tds_percentage3 = ''

            # Final result for prime probability +2
            if final_pass_tds_under_variable + 2.5 > 0:
                qb_pass_tds_under_percentage = calculate_pass_tds_under_percentage(2)
                qb_pass_tds_percentage4 = f"{qb_pass_tds_under_percentage:.1f}%"
                final_pass_tds_variable4 = f"u{final_pass_tds_under_variable + 2.5}"
            else:
                final_pass_tds_variable4 = ''
                qb_pass_tds_percentage4 = ''


            # under Pass Yards
            
            # Sorting list of team pass YDs allowed (smallest to largest)
            team_pass_yds_sorted = sorted(result_team_pass_yds, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_pass_yds_under_variable = team_pass_yds_sorted[team_pass_yds_index]
            # Repaeats previous steps for QB
            qb_pass_yds_sorted = sorted(result_qb_pass_yds, reverse=False)
            qb_pass_yds_under_variable = qb_pass_yds_sorted[qb_pass_yds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            max_pass_yds_under_variable = math.ceil(max(team_pass_yds_under_variable, qb_pass_yds_under_variable))
            final_pass_yds_under_variable = math.floor(max_pass_yds_under_variable / 25) * 25

            def calculate_pass_yds_under_percentage(stat_number):
                # Finds # of times QB pass YDs less than or equal to the final_under_variable
                qb_pass_yds_under_count = sum(1 for pass_yards in result_qb_pass_yds if pass_yards <= (final_pass_yds_under_variable + stat_number))
                # Finds % times QB pass YDs less than or equal to the final_under_variable out of qb_pass_yds_length
                qb_pass_yds_under_percentage = (qb_pass_yds_under_count / qb_pass_yds_length) if qb_pass_yds_length else 0
                qb_pass_yds_under_percentage = (qb_pass_yds_under_percentage * 100)
                return qb_pass_yds_under_percentage
            
            # Final result for prime probability
            if final_pass_yds_under_variable + .5 > 0:
                qb_pass_yds_under_percentage = calculate_pass_yds_under_percentage(0)
                qb_pass_yds_percentage = f"{qb_pass_yds_under_percentage:.1f}%"
                final_pass_yds_variable = f"u{final_pass_yds_under_variable + .5}"
            else:
                final_pass_yds_variable = ''
                qb_pass_yds_percentage = ''

            # Final result for prime probability -2
            if final_pass_yds_under_variable - 49.5 > 0:
                qb_pass_yds_under_percentage = calculate_pass_yds_under_percentage(-50)
                qb_pass_yds_percentage1 = f"{qb_pass_yds_under_percentage:.1f}%"
                final_pass_yds_variable1 = f"u{final_pass_yds_under_variable - 49.5}"
            else:
                final_pass_yds_variable1 = ''
                qb_pass_yds_percentage1 = ''

            # Final result for prime probability -1
            if final_pass_yds_under_variable - 24.5 > 0:
                qb_pass_yds_under_percentage = calculate_pass_yds_under_percentage(-25)
                qb_pass_yds_percentage2 = f"{qb_pass_yds_under_percentage:.1f}%"
                final_pass_yds_variable2 = f"u{final_pass_yds_under_variable - 24.5}"
            else:
                final_pass_yds_variable2 = ''
                qb_pass_yds_percentage2 = ''

            # Final result for prime probability +1
            if final_pass_yds_under_variable + 25.5 > 0:
                qb_pass_yds_under_percentage = calculate_pass_yds_under_percentage(25)
                qb_pass_yds_percentage3 = f"{qb_pass_yds_under_percentage:.1f}%"
                final_pass_yds_variable3 = f"u{final_pass_yds_under_variable + 25.5}"
            else:
                final_pass_yds_variable3 = ''
                qb_pass_yds_percentage3 = ''

            # Final result for prime probability +2
            if final_pass_yds_under_variable + 50.5 > 0:
                qb_pass_yds_under_percentage = calculate_pass_yds_under_percentage(50)
                qb_pass_yds_percentage4 = f"{qb_pass_yds_under_percentage:.1f}%"
                final_pass_yds_variable4 = f"u{final_pass_yds_under_variable + 50.5}"
            else:
                final_pass_yds_variable4 = ''
                qb_pass_yds_percentage4 = ''

            # under Rush Yards

            # Sorting list of QB rush YDs allowed (smallest to largest)
            qb_rush_yds_sorted = sorted(result_qb_rush_yds, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            qb_rush_yds_under_variable = qb_rush_yds_sorted[qb_rush_yds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            max_rush_yds_under_variable = qb_rush_yds_under_variable
            final_rush_yds_under_variable = math.floor(max_rush_yds_under_variable / 10) * 10

            def calculate_rush_yds_under_percentage(stat_number):
                # Finds # of times QB rush YDs less than or equal to the final_under_variable
                qb_rush_yds_under_count = sum(1 for rush_yards in result_qb_rush_yds if rush_yards <= (final_rush_yds_under_variable + stat_number))
                # Finds % times QB rush YDs less than or equal to the final_under_variable out of qb_rush_yds_length
                qb_rush_yds_under_percentage = (qb_rush_yds_under_count / qb_rush_yds_length) if qb_rush_yds_length else 0
                qb_rush_yds_under_percentage = (qb_rush_yds_under_percentage * 100)
                return qb_rush_yds_under_percentage
            
            # Final result for prime probability
            if final_rush_yds_under_variable + .5 > 0:
                qb_rush_yds_under_percentage = calculate_rush_yds_under_percentage(0)
                qb_rush_yds_percentage = f"{qb_rush_yds_under_percentage:.1f}%"
                final_rush_yds_variable = f"u{final_rush_yds_under_variable + .5}"
                if qb_rush_yds_under_percentage < (percent_threshold * 100):
                    final_rush_yds_variable = ''
                    qb_rush_yds_percentage = ''
            else:
                final_rush_yds_variable = ''
                qb_rush_yds_percentage = ''

            # Final result for prime probability -2
            if final_rush_yds_under_variable - 19.5 > 0:
                qb_rush_yds_under_percentage = calculate_rush_yds_under_percentage(-20)
                qb_rush_yds_percentage1 = f"{qb_rush_yds_under_percentage:.1f}%"
                final_rush_yds_variable1 = f"u{final_rush_yds_under_variable - 19.5}"
            else:
                final_rush_yds_variable1 = ''
                qb_rush_yds_percentage1 = ''

            # Final result for prime probability -1
            if final_rush_yds_under_variable - 9.5 > 0:
                qb_rush_yds_under_percentage = calculate_rush_yds_under_percentage(-10)
                qb_rush_yds_percentage2 = f"{qb_rush_yds_under_percentage:.1f}%"
                final_rush_yds_variable2 = f"u{final_rush_yds_under_variable - 9.5}"
            else:
                final_rush_yds_variable2 = ''
                qb_rush_yds_percentage2 = ''

            # Final result for prime probability +1
            if final_rush_yds_under_variable + 10.5 > 0:
                qb_rush_yds_under_percentage = calculate_rush_yds_under_percentage(10)
                qb_rush_yds_percentage3 = f"{qb_rush_yds_under_percentage:.1f}%"
                final_rush_yds_variable3 = f"u{final_rush_yds_under_variable + 10.5}"
            else:
                final_rush_yds_variable3 = ''
                qb_rush_yds_percentage3 = ''

            # Final result for prime probability +2
            if final_rush_yds_under_variable + 20.5 > 0:
                qb_rush_yds_under_percentage = calculate_rush_yds_under_percentage(20)
                qb_rush_yds_percentage4 = f"{qb_rush_yds_under_percentage:.1f}%"
                final_rush_yds_variable4 = f"u{final_rush_yds_under_variable + 20.5}"
            else:
                final_rush_yds_variable4 = ''
                qb_rush_yds_percentage4 = ''

    except (ValueError, SyntaxError) as e:
        print(f"Data Conversion Error: {e}")

    results = {
        'PassTDs': {
            'percentage': qb_pass_tds_percentage,
            'final_variable': final_pass_tds_variable,
            'percentage1': qb_pass_tds_percentage1,
            'final_variable1': final_pass_tds_variable1,
            'percentage2': qb_pass_tds_percentage2,
            'final_variable2': final_pass_tds_variable2,
            'percentage3': qb_pass_tds_percentage3,
            'final_variable3': final_pass_tds_variable3,
            'percentage4': qb_pass_tds_percentage4,
            'final_variable4': final_pass_tds_variable4,
        },
        'PassYards': {
            'percentage': qb_pass_yds_percentage,
            'final_variable': final_pass_yds_variable,
            'percentage1': qb_pass_yds_percentage1,
            'final_variable1': final_pass_yds_variable1,
            'percentage2': qb_pass_yds_percentage2,
            'final_variable2': final_pass_yds_variable2,
            'percentage3': qb_pass_yds_percentage3,
            'final_variable3': final_pass_yds_variable3,
            'percentage4': qb_pass_yds_percentage4,
            'final_variable4': final_pass_yds_variable4,
        },
        'RushYards': {
            'percentage': qb_rush_yds_percentage,
            'final_variable': final_rush_yds_variable,
            'percentage1': qb_rush_yds_percentage1,
            'final_variable1': final_rush_yds_variable1,
            'percentage2': qb_rush_yds_percentage2,
            'final_variable2': final_rush_yds_variable2,
            'percentage3': qb_rush_yds_percentage3,
            'final_variable3': final_rush_yds_variable3,
            'percentage4': qb_rush_yds_percentage4,
            'final_variable4': final_rush_yds_variable4,
        }
    }

    return json.dumps(results)

if __name__ == '__main__':
    primary_full_url = sys.argv[1]
    opp_full_url = sys.argv[2]
    over_under = sys.argv[3]
    percent_threshold = sys.argv[4]
    game_threshold = sys.argv[5]

    result = calculate_qb_data(primary_full_url, opp_full_url, over_under, percent_threshold, game_threshold)
    print(result)
