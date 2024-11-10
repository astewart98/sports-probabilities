import subprocess
import ast
import sys
import math
import json

def calculate_batter_data(primary_full_url, opp_full_url, over_under, percent_threshold, opp_pitcher_hits_threshold, batter_min_game_threshold, pitcher_min_game_threshold):
    script_path_batter_hits = 'Backend/Scraped_Data/MLB/Batters/scrapeBatterHits.py'
    script_path_pitcher_hits = 'Backend/Scraped_Data/MLB/Pitchers/scrapePitcherHitsAllowed.py'

    result_batter_hits, result_pitcher_hits = [], []

    result_batter_hits = subprocess.run(['python3', script_path_batter_hits, primary_full_url, batter_min_game_threshold], capture_output=True, text=True).stdout
    result_pitcher_hits = subprocess.run(['python3', script_path_pitcher_hits, opp_full_url, pitcher_min_game_threshold], capture_output=True, text=True).stdout.strip()

    # Convert results to lists
    try:
        if result_batter_hits:
            result_batter_hits = ast.literal_eval(result_batter_hits)
        if result_pitcher_hits:
            result_pitcher_hits = ast.literal_eval(result_pitcher_hits)

        # Change HTML percentage input to float and a decimal
        percent_threshold = (float(percent_threshold)) / 100
        # Changes HTML pitchers hits allowed threshold to integers
        opp_pitcher_hits_threshold= int(opp_pitcher_hits_threshold)

        # Finds length of returned batter and pitcher lists
        batter_hits_length = len(result_batter_hits)
        pitcher_hits_length = len(result_pitcher_hits)
        # Finding position number that is percent_threshold the way through the list (70% through list of 10 is the 7th position (0-9 #'s))
        pitcher_hits_index = int(pitcher_hits_length * percent_threshold)
        batter_hits_index = int(batter_hits_length * percent_threshold)

        # Calculate over/under probabability
        if over_under == 'over':
            # Finds # of times pitcher allowed hits was greater than or equal to the opp_pitcher_hits_threshold
            pitcher_hits_over_count = sum(1 for hit in result_pitcher_hits if hit >= opp_pitcher_hits_threshold)
            # Finds % times pitcher allowed hits was greater than or equal to the opp_pitcher_hits_threshold out of pitcher_hits_length
            pitcher_hits_over_percentage = (pitcher_hits_over_count / pitcher_hits_length) if pitcher_hits_length else 0

            if pitcher_hits_over_percentage >= percent_threshold:

                # Sorting list of pitcher hits allowed (largest to smallest)
                pitcher_hits_sorted = sorted(result_pitcher_hits, reverse=True)
                # Selecting integer in list that is in the above mentioned position (7th position # = 3)
                pitcher_over_variable = pitcher_hits_sorted[pitcher_hits_index]
                # Repaeats previous steps for batter
                batter_hits_sorted = sorted(result_batter_hits, reverse=True)
                batter_over_variable = batter_hits_sorted[batter_hits_index]
                # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
                final_over_variable = math.floor(min(pitcher_over_variable, batter_over_variable))

                def calculate_hits_over_percentage(stat_number):
                    # Finds # of times batter hit greater than or equal to the final_over_variable
                    batter_hits_over_count = sum(1 for hit in result_batter_hits if hit >= (final_over_variable + stat_number))
                    # Finds % times batter hit more than or equal to the final_over_variable out of batter_hits_length
                    batter_hits_over_percentage = (batter_hits_over_count / batter_hits_length) if batter_hits_length else 0
                    batter_hits_over_percentage = (batter_hits_over_percentage * 100)
                    return batter_hits_over_percentage

                # Final result for prime probability
                if final_over_variable - .5 > 0:
                    batter_hits_over_percentage = calculate_hits_over_percentage(0)
                    batter_hits_percentage = f"{batter_hits_over_percentage:.1f}%"
                    final_hits_variable = f"o{final_over_variable - .5}"
                else:
                    final_hits_variable = ''
                    batter_hits_percentage = ''

                # Final result for prime probability -2
                if final_over_variable - 2.5 > 0:
                    batter_hits_over_percentage = calculate_hits_over_percentage(-2)
                    batter_hits_percentage1 = f"{batter_hits_over_percentage:.1f}%"
                    final_hits_variable1 = f"o{final_over_variable - 2.5}"
                else:
                    final_hits_variable1 = ''
                    batter_hits_percentage1 = ''

                # Final result for prime probability -1
                if final_over_variable - 1.5 > 0:
                    batter_hits_over_percentage = calculate_hits_over_percentage(-1)
                    batter_hits_percentage2 = f"{batter_hits_over_percentage:.1f}%"
                    final_hits_variable2 = f"o{final_over_variable - 1.5}"
                else:
                    final_hits_variable2 = ''
                    batter_hits_percentage2 = ''

                # Final result for prime probability +1
                if final_over_variable + .5 > 0:
                    batter_hits_over_percentage = calculate_hits_over_percentage(1)
                    batter_hits_percentage3 = f"{batter_hits_over_percentage:.1f}%"
                    final_hits_variable3 = f"o{final_over_variable + .5}"
                else:
                    final_hits_variable3 = ''
                    batter_hits_percentage3 = ''

                # Final result for prime probability +2
                if final_over_variable + 1.5 > 0:
                    batter_hits_over_percentage = calculate_hits_over_percentage(2)
                    batter_hits_percentage4 = f"{batter_hits_over_percentage:.1f}%"
                    final_hits_variable4 = f"o{final_over_variable + 1.5}"
                else:
                    final_hits_variable4 = ''
                    batter_hits_percentage4 = ''
                    
            elif pitcher_hits_over_percentage <= percent_threshold:
                
                batter_hits_percentage = ''
                final_hits_variable = "PNAO"

                batter_hits_percentage1 = ''
                final_hits_variable1 = ''

                batter_hits_percentage2 = ''
                final_hits_variable2 = ''

                batter_hits_percentage3 = ''
                final_hits_variable3 = ''

                batter_hits_percentage4 = ''
                final_hits_variable4 = ''

        elif over_under == 'under':
            # Finds # of times pitcher allowed hits was less than or equal to the opp_pitcher_hits_threshold
            pitcher_hits_under_count = sum(1 for hit in result_pitcher_hits if hit <= opp_pitcher_hits_threshold)
            # Finds % times pitcher allowed hits was less than or equal to the opp_pitcher_hits_threshold out of pitcher_hits_length
            pitcher_hits_under_percentage = (pitcher_hits_under_count / pitcher_hits_length) if pitcher_hits_length else 0

            if pitcher_hits_under_percentage >= percent_threshold:

                # Sorting list of pitcher hits allowed (smallest to largest)
                pitcher_hits_sorted = sorted(result_pitcher_hits, reverse=False)
                # Selecting integer in list that is in the above mentioned position (7th position # = 3)
                pitcher_under_variable = pitcher_hits_sorted[pitcher_hits_index]
                # Repaeats previous steps for batter
                batter_hits_sorted = sorted(result_batter_hits, reverse=False)
                batter_under_variable = batter_hits_sorted[batter_hits_index]
                # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
                final_under_variable = math.ceil(max(pitcher_under_variable, batter_under_variable))

                def calculate_hits_under_percentage(stat_number):
                    # Finds # of times batter hit less than or equal to the final_under_variable
                    batter_hits_under_count = sum(1 for hit in result_batter_hits if hit <= (final_under_variable + stat_number))
                    # Finds % times batter hit less than or equal to the final_under_variable out of batter_hits_length
                    batter_hits_under_percentage = (batter_hits_under_count / batter_hits_length) if batter_hits_length else 0
                    batter_hits_under_percentage = (batter_hits_under_percentage * 100)
                    return batter_hits_under_percentage

                # Final result for prime probability
                if final_under_variable + .5 > 0:
                    batter_hits_under_percentage = calculate_hits_under_percentage(0)
                    batter_hits_percentage = f"{batter_hits_under_percentage:.1f}%"
                    final_hits_variable = f"u{final_under_variable + .5}"
                else:
                    final_hits_variable = ''
                    batter_hits_percentage = ''

                # Final result for prime probability -2
                if final_under_variable - 1.5 > 0:
                    batter_hits_under_percentage = calculate_hits_under_percentage(-2)
                    batter_hits_percentage1 = f"{batter_hits_under_percentage:.1f}%"
                    final_hits_variable1 = f"u{final_under_variable - 1.5}"
                else:
                    final_hits_variable1 = ''
                    batter_hits_percentage1 = ''

                # Final result for prime probability -1
                if final_under_variable - .5 > 0:
                    batter_hits_under_percentage = calculate_hits_under_percentage(-1)
                    batter_hits_percentage2 = f"{batter_hits_under_percentage:.1f}%"
                    final_hits_variable2 = f"u{final_under_variable - .5}"
                else:
                    final_hits_variable2 = ''
                    batter_hits_percentage2 = ''

                # Final result for prime probability +1
                if final_under_variable + 1.5 > 0:
                    batter_hits_under_percentage = calculate_hits_under_percentage(1)
                    batter_hits_percentage3 = f"{batter_hits_under_percentage:.1f}%"
                    final_hits_variable3 = f"u{final_under_variable + 1.5}"
                else:
                    final_hits_variable3 = ''
                    batter_hits_percentage3 = ''

                # Final result for prime probability +2
                if final_under_variable + 2.5 > 0:
                    batter_hits_under_percentage = calculate_hits_under_percentage(2)
                    batter_hits_percentage4 = f"{batter_hits_under_percentage:.1f}%"
                    final_hits_variable4 = f"u{final_under_variable + 2.5}"
                else:
                    final_hits_variable4 = ''
                    batter_hits_percentage4 = ''
                    
            elif pitcher_hits_under_percentage <= percent_threshold:
                
                batter_hits_percentage = ''
                final_hits_variable = "PNAU"

                batter_hits_percentage1 = ''
                final_hits_variable1 = ''

                batter_hits_percentage2 = ''
                final_hits_variable2 = ''

                batter_hits_percentage3 = ''
                final_hits_variable3 = ''

                batter_hits_percentage4 = ''
                final_hits_variable4 = ''

    except (ValueError, SyntaxError) as e:
        print(f"Data Conversion Error: {e}")

    results = {
        'Hits': {
            'percentage': batter_hits_percentage,
            'final_variable': final_hits_variable,
            'percentage1': batter_hits_percentage1,
            'final_variable1': final_hits_variable1,
            'percentage2': batter_hits_percentage2,
            'final_variable2': final_hits_variable2,
            'percentage3': batter_hits_percentage3,
            'final_variable3': final_hits_variable3,
            'percentage4': batter_hits_percentage4,
            'final_variable4': final_hits_variable4,
        }
    }

    return json.dumps(results)

if __name__ == '__main__':
    batter_full_url = sys.argv[1]
    opp_pitcher_full_url = sys.argv[2]
    over_under = sys.argv[3]
    percent_threshold = sys.argv[4]
    opp_pitcher_hits_threshold = sys.argv[5]
    batter_min_game_threshold = sys.argv[6]
    pitcher_min_game_threshold = sys.argv[7]

    result = calculate_batter_data(batter_full_url, opp_pitcher_full_url, over_under, percent_threshold, opp_pitcher_hits_threshold, batter_min_game_threshold, pitcher_min_game_threshold)
    print(result)
