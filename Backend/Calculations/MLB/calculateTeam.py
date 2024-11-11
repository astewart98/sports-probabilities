import subprocess
import ast
import sys
import math
import json
from pathlib import Path

def calculate_team_data(primary_full_url, opp_full_url, over_under, percent_threshold, team_min_game_threshold):
    base_dir = Path(__file__).resolve().parent

    script_path_team_runs = base_dir / '../../Scraped_Data/MLB/Teams/scrapeTeamRuns.py'
    script_path_team_RA = base_dir / '../../Scraped_Data/MLB/Teams/scrapeTeamRA.py'

    script_path_team_runs = str(script_path_team_runs)
    script_path_team_RA = str(script_path_team_RA)

    result_team_runs, result_team_RA, result_opp_team_runs, result_opp_team_RA = [], [], [], []

    result_team_runs = subprocess.run(['python3', script_path_team_runs, primary_full_url, team_min_game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_RA = subprocess.run(['python3', script_path_team_RA, primary_full_url, team_min_game_threshold], capture_output=True, text=True).stdout.strip()
    result_opp_team_runs = subprocess.run(['python3', script_path_team_runs, opp_full_url, team_min_game_threshold], capture_output=True, text=True).stdout.strip()
    result_opp_team_RA = subprocess.run(['python3', script_path_team_RA, opp_full_url, team_min_game_threshold], capture_output=True, text=True).stdout.strip()

    # Convert results to lists
    try:
        if result_team_runs:
            result_team_runs = ast.literal_eval(result_team_runs)
        if result_team_RA:
            result_team_RA = ast.literal_eval(result_team_RA)
        if result_opp_team_runs:
            result_opp_team_runs = ast.literal_eval(result_opp_team_runs)
        if result_opp_team_RA:
            result_opp_team_RA = ast.literal_eval(result_opp_team_RA)

        # Change HTML percentage input to float and a decimal
        percent_threshold = (float(percent_threshold)) / 100

        # Finds length of returned teams lists
        team_runs_length = len(result_team_runs)
        team_RA_length = len(result_team_RA)
        opp_team_RA_length = len(result_opp_team_RA)
        opp_team_runs_length = len(result_opp_team_runs)
        # Finding position number that is percent_threshold the way through the list (70% through list of 10 is the 7th position (0-9 #'s))
        opp_team_RA_index = int(opp_team_RA_length * percent_threshold)
        opp_team_total_runs_index = int(opp_team_total_length * percent_threshold)
        team_runs_index = int(team_runs_length * percent_threshold)
        team_total_runs_index = int(team_total_length * percent_threshold)

        # Calculate winner probabability (MONEYLINE)
        
        team_avg_runs = sum(result_team_runs) / team_runs_length
        team_avg_RA = sum(result_team_RA) / team_RA_length
        opp_team_avg_RA = sum(result_opp_team_RA) / opp_team_RA_length
        opp_team_avg_runs = sum(result_opp_team_runs) / opp_team_runs_length

        # NO IF STATEMENTS BECAUSE NO O/U
        # Weighted = averaged against other team
        team_weighted_runs = (team_avg_runs + opp_team_avg_RA) / 2
        opp_team_weighted_runs = (opp_team_avg_runs + team_avg_RA) / 2

        if team_weighted_runs > opp_team_weighted_runs:

            winner = "Primary Team"
            winner_percentage = "Winner"

        elif team_weighted_runs < opp_team_weighted_runs:

            winner = "Opposing Team"
            winner_percentage = "Winner"

        # Calculate O/U probabilities for individual runs
        if over_under == 'over':

            # Sorting list of opp team runs allowed (largest to smallest)
            opp_team_RA_sorted = sorted(result_opp_team_RA, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            opp_team_RA_over_variable = opp_team_RA_sorted[opp_team_RA_index]
            # Repaeats previous steps for primary team
            team_runs_sorted = sorted(result_team_runs, reverse=True)
            team_runs_over_variable = team_runs_sorted[team_runs_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_runs_over_variable = math.floor(min(opp_team_RA_over_variable, team_runs_over_variable))

            def calculate_team_runs_over_percentage(stat_number):
                # Finds # of times team runs greater than or equal to the final_over_variable
                team_runs_over_count = sum(1 for run in result_team_runs if run >= (final_runs_over_variable + stat_number))
                # Finds % times team runs greater than or equal to the final_over_variable out of team_runs_length
                team_runs_over_percentage = (team_runs_over_count / team_runs_length) if team_runs_length else 0
                team_runs_over_percentage = (team_runs_over_percentage * 100)
                return team_runs_over_percentage
            
            # Final result for prime probability
            if final_runs_over_variable - .5 > 0:
                team_runs_over_percentage = calculate_team_runs_over_percentage(0)
                individual_runs_percentage = f"{team_runs_over_percentage:.1f}%"
                final_individual_runs_variable = f"o{final_runs_over_variable - .5}"
            else:
                final_individual_runs_variable = ''
                individual_runs_percentage = ''

            # Final result for prime probability -2
            if final_runs_over_variable - 2.5 > 0:
                team_runs_over_percentage = calculate_team_runs_over_percentage(-2)
                individual_runs_percentage1 = f"{team_runs_over_percentage:.1f}%"
                final_individual_runs_variable1 = f"o{final_runs_over_variable - 2.5}"
            else:
                final_individual_runs_variable1 = ''
                individual_runs_percentage1 = ''
            # Final result for prime probability -1
            if final_runs_over_variable - 1.5 > 0:
                team_runs_over_percentage = calculate_team_runs_over_percentage(-1)
                individual_runs_percentage2 = f"{team_runs_over_percentage:.1f}%"
                final_individual_runs_variable2 = f"o{final_runs_over_variable - 1.5}"
            else:
                final_individual_runs_variable2 = ''
                individual_runs_percentage2 = ''
            # Final result for prime probability +1
            if final_runs_over_variable + .5 > 0:
                team_runs_over_percentage = calculate_team_runs_over_percentage(1)
                individual_runs_percentage3 = f"{team_runs_over_percentage:.1f}%"
                final_individual_runs_variable3 = f"o{final_runs_over_variable + .5}"
            else:
                final_individual_runs_variable3 = ''
                individual_runs_percentage3 = ''
            # Final result for prime probability +2
            if final_runs_over_variable + 1.5 > 0:
                team_runs_over_percentage = calculate_team_runs_over_percentage(2)
                individual_runs_percentage4 = f"{team_runs_over_percentage:.1f}%"
                final_individual_runs_variable4 = f"o{final_runs_over_variable + 1.5}"
            else:
                final_individual_runs_variable4 = ''
                individual_runs_percentage4 = ''

        elif over_under == 'under':
            
            # Sorting list of pitcher hits allowed (smallest to largest)
            opp_team_RA_sorted = sorted(result_opp_team_RA, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            opp_team_RA_under_variable = opp_team_RA_sorted[opp_team_RA_index]
            # Repaeats previous steps for primary team
            team_runs_sorted = sorted(result_team_runs, reverse=False)
            team_runs_under_variable = team_runs_sorted[team_runs_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_runs_under_variable = math.ceil(max(opp_team_RA_under_variable, team_runs_under_variable))

            
            def calculate_team_runs_under_percentage(stat_number):
                # Finds # of times team runs less than or equal to the final_under_variable
                team_runs_under_count = sum(1 for run in result_team_runs if run <= (final_runs_under_variable + stat_number))
                # Finds % times team runs less than or equal to the final_under_variable out of team_runs_length
                team_runs_under_percentage = (team_runs_under_count / team_runs_length) if team_runs_length else 0
                team_runs_under_percentage = (team_runs_under_percentage * 100)
                return team_runs_under_percentage
            
            # Final result for prime probability
            if final_runs_under_variable + .5 > 0:
                team_runs_under_percentage = calculate_team_runs_under_percentage(0)
                individual_runs_percentage = f"{team_runs_under_percentage:.1f}%"
                final_individual_runs_variable = f"u{final_runs_under_variable + .5}"
            else:
                final_individual_runs_variable = ''
                individual_runs_percentage = ''
            
            # Final result for prime probability -2
            if final_runs_under_variable - 1.5 > 0:
                team_runs_under_percentage = calculate_team_runs_under_percentage(-2)
                individual_runs_percentage1 = f"{team_runs_under_percentage:.1f}%"
                final_individual_runs_variable1 = f"u{final_runs_under_variable - 1.5}"
            else:
                final_individual_runs_variable1 = ''
                individual_runs_percentage1 = ''
            # Final result for prime probability -1
            if final_runs_under_variable - .5 > 0:
                team_runs_under_percentage = calculate_team_runs_under_percentage(-1)
                individual_runs_percentage2 = f"{team_runs_under_percentage:.1f}%"
                final_individual_runs_variable2 = f"u{final_runs_under_variable - .5}"
            else:
                final_individual_runs_variable2 = ''
                individual_runs_percentage2 = ''
            # Final result for prime probability +1
            if final_runs_under_variable + 1.5 > 0:
                team_runs_under_percentage = calculate_team_runs_under_percentage(1)
                individual_runs_percentage3 = f"{team_runs_under_percentage:.1f}%"
                final_individual_runs_variable3 = f"u{final_runs_under_variable + 1.5}"
            else:
                final_individual_runs_variable3 = ''
                individual_runs_percentage3 = ''
            # Final result for prime probability +2
            if final_runs_under_variable + 2.5 > 0:
                team_runs_under_percentage = calculate_team_runs_under_percentage(2)
                individual_runs_percentage4 = f"{team_runs_under_percentage:.1f}%"
                final_individual_runs_variable4 = f"u{final_runs_under_variable + 2.5}"
            else:
                final_individual_runs_variable4 = ''
                individual_runs_percentage4 = ''


        # Calculate O/U probabilities for total runs
        team_total_runs_RA = [runs + ra for runs, ra in zip(result_team_runs, result_team_RA)]
        opp_team_total_runs_RA = [runs + ra for runs, ra in zip(result_opp_team_runs, result_opp_team_RA)]
        opp_team_total_length = len(opp_team_total_runs_RA)
        team_total_length = len(team_total_runs_RA)

        if over_under == 'over':

            # Sorting list of opp team total runs allowed (largest to smallest)
            opp_team_total_runs_sorted = sorted(opp_team_total_runs_RA, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            opp_team_total_runs_over_variable = opp_team_total_runs_sorted[opp_team_total_runs_index]
            # Repaeats previous steps for primary team
            team_total_runs_sorted = sorted(team_total_runs_RA, reverse=True)
            team_total_runs_over_variable = team_total_runs_sorted[team_total_runs_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_total_runs_over_variable = math.floor(min(opp_team_total_runs_over_variable, team_total_runs_over_variable))

            
            def calculate_total_runs_over_percentage(stat_number):
                # Percent times "total Runs" stat number has happened to opp team
                opp_team_total_over_count = sum(1 for run in opp_team_total_runs_RA if run >= (final_total_runs_over_variable + stat_number))
                opp_team_total_over_percentage = (opp_team_total_over_count / opp_team_total_length * 100) if opp_team_total_length else 0
                # Percent times "total Runs" stat number has happened to team
                team_total_over_count = sum(1 for run in team_total_runs_RA if run >= (final_total_runs_over_variable + stat_number))
                team_total_over_percentage = (team_total_over_count / team_total_length * 100) if team_total_length else 0
                # Picking lowest percentage between opp team and team
                lowest_over_percentage = min(opp_team_total_over_percentage, team_total_over_percentage)
                return lowest_over_percentage

            # Final result for prime probability
            if final_total_runs_over_variable - .5 > 0:
                lowest_over_percentage = calculate_total_runs_over_percentage(0)
                total_runs_percentage = f"{lowest_over_percentage:.1f}%"
                final_total_runs_variable = f"o{final_total_runs_over_variable - .5}"
            else:
                final_total_runs_variable = ''
                total_runs_percentage = ''

            # Final result for prime probability
            if final_total_runs_over_variable - 2.5 > 0:
                lowest_over_percentage = calculate_total_runs_over_percentage(-2)
                total_runs_percentage1 = f"{lowest_over_percentage:.1f}%"
                final_total_runs_variable1 = f"o{final_total_runs_over_variable - 2.5}"
            else:
                final_total_runs_variable1 = ''
                total_runs_percentage1 = ''

            # Final result for prime probability
            if final_total_runs_over_variable - 1.5 > 0:
                lowest_over_percentage = calculate_total_runs_over_percentage(-1)
                total_runs_percentage2 = f"{lowest_over_percentage:.1f}%"
                final_total_runs_variable2 = f"o{final_total_runs_over_variable - 1.5}"
            else:
                final_total_runs_variable2 = ''
                total_runs_percentage2 = ''

            # Final result for prime probability
            if final_total_runs_over_variable + .5 > 0:
                lowest_over_percentage = calculate_total_runs_over_percentage(1)
                total_runs_percentage3 = f"{lowest_over_percentage:.1f}%"
                final_total_runs_variable3 = f"o{final_total_runs_over_variable + .5}"
            else:
                final_total_runs_variable3 = ''
                total_runs_percentage3 = ''

            # Final result for prime probability
            if final_runs_over_variable + 1.5 > 0:
                lowest_over_percentage = calculate_total_runs_over_percentage(2)
                total_runs_percentage4 = f"{lowest_over_percentage:.1f}%"
                final_total_runs_variable4 = f"o{final_total_runs_over_variable + 1.5}"
            else:
                final_total_runs_variable4 = ''
                total_runs_percentage4 = ''
                
        if over_under == 'under':

            # Sorting list of opp team total runs allowed (smallest to largest)
            opp_team_total_runs_sorted = sorted(opp_team_total_runs_RA, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            opp_team_total_runs_under_variable = opp_team_total_runs_sorted[opp_team_total_runs_index]
            # Repaeats previous steps for primary team
            team_total_runs_sorted = sorted(team_total_runs_RA, reverse=False)
            team_total_runs_under_variable = team_total_runs_sorted[team_total_runs_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_total_runs_under_variable = math.ceil(max(opp_team_total_runs_under_variable, team_total_runs_under_variable))

            
            def calculate_total_runs_under_percentage(stat_number):
                # Percent times "total Runs" stat number has happened to opp team
                opp_team_total_under_count = sum(1 for run in opp_team_total_runs_RA if run <= (final_total_runs_under_variable + stat_number))
                opp_team_total_under_percentage = (opp_team_total_under_count / opp_team_total_length * 100) if opp_team_total_length else 0
                # Percent times "total Runs" stat number has happened to team
                team_total_under_count = sum(1 for run in team_total_runs_RA if run <= (final_total_runs_under_variable + stat_number))
                team_total_under_percentage = (team_total_under_count / team_total_length * 100) if team_total_length else 0
                # Picking lowest percentage between opp team and team
                lowest_under_percentage = min(opp_team_total_under_percentage, team_total_under_percentage)
                return lowest_under_percentage

            # Final result for prime probability
            if final_total_runs_under_variable + .5 > 0:
                lowest_under_percentage = calculate_total_runs_under_percentage(0)
                total_runs_percentage = f"{lowest_under_percentage:.1f}%"
                final_total_runs_variable = f"u{final_total_runs_under_variable + .5}"
            else:
                final_total_runs_variable = ''
                total_runs_percentage = ''

            # Final result for prime probability
            if final_total_runs_under_variable - 1.5 > 0:
                lowest_under_percentage = calculate_total_runs_under_percentage(-2)
                total_runs_percentage1 = f"{lowest_under_percentage:.1f}%"
                final_total_runs_variable1 = f"u{final_total_runs_under_variable - 1.5}"
            else:
                final_total_runs_variable1 = ''
                total_runs_percentage1 = ''

            # Final result for prime probability
            if final_total_runs_under_variable - .5 > 0:
                lowest_under_percentage = calculate_total_runs_under_percentage(-1)
                total_runs_percentage2 = f"{lowest_under_percentage:.1f}%"
                final_total_runs_variable2 = f"u{final_total_runs_under_variable - .5}"
            else:
                final_total_runs_variable2 = ''
                total_runs_percentage2 = ''

            # Final result for prime probability
            if final_total_runs_under_variable + 1.5 > 0:
                lowest_under_percentage = calculate_total_runs_under_percentage(1)
                total_runs_percentage3 = f"{lowest_under_percentage:.1f}%"
                final_total_runs_variable3 = f"u{final_total_runs_under_variable + 1.5}"
            else:
                final_total_runs_variable3 = ''
                total_runs_percentage3 = ''

            # Final result for prime probability
            if final_total_runs_under_variable + 2.5 > 0:
                lowest_under_percentage = calculate_total_runs_under_percentage(2)
                total_runs_percentage4 = f"{lowest_under_percentage:.1f}%"
                final_total_runs_variable4 = f"u{final_total_runs_under_variable + 2.5}"
            else:
                final_total_runs_variable4 = ''
                total_runs_percentage4 = ''

    except (ValueError, SyntaxError) as e:
        print(f"Data Conversion Error: {e}")

    results = {
        'Individual Runs': {
            'percentage': individual_runs_percentage,
            'final_variable': final_individual_runs_variable,
            'percentage1': individual_runs_percentage1,
            'final_variable1': final_individual_runs_variable1,
            'percentage2': individual_runs_percentage2,
            'final_variable2': final_individual_runs_variable2,
            'percentage3': individual_runs_percentage3,
            'final_variable3': final_individual_runs_variable3,
            'percentage4': individual_runs_percentage4,
            'final_variable4': final_individual_runs_variable4,
        },
        'Total Runs': {
            'percentage': total_runs_percentage,
            'final_variable': final_total_runs_variable,
            'percentage1': total_runs_percentage1,
            'final_variable1': final_total_runs_variable1,
            'percentage2': total_runs_percentage2,
            'final_variable2': final_total_runs_variable2,
            'percentage3': total_runs_percentage3,
            'final_variable3': final_total_runs_variable3,
            'percentage4': total_runs_percentage4,
            'final_variable4': final_total_runs_variable4,
        },
        'Moneyline': {
            'winner_percentage': winner_percentage,
            'winner': winner
        }
    }

    return json.dumps(results)

if __name__ == '__main__':
    primary_full_url = sys.argv[1]
    opp_full_url = sys.argv[2]
    over_under = sys.argv[3]
    percent_threshold = sys.argv[4]
    team_min_game_threshold = sys.argv[5]

    result = calculate_team_data(primary_full_url, opp_full_url, over_under, percent_threshold, team_min_game_threshold)
    print(result)
