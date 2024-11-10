import subprocess
import ast
import sys
import math
import json

def calculate_team_data(primary_full_url, opp_full_url, over_under, percent_threshold, game_threshold):
    script_path_team_points_for = 'Backend/Scraped_Data/NFL/Teams/scrapeTeamPointsFor.py'
    script_path_team_points_against = 'Backend/Scraped_Data/NFL/Teams/scrapeTeamPointsAgainst.py'

    result_team_points_for, result_team_points_against, result_opp_team_points_for, result_opp_team_points_against = [], [], [], []

    result_team_points_for = subprocess.run(['python3', script_path_team_points_for, primary_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_points_against = subprocess.run(['python3', script_path_team_points_against, primary_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_opp_team_points_for = subprocess.run(['python3', script_path_team_points_for, opp_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_opp_team_points_against = subprocess.run(['python3', script_path_team_points_against, opp_full_url, game_threshold], capture_output=True, text=True).stdout.strip()

    # Convert results to lists
    try:
        if result_team_points_for:
            result_team_points_for = ast.literal_eval(result_team_points_for)
        if result_team_points_against:
            result_team_points_against = ast.literal_eval(result_team_points_against)
        if result_opp_team_points_for:
            result_opp_team_points_for = ast.literal_eval(result_opp_team_points_for)
        if result_opp_team_points_against:
            result_opp_team_points_against = ast.literal_eval(result_opp_team_points_against)

        # Change HTML percentage input to float and a decimal
        percent_threshold = (float(percent_threshold)) / 100

        # Finds length of returned teams lists
        team_points_for_length = len(result_team_points_for)
        team_points_against_length = len(result_team_points_against)
        opp_team_points_against_length = len(result_opp_team_points_against)
        opp_team_points_for_length = len(result_opp_team_points_for)
        # Finding position number that is percent_threshold the way through the list (70% through list of 10 is the 7th position (0-9 #'s))
        opp_team_points_against_index = int(opp_team_points_against_length * percent_threshold)
        opp_team_total_points_for_index = int(opp_team_total_length * percent_threshold)
        team_points_for_index = int(team_points_for_length * percent_threshold)
        team_total_points_for_index = int(team_total_length * percent_threshold)

        # Calculate winner probabability (MONEYLINE)

        team_avg_points_for = sum(result_team_points_for) / team_points_for_length
        team_avg_points_against = sum(result_team_points_against) / team_points_against_length
        opp_team_avg_points_against = sum(result_opp_team_points_against) / opp_team_points_against_length
        opp_team_avg_points_for = sum(result_opp_team_points_for) / opp_team_points_for_length

        # NO IF STATEMENTS BECAUSE NO O/U
        # Weighted = averaged against other team
        team_weighted_points_for = (team_avg_points_for + opp_team_avg_points_against) / 2
        opp_team_weighted_points_for = (opp_team_avg_points_for + team_avg_points_against) / 2

        if team_weighted_points_for > opp_team_weighted_points_for:

            winner = "Primary Team"
            winner_percentage = "Winner"

        elif team_weighted_points_for < opp_team_weighted_points_for:

            winner = "Opposing Team"
            winner_percentage = "Winner"

        # Calculate O/U probabilities for individual points
        if over_under == 'over':

            # Sorting list of opp team points allowed (largest to smallest)
            opp_team_points_against_sorted = sorted(result_opp_team_points_against, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            opp_team_points_against_over_variable = opp_team_points_against_sorted[opp_team_points_against_index]
            # Repaeats previous steps for primary team
            team_points_for_sorted = sorted(result_team_points_for, reverse=True)
            team_points_for_over_variable = team_points_for_sorted[team_points_for_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_points_for_over_variable = math.floor(min(opp_team_points_against_over_variable, team_points_for_over_variable))

            def calculate_team_points_for_over_percentage(stat_number):
                # Finds # of times team points greater than or equal to the final_over_variable
                team_points_for_over_count = sum(1 for run in result_team_points_for if run >= (final_points_for_over_variable + stat_number))
                # Finds % times team points greater than or equal to the final_over_variable out of team_points_for_length
                team_points_for_over_percentage = (team_points_for_over_count / team_points_for_length) if team_points_for_length else 0
                team_points_for_over_percentage = (team_points_for_over_percentage * 100)
                return team_points_for_over_percentage
            
            # Final result for prime probability
            if final_points_for_over_variable - .5 > 0:
                team_points_for_over_percentage = calculate_team_points_for_over_percentage(0)
                individual_points_for_percentage = f"{team_points_for_over_percentage:.1f}%"
                final_individual_points_for_variable = f"o{final_points_for_over_variable - .5}"
            else:
                final_individual_points_for_variable = ''
                individual_points_for_percentage = ''

            # Final result for prime probability -2
            if final_points_for_over_variable - 2.5 > 0:
                team_points_for_over_percentage = calculate_team_points_for_over_percentage(-2)
                individual_points_for_percentage1 = f"{team_points_for_over_percentage:.1f}%"
                final_individual_points_for_variable1 = f"o{final_points_for_over_variable - 2.5}"
            else:
                final_individual_points_for_variable1 = ''
                individual_points_for_percentage1 = ''
            # Final result for prime probability -1
            if final_points_for_over_variable - 1.5 > 0:
                team_points_for_over_percentage = calculate_team_points_for_over_percentage(-1)
                individual_points_for_percentage2 = f"{team_points_for_over_percentage:.1f}%"
                final_individual_points_for_variable2 = f"o{final_points_for_over_variable - 1.5}"
            else:
                final_individual_points_for_variable2 = ''
                individual_points_for_percentage2 = ''
            # Final result for prime probability +1
            if final_points_for_over_variable + .5 > 0:
                team_points_for_over_percentage = calculate_team_points_for_over_percentage(1)
                individual_points_for_percentage3 = f"{team_points_for_over_percentage:.1f}%"
                final_individual_points_for_variable3 = f"o{final_points_for_over_variable + .5}"
            else:
                final_individual_points_for_variable3 = ''
                individual_points_for_percentage3 = ''
            # Final result for prime probability +2
            if final_points_for_over_variable + 1.5 > 0:
                team_points_for_over_percentage = calculate_team_points_for_over_percentage(2)
                individual_points_for_percentage4 = f"{team_points_for_over_percentage:.1f}%"
                final_individual_points_for_variable4 = f"o{final_points_for_over_variable + 1.5}"
            else:
                final_individual_points_for_variable4 = ''
                individual_points_for_percentage4 = ''

        elif over_under == 'under':
            
            # Sorting list of opp team points allowed (smallest to largest)
            opp_team_points_against_sorted = sorted(result_opp_team_points_against, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            opp_team_points_against_under_variable = opp_team_points_against_sorted[opp_team_points_against_index]
            # Repaeats previous steps for primary team
            team_points_for_sorted = sorted(result_team_points_for, reverse=False)
            team_points_for_under_variable = team_points_for_sorted[team_points_for_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_points_for_under_variable = math.ceil(max(opp_team_points_against_under_variable, team_points_for_under_variable))
            
            def calculate_team_points_for_under_percentage(stat_number):
                # Finds # of times team points for less than or equal to the final_under_variable
                team_points_for_under_count = sum(1 for run in result_team_points_for if run <= (final_points_for_under_variable + stat_number))
                # Finds % times team points for less than or equal to the final_under_variable out of team_points_for_length
                team_points_for_under_percentage = (team_points_for_under_count / team_points_for_length) if team_points_for_length else 0
                team_points_for_under_percentage = (team_points_for_under_percentage * 100)
                return team_points_for_under_percentage
            
            # Final result for prime probability
            if final_points_for_under_variable + .5 > 0:
                team_points_for_under_percentage = calculate_team_points_for_under_percentage(0)
                individual_points_for_percentage = f"{team_points_for_under_percentage:.1f}%"
                final_individual_points_for_variable = f"u{final_points_for_under_variable + .5}"
            else:
                final_individual_points_for_variable = ''
                individual_points_for_percentage = ''
            
            # Final result for prime probability -2
            if final_points_for_under_variable - 1.5 > 0:
                team_points_for_under_percentage = calculate_team_points_for_under_percentage(-2)
                individual_points_for_percentage1 = f"{team_points_for_under_percentage:.1f}%"
                final_individual_points_for_variable1 = f"u{final_points_for_under_variable - 1.5}"
            else:
                final_individual_points_for_variable1 = ''
                individual_points_for_percentage1 = ''
            # Final result for prime probability -1
            if final_points_for_under_variable - .5 > 0:
                team_points_for_under_percentage = calculate_team_points_for_under_percentage(-1)
                individual_points_for_percentage2 = f"{team_points_for_under_percentage:.1f}%"
                final_individual_points_for_variable2 = f"u{final_points_for_under_variable - .5}"
            else:
                final_individual_points_for_variable2 = ''
                individual_points_for_percentage2 = ''
            # Final result for prime probability +1
            if final_points_for_under_variable + 1.5 > 0:
                team_points_for_under_percentage = calculate_team_points_for_under_percentage(1)
                individual_points_for_percentage3 = f"{team_points_for_under_percentage:.1f}%"
                final_individual_points_for_variable3 = f"u{final_points_for_under_variable + 1.5}"
            else:
                final_individual_points_for_variable3 = ''
                individual_points_for_percentage3 = ''
            # Final result for prime probability +2
            if final_points_for_under_variable + 2.5 > 0:
                team_points_for_under_percentage = calculate_team_points_for_under_percentage(2)
                individual_points_for_percentage4 = f"{team_points_for_under_percentage:.1f}%"
                final_individual_points_for_variable4 = f"u{final_points_for_under_variable + 2.5}"
            else:
                final_individual_points_for_variable4 = ''
                individual_points_for_percentage4 = ''


        # Calculate O/U probabilities for total points
        team_total_points_for_points_against = [points_for + ra for points_for, ra in zip(result_team_points_for, result_team_points_against)]
        opp_team_total_points_for_points_against = [points_for + ra for points_for, ra in zip(result_opp_team_points_for, result_opp_team_points_against)]
        opp_team_total_length = len(opp_team_total_points_for_points_against)
        team_total_length = len(team_total_points_for_points_against)
        if over_under == 'over':

            # Sorting list of opp team total points for (largest to smallest)
            opp_team_total_points_for_sorted = sorted(opp_team_total_points_for_points_against, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            opp_team_total_points_for_over_variable = opp_team_total_points_for_sorted[opp_team_total_points_for_index]
            # Repaeats previous steps for primary team
            team_total_points_for_sorted = sorted(team_total_points_for_points_against, reverse=True)
            team_total_points_for_over_variable = team_total_points_for_sorted[team_total_points_for_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_total_points_for_over_variable = math.floor(min(opp_team_total_points_for_over_variable, team_total_points_for_over_variable))
            
            def calculate_total_points_for_over_percentage(stat_number):
                # Percent times "total points" stat number has happened to opp team
                opp_team_total_over_count = sum(1 for run in opp_team_total_points_for_points_against if run >= (final_total_points_for_over_variable + stat_number))
                opp_team_total_over_percentage = (opp_team_total_over_count / opp_team_total_length * 100) if opp_team_total_length else 0
                # Percent times "total points" stat number has happened to team
                team_total_over_count = sum(1 for run in team_total_points_for_points_against if run >= (final_total_points_for_over_variable + stat_number))
                team_total_over_percentage = (team_total_over_count / team_total_length * 100) if team_total_length else 0
                # Picking lowest percentage between opp team and team
                lowest_over_percentage = min(opp_team_total_over_percentage, team_total_over_percentage)
                return lowest_over_percentage

            # Final result for prime probability
            if final_total_points_for_over_variable - .5 > 0:
                lowest_over_percentage = calculate_total_points_for_over_percentage(0)
                total_points_for_percentage = f"{lowest_over_percentage:.1f}%"
                final_total_points_for_variable = f"o{final_total_points_for_over_variable - .5}"
            else:
                final_total_points_for_variable = ''
                total_points_for_percentage = ''

            # Final result for prime probability
            if final_total_points_for_over_variable - 2.5 > 0:
                lowest_over_percentage = calculate_total_points_for_over_percentage(-2)
                total_points_for_percentage1 = f"{lowest_over_percentage:.1f}%"
                final_total_points_for_variable1 = f"o{final_total_points_for_over_variable - 2.5}"
            else:
                final_total_points_for_variable1 = ''
                total_points_for_percentage1 = ''

            # Final result for prime probability
            if final_total_points_for_over_variable - 1.5 > 0:
                lowest_over_percentage = calculate_total_points_for_over_percentage(-1)
                total_points_for_percentage2 = f"{lowest_over_percentage:.1f}%"
                final_total_points_for_variable2 = f"o{final_total_points_for_over_variable - 1.5}"
            else:
                final_total_points_for_variable2 = ''
                total_points_for_percentage2 = ''

            # Final result for prime probability
            if final_total_points_for_over_variable + .5 > 0:
                lowest_over_percentage = calculate_total_points_for_over_percentage(1)
                total_points_for_percentage3 = f"{lowest_over_percentage:.1f}%"
                final_total_points_for_variable3 = f"o{final_total_points_for_over_variable + .5}"
            else:
                final_total_points_for_variable3 = ''
                total_points_for_percentage3 = ''

            # Final result for prime probability
            if final_points_for_over_variable + 1.5 > 0:
                lowest_over_percentage = calculate_total_points_for_over_percentage(2)
                total_points_for_percentage4 = f"{lowest_over_percentage:.1f}%"
                final_total_points_for_variable4 = f"o{final_total_points_for_over_variable + 1.5}"
            else:
                final_total_points_for_variable4 = ''
                total_points_for_percentage4 = ''
                
        if over_under == 'under':

            # Sorting list of opp team total points for (smallest to largest)
            opp_team_total_points_for_sorted = sorted(opp_team_total_points_for_points_against, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            opp_team_total_points_for_under_variable = opp_team_total_points_for_sorted[opp_team_total_points_for_index]
            # Repaeats previous steps for primary team
            team_total_points_for_sorted = sorted(team_total_points_for_points_against, reverse=False)
            team_total_points_for_under_variable = team_total_points_for_sorted[team_total_points_for_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_total_points_for_under_variable = math.ceil(max(opp_team_total_points_for_under_variable, team_total_points_for_under_variable))
            
            def calculate_total_points_for_under_percentage(stat_number):
                # Percent times "total points" stat number has happened to opp team
                opp_team_total_under_count = sum(1 for run in opp_team_total_points_for_points_against if run <= (final_total_points_for_under_variable + stat_number))
                opp_team_total_under_percentage = (opp_team_total_under_count / opp_team_total_length * 100) if opp_team_total_length else 0
                # Percent times "total points" stat number has happened to team
                team_total_under_count = sum(1 for run in team_total_points_for_points_against if run <= (final_total_points_for_under_variable + stat_number))
                team_total_under_percentage = (team_total_under_count / team_total_length * 100) if team_total_length else 0
                # Picking lowest percentage between opp team and team
                lowest_under_percentage = min(opp_team_total_under_percentage, team_total_under_percentage)
                return lowest_under_percentage

            # Final result for prime probability
            if final_total_points_for_under_variable + .5 > 0:
                lowest_under_percentage = calculate_total_points_for_under_percentage(0)
                total_points_for_percentage = f"{lowest_under_percentage:.1f}%"
                final_total_points_for_variable = f"u{final_total_points_for_under_variable + .5}"
            else:
                final_total_points_for_variable = ''
                total_points_for_percentage = ''

            # Final result for prime probability
            if final_total_points_for_under_variable - 1.5 > 0:
                lowest_under_percentage = calculate_total_points_for_under_percentage(-2)
                total_points_for_percentage1 = f"{lowest_under_percentage:.1f}%"
                final_total_points_for_variable1 = f"u{final_total_points_for_under_variable - 1.5}"
            else:
                final_total_points_for_variable1 = ''
                total_points_for_percentage1 = ''

            # Final result for prime probability
            if final_total_points_for_under_variable - .5 > 0:
                lowest_under_percentage = calculate_total_points_for_under_percentage(-1)
                total_points_for_percentage2 = f"{lowest_under_percentage:.1f}%"
                final_total_points_for_variable2 = f"u{final_total_points_for_under_variable - .5}"
            else:
                final_total_points_for_variable2 = ''
                total_points_for_percentage2 = ''

            # Final result for prime probability
            if final_total_points_for_under_variable + 1.5 > 0:
                lowest_under_percentage = calculate_total_points_for_under_percentage(1)
                total_points_for_percentage3 = f"{lowest_under_percentage:.1f}%"
                final_total_points_for_variable3 = f"u{final_total_points_for_under_variable + 1.5}"
            else:
                final_total_points_for_variable3 = ''
                total_points_for_percentage3 = ''

            # Final result for prime probability
            if final_total_points_for_under_variable + 2.5 > 0:
                lowest_under_percentage = calculate_total_points_for_under_percentage(2)
                total_points_for_percentage4 = f"{lowest_under_percentage:.1f}%"
                final_total_points_for_variable4 = f"u{final_total_points_for_under_variable + 2.5}"
            else:
                final_total_points_for_variable4 = ''
                total_points_for_percentage4 = ''

    except (ValueError, SyntaxError) as e:
        print(f"Data Conversion Error: {e}")

    results = {
        'IndivPoints': {
            'percentage': individual_points_for_percentage,
            'final_variable': final_individual_points_for_variable,
            'percentage1': individual_points_for_percentage1,
            'final_variable1': final_individual_points_for_variable1,
            'percentage2': individual_points_for_percentage2,
            'final_variable2': final_individual_points_for_variable2,
            'percentage3': individual_points_for_percentage3,
            'final_variable3': final_individual_points_for_variable3,
            'percentage4': individual_points_for_percentage4,
            'final_variable4': final_individual_points_for_variable4,
        },
        'TotPoints': {
            'percentage': total_points_for_percentage,
            'final_variable': final_total_points_for_variable,
            'percentage1': total_points_for_percentage1,
            'final_variable1': final_total_points_for_variable1,
            'percentage2': total_points_for_percentage2,
            'final_variable2': final_total_points_for_variable2,
            'percentage3': total_points_for_percentage3,
            'final_variable3': final_total_points_for_variable3,
            'percentage4': total_points_for_percentage4,
            'final_variable4': final_total_points_for_variable4,
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
    game_threshold = sys.argv[5]

    result = calculate_team_data(primary_full_url, opp_full_url, over_under, percent_threshold, game_threshold)
    print(result)
