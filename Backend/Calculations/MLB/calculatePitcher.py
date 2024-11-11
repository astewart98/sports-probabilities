import subprocess
import ast
import sys
import math
import json
from pathlib import Path

def calculate_pitcher_data(primary_full_url, opp_full_url, over_under, percent_threshold, pitcher_min_game_threshold, team_min_game_threshold):
    base_dir = Path(__file__).resolve().parent

    script_path_pitcher_IP = base_dir / '../../Scraped_Data/MLB/Pitchers/scrapePitcherIP.py'
    script_path_pitcher_SO = base_dir / '../../Scraped_Data/MLB/Pitchers/scrapePitcherSO.py'
    script_path_pitcher_hits = base_dir / '../../Scraped_Data/MLB/Pitchers/scrapePitcherHitsAllowed.py'
    script_path_pitcher_walks = base_dir / '../../Scraped_Data/MLB/Pitchers/scrapePitcherWalksAllowed.py'
    script_path_team_SO = base_dir / '../../Scraped_Data/MLB/Teams/scrapeTeamSO.py'
    script_path_team_hits = base_dir / '../../Scraped_Data/MLB/Teams/scrapeTeamHits.py'
    script_path_team_walks = base_dir / '../../Scraped_Data/MLB/Teams/scrapeTeamWalks.py'

    script_path_pitcher_IP = str(script_path_pitcher_IP)
    script_path_pitcher_SO = str(script_path_pitcher_SO)
    script_path_pitcher_hits = str(script_path_pitcher_hits)
    script_path_pitcher_walks = str(script_path_pitcher_walks)
    script_path_team_SO = str(script_path_team_SO)
    script_path_team_hits = str(script_path_team_hits)
    script_path_team_walks = str(script_path_team_walks)

    result_pitcher_IP, result_pitcher_SO, result_pitcher_hits, result_pitcher_walks, result_team_SO, result_team_hits, result_team_walks = [], [], [], [], [], [], []

    result_pitcher_IP = subprocess.run(['python3', script_path_pitcher_IP, primary_full_url, pitcher_min_game_threshold], capture_output=True, text=True).stdout.strip()
    result_pitcher_SO = subprocess.run(['python3', script_path_pitcher_SO, primary_full_url, pitcher_min_game_threshold], capture_output=True, text=True).stdout.strip()
    result_pitcher_hits = subprocess.run(['python3', script_path_pitcher_hits, primary_full_url, pitcher_min_game_threshold], capture_output=True, text=True).stdout.strip()
    result_pitcher_walks = subprocess.run(['python3', script_path_pitcher_walks, primary_full_url, pitcher_min_game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_SO = subprocess.run(['python3', script_path_team_SO, opp_full_url, team_min_game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_hits = subprocess.run(['python3', script_path_team_hits, opp_full_url, team_min_game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_walks = subprocess.run(['python3', script_path_team_walks, opp_full_url, team_min_game_threshold], capture_output=True, text=True).stdout.strip()

    # Convert results to lists
    try:
        if result_pitcher_IP:
            result_pitcher_IP = ast.literal_eval(result_pitcher_IP)
        if result_pitcher_SO:
            result_pitcher_SO = ast.literal_eval(result_pitcher_SO)
        if result_pitcher_hits:
            result_pitcher_hits = ast.literal_eval(result_pitcher_hits)
        if result_pitcher_walks:
            result_pitcher_walks = ast.literal_eval(result_pitcher_walks)
        if result_team_SO:
            result_team_SO = ast.literal_eval(result_team_SO)
        if result_team_hits:
            result_team_hits = ast.literal_eval(result_team_hits)
        if result_team_walks:
            result_team_walks = ast.literal_eval(result_team_walks)

        # Calculate pitcher average IP
        average_pitcher_IP = sum(result_pitcher_IP) / len(result_pitcher_IP) if result_pitcher_IP else 0

        # Adjusts result_team_(stat) to be based on # of IP by the pitcher
        adjusted_result_team_SO = [(number / 9) * average_pitcher_IP for number in result_team_SO]
        adjusted_result_team_hits = [(number / 9) * average_pitcher_IP for number in result_team_hits]
        adjusted_result_team_walks = [(number / 9) * average_pitcher_IP for number in result_team_walks]

        # Change HTML percentage input to float and a decimal
        percent_threshold = (float(percent_threshold)) / 100

        # Finds length of returned pitcher and team lists
        pitcher_SO_length = len(result_pitcher_SO)
        pitcher_hits_length = len(result_pitcher_hits)
        pitcher_walks_length = len(result_pitcher_walks)
        team_SO_length = len(result_team_SO)
        team_hits_length = len(result_team_hits)
        team_walks_length = len(result_team_walks)

        # Finding position number that is percent_threshold the way through the list (70% through list of 10 is the 7th position (0-9 #'s))
        # Strikeouts
        team_SO_index = int(team_SO_length * percent_threshold)
        pitcher_SO_index = int(pitcher_SO_length * percent_threshold)
        # Hits
        team_hits_index = int(team_hits_length * percent_threshold)
        pitcher_hits_index = int(pitcher_hits_length * percent_threshold)
        # Walks
        team_walks_index = int(team_walks_length * percent_threshold)
        pitcher_walks_index = int(pitcher_walks_length * percent_threshold)

        # Calculate Over probabilities for all stat categories
        if over_under == 'over':
            # Over Strikeouts

            # Sorting list of team SO's (largest to smallest)
            team_SO_sorted = sorted(adjusted_result_team_SO, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_SO_over_variable = team_SO_sorted[team_SO_index]
            # Repaeats previous steps for pitcher
            pitcher_SO_sorted = sorted(result_pitcher_SO, reverse=True)
            pitcher_SO_over_variable = pitcher_SO_sorted[pitcher_SO_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_SO_over_variable = math.floor(min(team_SO_over_variable, pitcher_SO_over_variable))

            def calculate_SO_over_percentage(stat_number):
                # Finds # of times pitcher SO greater than or equal to the final_over_variable
                pitcher_SO_over_count = sum(1 for SO in result_pitcher_SO if SO >= (final_SO_over_variable + stat_number))
                # Finds % times pitcher SO greater than or equal to the final_over_variable out of pitcher_SO_length
                pitcher_SO_over_percentage = (pitcher_SO_over_count / pitcher_SO_length) if pitcher_SO_length else 0
                pitcher_SO_over_percentage = (pitcher_SO_over_percentage * 100)
                return pitcher_SO_over_percentage
            
            # Final result for prime probability
            if final_SO_over_variable - .5 > 0:
                pitcher_SO_over_percentage = calculate_SO_over_percentage(0)
                pitcher_SO_percentage = f"{pitcher_SO_over_percentage:.1f}%"
                final_SO_variable = f"o{final_SO_over_variable - .5}"
            else:
                final_SO_variable = ''
                pitcher_SO_percentage = ''

            # Final result for prime probability -2
            if final_SO_over_variable - 2.5 > 0:
                pitcher_SO_over_percentage = calculate_SO_over_percentage(-2)
                pitcher_SO_percentage1 = f"{pitcher_SO_over_percentage:.1f}%"
                final_SO_variable1 = f"o{final_SO_over_variable - 2.5}"
            else:
                final_SO_variable1 = ''
                pitcher_SO_percentage1 = ''

            # Final result for prime probability -1
            if final_SO_over_variable - 1.5 > 0:
                pitcher_SO_over_percentage = calculate_SO_over_percentage(-1)
                pitcher_SO_percentage2 = f"{pitcher_SO_over_percentage:.1f}%"
                final_SO_variable2 = f"o{final_SO_over_variable - 1.5}"
            else:
                final_SO_variable2 = ''
                pitcher_SO_percentage2 = ''

            # Final result for prime probability +1
            if final_SO_over_variable + .5 > 0:
                pitcher_SO_over_percentage = calculate_SO_over_percentage(1)
                pitcher_SO_percentage3 = f"{pitcher_SO_over_percentage:.1f}%"
                final_SO_variable3 = f"o{final_SO_over_variable + .5}"
            else:
                final_SO_variable3 = ''
                pitcher_SO_percentage3 = ''

            # Final result for prime probability +2
            if final_SO_over_variable + 1.5 > 0:
                pitcher_SO_over_percentage = calculate_SO_over_percentage(2)
                pitcher_SO_percentage4 = f"{pitcher_SO_over_percentage:.1f}%"
                final_SO_variable4 = f"o{final_SO_over_variable + 1.5}"
            else:
                final_SO_variable4 = ''
                pitcher_SO_percentage4 = ''

            # Over Hits
            
            # Sorting list of team hits (largest to smallest)
            team_hits_sorted = sorted(adjusted_result_team_hits, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_hits_over_variable = team_hits_sorted[team_hits_index]
            # Repaeats previous steps for pitcher
            pitcher_hits_sorted = sorted(result_pitcher_hits, reverse=True)
            pitcher_hits_over_variable = pitcher_hits_sorted[pitcher_hits_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_hits_over_variable = math.floor(min(team_hits_over_variable, pitcher_hits_over_variable))

            def calculate_hits_over_percentage(stat_number):
                # Finds # of times pitcher allowed hits greater than or equal to the final_over_variable
                pitcher_hits_over_count = sum(1 for hits in result_pitcher_hits if hits >= (final_hits_over_variable + stat_number))
                # Finds % times pitcher allowed hits greater than or equal to the final_over_variable out of pitcher_hits_length
                pitcher_hits_over_percentage = (pitcher_hits_over_count / pitcher_hits_length) if pitcher_hits_length else 0
                pitcher_hits_over_percentage = (pitcher_hits_over_percentage * 100)
                return pitcher_hits_over_percentage
            
            # Final result for prime probability
            if final_hits_over_variable - .5 > 0:
                pitcher_hits_over_percentage = calculate_hits_over_percentage(0)
                pitcher_hits_percentage = f"{pitcher_hits_over_percentage:.1f}%"
                final_hits_variable = f"o{final_hits_over_variable - .5}"
            else:
                final_hits_variable = ''
                pitcher_hits_percentage = ''

            # Final result for prime probability -2
            if final_hits_over_variable - 2.5 > 0:
                pitcher_hits_over_percentage = calculate_hits_over_percentage(-2)
                pitcher_hits_percentage1 = f"{pitcher_hits_over_percentage:.1f}%"
                final_hits_variable1 = f"o{final_hits_over_variable - 2.5}"
            else:
                final_hits_variable1 = ''
                pitcher_hits_percentage1 = ''

            # Final result for prime probability -1
            if final_hits_over_variable - 1.5 > 0:
                pitcher_hits_over_percentage = calculate_hits_over_percentage(-1)
                pitcher_hits_percentage2 = f"{pitcher_hits_over_percentage:.1f}%"
                final_hits_variable2 = f"o{final_hits_over_variable - 1.5}"
            else:
                final_hits_variable2 = ''
                pitcher_hits_percentage2 = ''

            # Final result for prime probability +1
            if final_hits_over_variable + .5 > 0:
                pitcher_hits_over_percentage = calculate_hits_over_percentage(1)
                pitcher_hits_percentage3 = f"{pitcher_hits_over_percentage:.1f}%"
                final_hits_variable3 = f"o{final_hits_over_variable + .5}"
            else:
                final_hits_variable3 = ''
                pitcher_hits_percentage3 = ''

            # Final result for prime probability +2
            if final_hits_over_variable + 1.5 > 0:
                pitcher_hits_over_percentage = calculate_hits_over_percentage(2)
                pitcher_hits_percentage4 = f"{pitcher_hits_over_percentage:.1f}%"
                final_hits_variable4 = f"o{final_hits_over_variable + 1.5}"
            else:
                final_hits_variable4 = ''
                pitcher_hits_percentage4 = ''

            # Over Walks

            # Sorting list of team walks (largest to smallest)
            team_walks_sorted = sorted(adjusted_result_team_walks, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_walks_over_variable = team_walks_sorted[team_walks_index]
            # Repaeats previous steps for pitcher
            pitcher_walks_sorted = sorted(result_pitcher_walks, reverse=True)
            pitcher_walks_over_variable = pitcher_walks_sorted[pitcher_walks_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_walks_over_variable = math.floor(min(team_walks_over_variable, pitcher_walks_over_variable))

            def calculate_walks_over_percentage(stat_number):
                # Finds # of times pitcher allowed walks greater than or equal to the final_over_variable
                pitcher_walks_over_count = sum(1 for walks in result_pitcher_walks if walks >= (final_walks_over_variable + stat_number))
                # Finds % times pitcher allowed walks greater than or equal to the final_over_variable out of pitcher_walks_length
                pitcher_walks_over_percentage = (pitcher_walks_over_count / pitcher_walks_length) if pitcher_walks_length else 0
                pitcher_walks_over_percentage = (pitcher_walks_over_percentage * 100)
                return pitcher_walks_over_percentage
            
            # Final result for prime probability
            if final_walks_over_variable - .5 > 0:
                pitcher_walks_over_percentage = calculate_walks_over_percentage(0)
                pitcher_walks_percentage = f"{pitcher_walks_over_percentage:.1f}%"
                final_walks_variable = f"o{final_walks_over_variable - .5}"
            else:
                final_walks_variable = ''
                pitcher_walks_percentage = ''

            # Final result for prime probability -2
            if final_walks_over_variable - 2.5 > 0:
                pitcher_walks_over_percentage = calculate_walks_over_percentage(-2)
                pitcher_walks_percentage1 = f"{pitcher_walks_over_percentage:.1f}%"
                final_walks_variable1 = f"o{final_walks_over_variable - 2.5}"
            else:
                final_walks_variable1 = ''
                pitcher_walks_percentage1 = ''

            # Final result for prime probability -1
            if final_walks_over_variable - 1.5 > 0:
                pitcher_walks_over_percentage = calculate_walks_over_percentage(-1)
                pitcher_walks_percentage2 = f"{pitcher_walks_over_percentage:.1f}%"
                final_walks_variable2 = f"o{final_walks_over_variable - 1.5}"
            else:
                final_walks_variable2 = ''
                pitcher_walks_percentage2 = ''

            # Final result for prime probability +1
            if final_walks_over_variable + .5 > 0:
                pitcher_walks_over_percentage = calculate_walks_over_percentage(1)
                pitcher_walks_percentage3 = f"{pitcher_walks_over_percentage:.1f}%"
                final_walks_variable3 = f"o{final_walks_over_variable + .5}"
            else:
                final_walks_variable3 = ''
                pitcher_walks_percentage3 = ''

            # Final result for prime probability +2
            if final_walks_over_variable + 1.5 > 0:
                pitcher_walks_over_percentage = calculate_walks_over_percentage(2)
                pitcher_walks_percentage4 = f"{pitcher_walks_over_percentage:.1f}%"
                final_walks_variable4 = f"o{final_walks_over_variable + 1.5}"
            else:
                final_walks_variable4 = ''
                pitcher_walks_percentage4 = ''

        # Calculate Under probabilities for all stat categories
        elif over_under == 'under':
            # Under Strikeouts

            # Sorting list of team SO's (smallest to largest)
            team_SO_sorted = sorted(adjusted_result_team_SO, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_SO_under_variable = team_SO_sorted[team_SO_index]
            # Repaeats previous steps for pitcher
            pitcher_SO_sorted = sorted(result_pitcher_SO, reverse=False)
            pitcher_SO_under_variable = pitcher_SO_sorted[pitcher_SO_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_SO_under_variable = math.ceil(max(team_SO_under_variable, pitcher_SO_under_variable))

            
            def calculate_SO_under_percentage(stat_number):
                # Finds # of times pitcher SO's less than or equal to the final_under_variable
                pitcher_SO_under_count = sum(1 for SO in result_pitcher_SO if SO <= (final_SO_under_variable + stat_number))
                # Finds % times pitcher SO's less than or equal to the final_under_variable out of pitcher_SO_length
                pitcher_SO_under_percentage = (pitcher_SO_under_count / pitcher_SO_length) if pitcher_SO_length else 0
                pitcher_SO_under_percentage = (pitcher_SO_under_percentage * 100)
                return pitcher_SO_under_percentage
            
            # Final result for prime probability
            if final_SO_under_variable + .5 > 0:
                pitcher_SO_under_percentage = calculate_SO_under_percentage(0)
                pitcher_SO_percentage = f"{pitcher_SO_under_percentage:.1f}%"
                final_SO_variable = f"u{final_SO_under_variable + .5}"
            else:
                final_SO_variable = ''
                pitcher_SO_percentage = ''

            # Final result for prime probability -2
            if final_SO_under_variable - 1.5 > 0:
                pitcher_SO_under_percentage = calculate_SO_under_percentage(-2)
                pitcher_SO_percentage1 = f"{pitcher_SO_under_percentage:.1f}%"
                final_SO_variable1 = f"u{final_SO_under_variable - 1.5}"
            else:
                final_SO_variable1 = ''
                pitcher_SO_percentage1 = ''

            # Final result for prime probability -1
            if final_SO_under_variable - .5 > 0:
                pitcher_SO_under_percentage = calculate_SO_under_percentage(-1)
                pitcher_SO_percentage2 = f"{pitcher_SO_under_percentage:.1f}%"
                final_SO_variable2 = f"u{final_SO_under_variable - .5}"
            else:
                final_SO_variable2 = ''
                pitcher_SO_percentage2 = ''

            # Final result for prime probability +1
            if final_SO_under_variable + 1.5 > 0:
                pitcher_SO_under_percentage = calculate_SO_under_percentage(1)
                pitcher_SO_percentage3 = f"{pitcher_SO_under_percentage:.1f}%"
                final_SO_variable3 = f"u{final_SO_under_variable + 1.5}"
            else:
                final_SO_variable3 = ''
                pitcher_SO_percentage3 = ''

            # Final result for prime probability +2
            if final_SO_under_variable + 2.5 > 0:
                pitcher_SO_under_percentage = calculate_SO_under_percentage(2)
                pitcher_SO_percentage4 = f"{pitcher_SO_under_percentage:.1f}%"
                final_SO_variable4 = f"u{final_SO_under_variable + 2.5}"
            else:
                final_SO_variable4 = ''
                pitcher_SO_percentage4 = ''


            # Under Hits
            
            # Sorting list of team hits (smallest to largest)
            team_hits_sorted = sorted(adjusted_result_team_hits, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_hits_under_variable = team_hits_sorted[team_hits_index]
            # Repaeats previous steps for pitcher
            pitcher_hits_sorted = sorted(result_pitcher_hits, reverse=False)
            pitcher_hits_under_variable = pitcher_hits_sorted[pitcher_hits_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_hits_under_variable = math.ceil(max(team_hits_under_variable, pitcher_hits_under_variable))

            
            def calculate_hits_under_percentage(stat_number):
                # Finds # of times pitcher hits allowed less than or equal to the final_under_variable
                pitcher_hits_under_count = sum(1 for hits in result_pitcher_hits if hits <= (final_hits_under_variable + stat_number))
                # Finds % times pitcher hits allowed less than or equal to the final_under_variable out of pitcher_hits_length
                pitcher_hits_under_percentage = (pitcher_hits_under_count / pitcher_hits_length) if pitcher_hits_length else 0
                pitcher_hits_under_percentage = (pitcher_hits_under_percentage * 100)
                return pitcher_hits_under_percentage
            
            # Final result for prime probability
            if final_hits_under_variable + .5 > 0:
                pitcher_hits_under_percentage = calculate_hits_under_percentage(0)
                pitcher_hits_percentage = f"{pitcher_hits_under_percentage:.1f}%"
                final_hits_variable = f"u{final_hits_under_variable + .5}"
            else:
                final_hits_variable = ''
                pitcher_hits_percentage = ''

            # Final result for prime probability -2
            if final_hits_under_variable - 1.5 > 0:
                pitcher_hits_under_percentage = calculate_hits_under_percentage(-2)
                pitcher_hits_percentage1 = f"{pitcher_hits_under_percentage:.1f}%"
                final_hits_variable1 = f"u{final_hits_under_variable - 1.5}"
            else:
                final_hits_variable1 = ''
                pitcher_hits_percentage1 = ''

            # Final result for prime probability -1
            if final_hits_under_variable - .5 > 0:
                pitcher_hits_under_percentage = calculate_hits_under_percentage(-1)
                pitcher_hits_percentage2 = f"{pitcher_hits_under_percentage:.1f}%"
                final_hits_variable2 = f"u{final_hits_under_variable - .5}"
            else:
                final_hits_variable2 = ''
                pitcher_hits_percentage2 = ''

            # Final result for prime probability +1
            if final_hits_under_variable + 1.5 > 0:
                pitcher_hits_under_percentage = calculate_hits_under_percentage(1)
                pitcher_hits_percentage3 = f"{pitcher_hits_under_percentage:.1f}%"
                final_hits_variable3 = f"u{final_hits_under_variable + 1.5}"
            else:
                final_hits_variable3 = ''
                pitcher_hits_percentage3 = ''

            # Final result for prime probability +2
            if final_hits_under_variable + 2.5 > 0:
                pitcher_hits_under_percentage = calculate_hits_under_percentage(2)
                pitcher_hits_percentage4 = f"{pitcher_hits_under_percentage:.1f}%"
                final_hits_variable4 = f"u{final_hits_under_variable + 2.5}"
            else:
                final_hits_variable4 = ''
                pitcher_hits_percentage4 = ''

            # under Walks

            # Sorting list of team walks (smallest to largest)
            team_walks_sorted = sorted(adjusted_result_team_walks, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_walks_under_variable = team_walks_sorted[team_walks_index]
            # Repaeats previous steps for pitcher
            pitcher_walks_sorted = sorted(result_pitcher_walks, reverse=False)
            pitcher_walks_under_variable = pitcher_walks_sorted[pitcher_walks_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_walks_under_variable = math.ceil(max(team_walks_under_variable, pitcher_walks_under_variable))

            
            def calculate_walks_under_percentage(stat_number):
                # Finds # of times pitcher walks allowed less than or equal to the final_under_variable
                pitcher_walks_under_count = sum(1 for walks in result_pitcher_walks if walks <= (final_walks_under_variable + stat_number))
                # Finds % times pitcher walks allowed less than or equal to the final_under_variable out of pitcher_walks_length
                pitcher_walks_under_percentage = (pitcher_walks_under_count / pitcher_walks_length) if pitcher_walks_length else 0
                pitcher_walks_under_percentage = (pitcher_walks_under_percentage * 100)
                return pitcher_walks_under_percentage
            
            # Final result for prime probability
            if final_walks_under_variable + .5 > 0:
                pitcher_walks_under_percentage = calculate_walks_under_percentage(0)
                pitcher_walks_percentage = f"{pitcher_walks_under_percentage:.1f}%"
                final_walks_variable = f"u{final_walks_under_variable + .5}"
            else:
                final_walks_variable = ''
                pitcher_walks_percentage = ''

            # Final result for prime probability -2
            if final_walks_under_variable - 1.5 > 0:
                pitcher_walks_under_percentage = calculate_walks_under_percentage(-2)
                pitcher_walks_percentage1 = f"{pitcher_walks_under_percentage:.1f}%"
                final_walks_variable1 = f"u{final_walks_under_variable - 1.5}"
            else:
                final_walks_variable1 = ''
                pitcher_walks_percentage1 = ''

            # Final result for prime probability -1
            if final_walks_under_variable - .5 > 0:
                pitcher_walks_under_percentage = calculate_walks_under_percentage(-1)
                pitcher_walks_percentage2 = f"{pitcher_walks_under_percentage:.1f}%"
                final_walks_variable2 = f"u{final_walks_under_variable - .5}"
            else:
                final_walks_variable2 = ''
                pitcher_walks_percentage2 = ''

            # Final result for prime probability +1
            if final_walks_under_variable + 1.5 > 0:
                pitcher_walks_under_percentage = calculate_walks_under_percentage(1)
                pitcher_walks_percentage3 = f"{pitcher_walks_under_percentage:.1f}%"
                final_walks_variable3 = f"u{final_walks_under_variable + 1.5}"
            else:
                final_walks_variable3 = ''
                pitcher_walks_percentage3 = ''

            # Final result for prime probability +2
            if final_walks_under_variable + 2.5 > 0:
                pitcher_walks_under_percentage = calculate_walks_under_percentage(2)
                pitcher_walks_percentage4 = f"{pitcher_walks_under_percentage:.1f}%"
                final_walks_variable4 = f"u{final_walks_under_variable + 2.5}"
            else:
                final_walks_variable4 = ''
                pitcher_walks_percentage4 = ''

    except (ValueError, SyntaxError) as e:
        print(f"Data Conversion Error: {e}")

    results = {
        'Strikeouts': {
            'percentage': pitcher_SO_percentage,
            'final_variable': final_SO_variable,
            'percentage1': pitcher_SO_percentage1,
            'final_variable1': final_SO_variable1,
            'percentage2': pitcher_SO_percentage2,
            'final_variable2': final_SO_variable2,
            'percentage3': pitcher_SO_percentage3,
            'final_variable3': final_SO_variable3,
            'percentage4': pitcher_SO_percentage4,
            'final_variable4': final_SO_variable4,
        },
        'Hits': {
            'percentage': pitcher_hits_percentage,
            'final_variable': final_hits_variable,
            'percentage1': pitcher_hits_percentage1,
            'final_variable1': final_hits_variable1,
            'percentage2': pitcher_hits_percentage2,
            'final_variable2': final_hits_variable2,
            'percentage3': pitcher_hits_percentage3,
            'final_variable3': final_hits_variable3,
            'percentage4': pitcher_hits_percentage4,
            'final_variable4': final_hits_variable4,
        },
        'Walks': {
            'percentage': pitcher_walks_percentage,
            'final_variable': final_walks_variable,
            'percentage1': pitcher_walks_percentage1,
            'final_variable1': final_walks_variable1,
            'percentage2': pitcher_walks_percentage2,
            'final_variable2': final_walks_variable2,
            'percentage3': pitcher_walks_percentage3,
            'final_variable3': final_walks_variable3,
            'percentage4': pitcher_walks_percentage4,
            'final_variable4': final_walks_variable4,
        }
    }

    return json.dumps(results)

if __name__ == '__main__':
    primary_full_url = sys.argv[1]
    opp_full_url = sys.argv[2]
    over_under = sys.argv[3]
    percent_threshold = sys.argv[4]
    pitcher_min_game_threshold = sys.argv[5]
    team_min_game_threshold = sys.argv[6]

    result = calculate_pitcher_data(primary_full_url, opp_full_url, over_under, percent_threshold, pitcher_min_game_threshold, team_min_game_threshold)
    print(result)
