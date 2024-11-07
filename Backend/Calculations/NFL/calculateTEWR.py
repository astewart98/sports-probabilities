import subprocess
import ast
import sys
import math
import json

def calculate_te_wr_data(primary_full_url, opp_full_url, over_under, percent_threshold, game_threshold):
    script_path_te_wr_receptions = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/NFL/TE_WR/scrapeTEWRreceptions.py'
    script_path_te_wr_rec_yds = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/NFL/TE_WR/scrapeTEWRrecYards.py'
    script_path_team_receptions = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/NFL/Teams/scrapeTeamReceptions.py'
    script_path_team_rec_yds = '/Users/astewart9841/Desktop/Coding/Bet_Project/Backend/Scraped_Data/NFL/Teams/scrapeTeamPassYds.py'

    result_te_wr_receptions, result_te_wr_rec_yds, result_team_receptions, result_team_rec_yds = [], [], [], []

    result_te_wr_receptions = subprocess.run(['python3', script_path_te_wr_receptions, primary_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_te_wr_rec_yds = subprocess.run(['python3', script_path_te_wr_rec_yds, primary_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_receptions = subprocess.run(['python3', script_path_team_receptions, opp_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_rec_yds = subprocess.run(['python3', script_path_team_rec_yds, opp_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    

    # Convert results to lists
    try:
        if result_te_wr_receptions:
            result_te_wr_receptions = ast.literal_eval(result_te_wr_receptions)
        if result_te_wr_rec_yds:
            result_te_wr_rec_yds = ast.literal_eval(result_te_wr_rec_yds)
        if result_team_receptions:
            result_team_receptions = ast.literal_eval(result_team_receptions)
        if result_team_rec_yds:
            result_team_rec_yds = ast.literal_eval(result_team_rec_yds)

        # Finds length of returned TE/WR and team lists
        te_wr_receptions_length = len(result_te_wr_receptions)
        te_wr_rec_yds_length = len(result_te_wr_rec_yds)
        team_receptions_length = len(result_team_receptions)
        team_rec_yds_length = len(result_team_rec_yds)
        # Finding position number that is percent_threshold the way through the list (70% through list of 10 is the 7th position (0-9 #'s))
        team_receptions_index = int(team_receptions_length * percent_threshold)
        team_rec_yds_index = int(team_rec_yds_length * percent_threshold)
        te_wr_receptions_index = int(te_wr_receptions_length * percent_threshold)
        te_wr_rec_yds_index = int(te_wr_rec_yds_length * percent_threshold)

        # Change HTML percentage input to float and a decimal
        percent_threshold = (float(percent_threshold)) / 100

        # Calculate Over probabilities for all stat categories
        if over_under == 'over':
            # Over Receptions

            # Sorting list of team receptions allowed (largest to smallest)
            team_receptions_sorted = sorted(result_team_receptions, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_receptions_over_variable = team_receptions_sorted[team_receptions_index]
            # Repaeats previous steps for TE/WR
            te_wr_receptions_sorted = sorted(result_te_wr_receptions, reverse=True)
            te_wr_receptions_over_variable = te_wr_receptions_sorted[te_wr_receptions_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_receptions_over_variable = math.floor(min(team_receptions_over_variable, te_wr_receptions_over_variable))

            def calculate_receptions_over_percentage(stat_number):
                # Finds # of times TE/WR receptions greater than or equal to the final_over_variable
                te_wr_receptions_over_count = sum(1 for SO in result_te_wr_receptions if SO >= (final_receptions_over_variable + stat_number))
                # Finds % times TE/WR receptions greater than or equal to the final_over_variable out of te_wr_receptions_length
                te_wr_receptions_over_percentage = (te_wr_receptions_over_count / te_wr_receptions_length) if te_wr_receptions_length else 0
                te_wr_receptions_over_percentage = (te_wr_receptions_over_percentage * 100)
                return te_wr_receptions_over_percentage
            
            # Final result for prime probability
            if final_receptions_over_variable - .5 > 0:
                te_wr_receptions_over_percentage = calculate_receptions_over_percentage(0)
                te_wr_receptions_percentage = f"{te_wr_receptions_over_percentage:.1f}%"
                final_receptions_variable = f"o{final_receptions_over_variable - .5}"
            else:
                final_receptions_variable = ''
                te_wr_receptions_percentage = ''

            # Final result for prime probability -2
            if final_receptions_over_variable - 2.5 > 0:
                te_wr_receptions_over_percentage = calculate_receptions_over_percentage(-2)
                te_wr_receptions_percentage1 = f"{te_wr_receptions_over_percentage:.1f}%"
                final_receptions_variable1 = f"o{final_receptions_over_variable - 2.5}"
            else:
                final_receptions_variable1 = ''
                te_wr_receptions_percentage1 = ''

            # Final result for prime probability -1
            if final_receptions_over_variable - 1.5 > 0:
                te_wr_receptions_over_percentage = calculate_receptions_over_percentage(-1)
                te_wr_receptions_percentage2 = f"{te_wr_receptions_over_percentage:.1f}%"
                final_receptions_variable2 = f"o{final_receptions_over_variable - 1.5}"
            else:
                final_receptions_variable2 = ''
                te_wr_receptions_percentage2 = ''

            # Final result for prime probability +1
            if final_receptions_over_variable + .5 > 0:
                te_wr_receptions_over_percentage = calculate_receptions_over_percentage(1)
                te_wr_receptions_percentage3 = f"{te_wr_receptions_over_percentage:.1f}%"
                final_receptions_variable3 = f"o{final_receptions_over_variable + .5}"
            else:
                final_receptions_variable3 = ''
                te_wr_receptions_percentage3 = ''

            # Final result for prime probability +2
            if final_receptions_over_variable + 1.5 > 0:
                te_wr_receptions_over_percentage = calculate_receptions_over_percentage(2)
                te_wr_receptions_percentage4 = f"{te_wr_receptions_over_percentage:.1f}%"
                final_receptions_variable4 = f"o{final_receptions_over_variable + 1.5}"
            else:
                final_receptions_variable4 = ''
                te_wr_receptions_percentage4 = ''

            # Over Receiving Yards
            
            # Sorting list of team rec YDs allowed (largest to smallest)
            team_rec_yds_sorted = sorted(result_team_rec_yds, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_rec_yds_over_variable = team_rec_yds_sorted[team_rec_yds_index]
            # Repaeats previous steps for TE/WR
            te_wr_rec_yds_sorted = sorted(result_te_wr_rec_yds, reverse=True)
            te_wr_rec_yds_over_variable = te_wr_rec_yds_sorted[te_wr_rec_yds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            min_rec_yds_over_variable = math.floor(min(team_rec_yds_over_variable, te_wr_rec_yds_over_variable))
            if min_rec_yds_over_variable < 25:
                final_rec_yds_over_variable = 25
            else:
                final_rec_yds_over_variable = math.floor(min_rec_yds_over_variable / 10) * 10
            
            def calculate_rec_yds_over_percentage(stat_number):
                # Finds # of times TE/WR rec YDs greater than or equal to the final_over_variable
                te_wr_rec_yds_over_count = sum(1 for hits in result_te_wr_rec_yds if hits >= (final_rec_yds_over_variable + stat_number))
                # Finds % times TE/WR rec YDs greater than or equal to the final_over_variable out of te_wr_rec_yds_length
                te_wr_rec_yds_over_percentage = (te_wr_rec_yds_over_count / te_wr_rec_yds_length) if te_wr_rec_yds_length else 0
                te_wr_rec_yds_over_percentage = (te_wr_rec_yds_over_percentage * 100)
                return te_wr_rec_yds_over_percentage
            
            # Final result for prime probability
            if final_rec_yds_over_variable - .5 > 0:
                te_wr_rec_yds_over_percentage = calculate_rec_yds_over_percentage(0)
                te_wr_rec_yds_percentage = f"{te_wr_rec_yds_over_percentage:.1f}%"
                final_rec_yds_variable = f"o{final_rec_yds_over_variable - .5}"
                if te_wr_rec_yds_over_percentage < (percent_threshold * 100):
                    final_rec_yds_variable = ''
                    te_wr_rec_yds_percentage = ''
            else:
                final_rec_yds_variable = ''
                te_wr_rec_yds_percentage = ''

            # Final result for prime probability -2
            if final_rec_yds_over_variable - 20.5 > 0:
                te_wr_rec_yds_over_percentage = calculate_rec_yds_over_percentage(-20)
                te_wr_rec_yds_percentage1 = f"{te_wr_rec_yds_over_percentage:.1f}%"
                final_rec_yds_variable1 = f"o{final_rec_yds_over_variable - 20.5}"
            else:
                final_rec_yds_variable1 = ''
                te_wr_rec_yds_percentage1 = ''

            # Final result for prime probability -1
            if final_rec_yds_over_variable - 10.5 > 0:
                te_wr_rec_yds_over_percentage = calculate_rec_yds_over_percentage(-10)
                te_wr_rec_yds_percentage2 = f"{te_wr_rec_yds_over_percentage:.1f}%"
                final_rec_yds_variable2 = f"o{final_rec_yds_over_variable - 10.5}"
                
            else:
                final_rec_yds_variable2 = ''
                te_wr_rec_yds_percentage2 = ''

            # Final result for prime probability +1
            if final_rec_yds_over_variable + 9.5 > 0:
                if final_rec_yds_over_variable == 25:
                    te_wr_rec_yds_over_percentage = calculate_rec_yds_over_percentage(15)
                    final_rec_yds_variable3 = f"o{final_rec_yds_over_variable + 14.5}"
                else:
                    te_wr_rec_yds_over_percentage = calculate_rec_yds_over_percentage(10)
                    final_rec_yds_variable3 = f"o{final_rec_yds_over_variable + 9.5}"
                te_wr_rec_yds_percentage3 = f"{te_wr_rec_yds_over_percentage:.1f}%"
            else:
                final_rec_yds_variable3 = ''
                te_wr_rec_yds_percentage3 = ''

            # Final result for prime probability +2
            if final_rec_yds_over_variable + 19.5 > 0:
                if final_rec_yds_over_variable == 25:
                    te_wr_rec_yds_over_percentage = calculate_rec_yds_over_percentage(25)
                    final_rec_yds_variable4 = f"o{final_rec_yds_over_variable + 24.5}"
                else:
                    te_wr_rec_yds_over_percentage = calculate_rec_yds_over_percentage(20)
                    final_rec_yds_variable4 = f"o{final_rec_yds_over_variable + 19.5}"
                te_wr_rec_yds_percentage4 = f"{te_wr_rec_yds_over_percentage:.1f}%"
            else:
                final_rec_yds_variable4 = ''
                te_wr_rec_yds_percentage4 = ''

        # Calculate UNDER probabilities for all stat categories
        elif over_under == 'under':
            # under Receptions

            # Sorting list of team receptions allowed (smallest to largest)
            team_receptions_sorted = sorted(result_team_receptions, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_receptions_under_variable = team_receptions_sorted[team_receptions_index]
            # Repaeats previous steps for TE/WR
            te_wr_receptions_sorted = sorted(result_te_wr_receptions, reverse=False)
            te_wr_receptions_under_variable = te_wr_receptions_sorted[te_wr_receptions_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_receptions_under_variable = math.ceil(min(team_receptions_under_variable, te_wr_receptions_under_variable))
            
            def calculate_receptions_under_percentage(stat_number):
                # Finds # of times TE/WR receptions less than or equal to the final_under_variable
                te_wr_receptions_under_count = sum(1 for SO in result_te_wr_receptions if SO <= (final_receptions_under_variable + stat_number))
                # Finds % times TE/WR receptions less than or equal to the final_under_variable out of te_wr_receptions_length
                te_wr_receptions_under_percentage = (te_wr_receptions_under_count / te_wr_receptions_length) if te_wr_receptions_length else 0
                te_wr_receptions_under_percentage = (te_wr_receptions_under_percentage * 100)
                return te_wr_receptions_under_percentage
            
            # Final result for prime probability
            if final_receptions_under_variable + .5 > 0:
                te_wr_receptions_under_percentage = calculate_receptions_under_percentage(0)
                te_wr_receptions_percentage = f"{te_wr_receptions_under_percentage:.1f}%"
                final_receptions_variable = f"u{final_receptions_under_variable + .5}"
            else:
                final_receptions_variable = ''
                te_wr_receptions_percentage = ''

            # Final result for prime probability -2
            if final_receptions_under_variable - 1.5 > 0:
                te_wr_receptions_under_percentage = calculate_receptions_under_percentage(-2)
                te_wr_receptions_percentage1 = f"{te_wr_receptions_under_percentage:.1f}%"
                final_receptions_variable1 = f"u{final_receptions_under_variable - 1.5}"
            else:
                final_receptions_variable1 = ''
                te_wr_receptions_percentage1 = ''

            # Final result for prime probability -1
            if final_receptions_under_variable - .5 > 0:
                te_wr_receptions_under_percentage = calculate_receptions_under_percentage(-1)
                te_wr_receptions_percentage2 = f"{te_wr_receptions_under_percentage:.1f}%"
                final_receptions_variable2 = f"u{final_receptions_under_variable - .5}"
            else:
                final_receptions_variable2 = ''
                te_wr_receptions_percentage2 = ''

            # Final result for prime probability +1
            if final_receptions_under_variable + 1.5 > 0:
                te_wr_receptions_under_percentage = calculate_receptions_under_percentage(1)
                te_wr_receptions_percentage3 = f"{te_wr_receptions_under_percentage:.1f}%"
                final_receptions_variable3 = f"u{final_receptions_under_variable + 1.5}"
            else:
                final_receptions_variable3 = ''
                te_wr_receptions_percentage3 = ''

            # Final result for prime probability +2
            if final_receptions_under_variable + 2.5 > 0:
                te_wr_receptions_under_percentage = calculate_receptions_under_percentage(2)
                te_wr_receptions_percentage4 = f"{te_wr_receptions_under_percentage:.1f}%"
                final_receptions_variable4 = f"u{final_receptions_under_variable + 2.5}"
            else:
                final_receptions_variable4 = ''
                te_wr_receptions_percentage4 = ''

            # under Receiving Yards
            
            # Sorting list of team rec YDs allowed (smallest to largest)
            team_rec_yds_sorted = sorted(result_team_rec_yds, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_rec_yds_under_variable = team_rec_yds_sorted[team_rec_yds_index]
            # Repaeats previous steps for TE/WR
            te_wr_rec_yds_sorted = sorted(result_te_wr_rec_yds, reverse=False)
            te_wr_rec_yds_under_variable = te_wr_rec_yds_sorted[te_wr_rec_yds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            max_rec_yds_under_variable = math.ceil(min(team_rec_yds_under_variable, te_wr_rec_yds_under_variable))
            final_rec_yds_under_variable = math.ceil(max_rec_yds_under_variable / 10) * 10
            
            def calculate_rec_yds_under_percentage(stat_number):
                # Finds # of times TE/WR rec YDs less than or equal to the final_under_variable
                te_wr_rec_yds_under_count = sum(1 for hits in result_te_wr_rec_yds if hits <= (final_rec_yds_under_variable + stat_number))
                # Finds % times TE/WR rec YDs less than or equal to the final_under_variable out of te_wr_rec_yds_length
                te_wr_rec_yds_under_percentage = (te_wr_rec_yds_under_count / te_wr_rec_yds_length) if te_wr_rec_yds_length else 0
                te_wr_rec_yds_under_percentage = (te_wr_rec_yds_under_percentage * 100)
                return te_wr_rec_yds_under_percentage
            
            # Final result for prime probability
            if final_rec_yds_under_variable + .5 > 0:
                te_wr_rec_yds_under_percentage = calculate_rec_yds_under_percentage(0)
                te_wr_rec_yds_percentage = f"{te_wr_rec_yds_under_percentage:.1f}%"
                final_rec_yds_variable = f"u{final_rec_yds_under_variable + .5}"
                if te_wr_rec_yds_under_percentage < (percent_threshold * 100):
                    final_rec_yds_variable = ''
                    te_wr_rec_yds_percentage = ''
            else:
                final_rec_yds_variable = ''
                te_wr_rec_yds_percentage = ''

            # Final result for prime probability -2
            if final_rec_yds_under_variable - 19.5 > 0:
                te_wr_rec_yds_under_percentage = calculate_rec_yds_under_percentage(-20)
                te_wr_rec_yds_percentage1 = f"{te_wr_rec_yds_under_percentage:.1f}%"
                final_rec_yds_variable1 = f"u{final_rec_yds_under_variable - 19.5}"
            else:
                final_rec_yds_variable1 = ''
                te_wr_rec_yds_percentage1 = ''

            # Final result for prime probability -1
            if final_rec_yds_under_variable - 9.5 > 0:
                te_wr_rec_yds_under_percentage = calculate_rec_yds_under_percentage(-10)
                te_wr_rec_yds_percentage2 = f"{te_wr_rec_yds_under_percentage:.1f}%"
                final_rec_yds_variable2 = f"u{final_rec_yds_under_variable - 9.5}"
            else:
                final_rec_yds_variable2 = ''
                te_wr_rec_yds_percentage2 = ''

            # Final result for prime probability +1
            if final_rec_yds_under_variable + 10.5 > 0:
                te_wr_rec_yds_under_percentage = calculate_rec_yds_under_percentage(10)
                te_wr_rec_yds_percentage3 = f"{te_wr_rec_yds_under_percentage:.1f}%"
                final_rec_yds_variable3 = f"u{final_rec_yds_under_variable + 10.5}"
            else:
                final_rec_yds_variable3 = ''
                te_wr_rec_yds_percentage3 = ''

            # Final result for prime probability +2
            if final_rec_yds_under_variable + 20.5 > 0:
                te_wr_rec_yds_under_percentage = calculate_rec_yds_under_percentage(20)
                te_wr_rec_yds_percentage4 = f"{te_wr_rec_yds_under_percentage:.1f}%"
                final_rec_yds_variable4 = f"u{final_rec_yds_under_variable + 20.5}"
            else:
                final_rec_yds_variable4 = ''
                te_wr_rec_yds_percentage4 = ''

    except (ValueError, SyntaxError) as e:
        print(f"Data Conversion Error: {e}")

    results = {
        'RecYds': {
            'percentage': te_wr_rec_yds_percentage,
            'final_variable': final_rec_yds_variable,
            'percentage1': te_wr_rec_yds_percentage1,
            'final_variable1': final_rec_yds_variable1,
            'percentage2': te_wr_rec_yds_percentage2,
            'final_variable2': final_rec_yds_variable2,
            'percentage3': te_wr_rec_yds_percentage3,
            'final_variable3': final_rec_yds_variable3,
            'percentage4': te_wr_rec_yds_percentage4,
            'final_variable4': final_rec_yds_variable4,
        },
        'Receptions': {
            'percentage': te_wr_receptions_percentage,
            'final_variable': final_receptions_variable,
            'percentage1': te_wr_receptions_percentage1,
            'final_variable1': final_receptions_variable1,
            'percentage2': te_wr_receptions_percentage2,
            'final_variable2': final_receptions_variable2,
            'percentage3': te_wr_receptions_percentage3,
            'final_variable3': final_receptions_variable3,
            'percentage4': te_wr_receptions_percentage4,
            'final_variable4': final_receptions_variable4,
        }
    }

    return json.dumps(results)

if __name__ == '__main__':
    primary_full_url = sys.argv[1]
    opp_full_url = sys.argv[2]
    over_under = sys.argv[3]
    percent_threshold = sys.argv[4]
    game_threshold = sys.argv[5]

    result = calculate_te_wr_data(primary_full_url, opp_full_url, over_under, percent_threshold, game_threshold)
    print(result)
