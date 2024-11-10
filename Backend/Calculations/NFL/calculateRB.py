import subprocess
import ast
import sys
import math
import json

def calculate_rb_data(primary_full_url, opp_full_url, over_under, percent_threshold, game_threshold):
    script_path_rb_rush_att = 'Backend/Scraped_Data/NFL/RB/scrapeRBrushAttempts.py'
    script_path_rb_rec_yds = 'Backend/Scraped_Data/NFL/RB/scrapeRBrecYards.py'
    script_path_rb_rush_yds = 'Backend/Scraped_Data/NFL/RB/scrapeRBrushYards.py'
    script_path_team_rush_att = 'Backend/Scraped_Data/NFL/Teams/scrapeTeamRushAttempts.py'
    script_path_team_rec_yds = 'Backend/Scraped_Data/NFL/Teams/scrapeTeamPassYds.py'
    script_path_team_rush_yds = 'Backend/Scraped_Data/NFL/Teams/scrapeTeamRushYds.py'

    result_rb_rush_att, result_rb_rec_yds, result_rb_rush_yds, result_team_rush_att, result_team_rec_yds, result_team_rush_yds = [], [], [], [], [], []

    result_rb_rush_att = subprocess.run(['python3', script_path_rb_rush_att, primary_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_rb_rec_yds = subprocess.run(['python3', script_path_rb_rec_yds, primary_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_rb_rush_yds = subprocess.run(['python3', script_path_rb_rush_yds, primary_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_rush_att = subprocess.run(['python3', script_path_team_rush_att, opp_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_rec_yds = subprocess.run(['python3', script_path_team_rec_yds, opp_full_url, game_threshold], capture_output=True, text=True).stdout.strip()
    result_team_rush_yds = subprocess.run(['python3', script_path_team_rush_yds, opp_full_url, game_threshold], capture_output=True, text=True).stdout.strip()

    # Convert results to lists
    try:
        if result_rb_rush_att:
            result_rb_rush_att = ast.literal_eval(result_rb_rush_att)
        if result_rb_rec_yds:
            result_rb_rec_yds = ast.literal_eval(result_rb_rec_yds)
        if result_rb_rush_yds:
            result_rb_rush_yds = ast.literal_eval(result_rb_rush_yds)
        if result_team_rush_att:
            result_team_rush_att = ast.literal_eval(result_team_rush_att)
        if result_team_rec_yds:
            result_team_rec_yds = ast.literal_eval(result_team_rec_yds)
        if result_team_rush_yds:
            result_team_rush_yds = ast.literal_eval(result_team_rush_yds)

        # Finds length of returned RB and team lists
        rb_rush_att_length = len(result_rb_rush_att)
        rb_rec_yds_length = len(result_rb_rec_yds)
        rb_rush_yds_length = len(result_rb_rush_yds)
        team_rush_att_length = len(result_team_rush_att)
        team_rec_yds_length = len(result_team_rec_yds)
        team_rush_yds_length = len(result_team_rush_yds)
        # Finding position number that is percent_threshold the way through the list (70% through list of 10 is the 7th position (0-9 #'s))
        team_rush_att_index = int(team_rush_att_length * percent_threshold)
        team_rec_yds_index = int(team_rec_yds_length * percent_threshold)
        team_rush_yds_index = int(team_rush_yds_length * percent_threshold)
        rb_rush_att_index = int(rb_rush_att_length * percent_threshold)
        rb_rec_yds_index = int(rb_rec_yds_length * percent_threshold)
        rb_rush_yds_index = int(rb_rush_yds_length * percent_threshold)

        # Change HTML percentage input to float and a decimal
        percent_threshold = (float(percent_threshold)) / 100

        # Calculate Over probabilities for all stat categories
        if over_under == 'over':
            # Over Rush Attempts

            # Sorting list of team rush atts allowed (largest to smallest)
            team_rush_att_sorted = sorted(result_team_rush_att, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_rush_att_over_variable = team_rush_att_sorted[team_rush_att_index]
            # Repaeats previous steps for RB
            rb_rush_att_sorted = sorted(result_rb_rush_att, reverse=True)
            rb_rush_att_over_variable = rb_rush_att_sorted[rb_rush_att_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_rush_att_over_variable = math.floor(min(team_rush_att_over_variable, rb_rush_att_over_variable))

            def calculate_rush_att_over_percentage(stat_number):
                # Finds # of times RB rush atts greater than or equal to the final_over_variable
                rb_rush_att_over_count = sum(1 for SO in result_rb_rush_att if SO >= (final_rush_att_over_variable + stat_number))
                # Finds % times RB rush atts greater than or equal to the final_over_variable out of rb_rush_att_length
                rb_rush_att_over_percentage = (rb_rush_att_over_count / rb_rush_att_length) if rb_rush_att_length else 0
                rb_rush_att_over_percentage = (rb_rush_att_over_percentage * 100)
                return rb_rush_att_over_percentage
            
            # Final result for prime probability
            if final_rush_att_over_variable - .5 > 0:
                rb_rush_att_over_percentage = calculate_rush_att_over_percentage(0)
                rb_rush_att_percentage = f"{rb_rush_att_over_percentage:.1f}%"
                final_rush_att_variable = f"o{final_rush_att_over_variable - .5}"
            else:
                final_rush_att_variable = ''
                rb_rush_att_percentage = ''

            # Final result for prime probability -2
            if final_rush_att_over_variable - 2.5 > 0:
                rb_rush_att_over_percentage = calculate_rush_att_over_percentage(-2)
                rb_rush_att_percentage1 = f"{rb_rush_att_over_percentage:.1f}%"
                final_rush_att_variable1 = f"o{final_rush_att_over_variable - 2.5}"
            else:
                final_rush_att_variable1 = ''
                rb_rush_att_percentage1 = ''

            # Final result for prime probability -1
            if final_rush_att_over_variable - 1.5 > 0:
                rb_rush_att_over_percentage = calculate_rush_att_over_percentage(-1)
                rb_rush_att_percentage2 = f"{rb_rush_att_over_percentage:.1f}%"
                final_rush_att_variable2 = f"o{final_rush_att_over_variable - 1.5}"
            else:
                final_rush_att_variable2 = ''
                rb_rush_att_percentage2 = ''

            # Final result for prime probability +1
            if final_rush_att_over_variable + .5 > 0:
                rb_rush_att_over_percentage = calculate_rush_att_over_percentage(1)
                rb_rush_att_percentage3 = f"{rb_rush_att_over_percentage:.1f}%"
                final_rush_att_variable3 = f"o{final_rush_att_over_variable + .5}"
            else:
                final_rush_att_variable3 = ''
                rb_rush_att_percentage3 = ''

            # Final result for prime probability +2
            if final_rush_att_over_variable + 1.5 > 0:
                rb_rush_att_over_percentage = calculate_rush_att_over_percentage(2)
                rb_rush_att_percentage4 = f"{rb_rush_att_over_percentage:.1f}%"
                final_rush_att_variable4 = f"o{final_rush_att_over_variable + 1.5}"
            else:
                final_rush_att_variable4 = ''
                rb_rush_att_percentage4 = ''

            # Over Receiving Yards
            
            # Sorting list of team rec YDs allowed (largest to smallest)
            team_rec_yds_sorted = sorted(result_team_rec_yds, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_rec_yds_over_variable = team_rec_yds_sorted[team_rec_yds_index]
            # Repaeats previous steps for RB
            rb_rec_yds_sorted = sorted(result_rb_rec_yds, reverse=True)
            rb_rec_yds_over_variable = rb_rec_yds_sorted[rb_rec_yds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            min_rec_yds_over_variable = math.floor(min(team_rec_yds_over_variable, rb_rec_yds_over_variable))
            if min_rec_yds_over_variable < 25:
                final_rec_yds_over_variable = 25
            else:
                final_rec_yds_over_variable = math.floor(min_rec_yds_over_variable / 10) * 10

            def calculate_rec_yds_over_percentage(stat_number):
                # Finds # of times RB rec YDs greater than or equal to the final_over_variable
                rb_rec_yds_over_count = sum(1 for hits in result_rb_rec_yds if hits >= (final_rec_yds_over_variable + stat_number))
                # Finds % times RB rec YDs greater than or equal to the final_over_variable out of rb_rec_yds_length
                rb_rec_yds_over_percentage = (rb_rec_yds_over_count / rb_rec_yds_length) if rb_rec_yds_length else 0
                rb_rec_yds_over_percentage = (rb_rec_yds_over_percentage * 100)
                return rb_rec_yds_over_percentage
            
            # Final result for prime probability
            if final_rec_yds_over_variable - .5 > 0:
                rb_rec_yds_over_percentage = calculate_rec_yds_over_percentage(0)
                rb_rec_yds_percentage = f"{rb_rec_yds_over_percentage:.1f}%"
                final_rec_yds_variable = f"o{final_rec_yds_over_variable - .5}"
                if rb_rec_yds_over_percentage < (percent_threshold * 100):
                    final_rec_yds_variable = ''
                    rb_rec_yds_percentage = ''
            else:
                final_rec_yds_variable = ''
                rb_rec_yds_percentage = ''

            # Final result for prime probability -2
            if final_rec_yds_over_variable - 20.5 > 0:
                rb_rec_yds_over_percentage = calculate_rec_yds_over_percentage(-20)
                rb_rec_yds_percentage1 = f"{rb_rec_yds_over_percentage:.1f}%"
                final_rec_yds_variable1 = f"o{final_rec_yds_over_variable - 20.5}"
                
            else:
                final_rec_yds_variable1 = ''
                rb_rec_yds_percentage1 = ''

            # Final result for prime probability -1
            if final_rec_yds_over_variable - 10.5 > 0:
                rb_rec_yds_over_percentage = calculate_rec_yds_over_percentage(-10)
                rb_rec_yds_percentage2 = f"{rb_rec_yds_over_percentage:.1f}%"
                final_rec_yds_variable2 = f"o{final_rec_yds_over_variable - 10.5}"
                
            else:
                final_rec_yds_variable2 = ''
                rb_rec_yds_percentage2 = ''

            # Final result for prime probability +1
            if final_rec_yds_over_variable + 9.5 > 0:
                if final_rec_yds_over_variable == 25:
                    rb_rec_yds_over_percentage = calculate_rec_yds_over_percentage(15)
                    final_rec_yds_variable3 = f"o{final_rec_yds_over_variable + 14.5}"
                else:
                    rb_rec_yds_over_percentage = calculate_rec_yds_over_percentage(10)
                    final_rec_yds_variable3 = f"o{final_rec_yds_over_variable + 9.5}"
                rb_rec_yds_percentage3 = f"{rb_rec_yds_over_percentage:.1f}%"
            else:
                final_rec_yds_variable3 = ''
                rb_rec_yds_percentage3 = ''

            # Final result for prime probability +2
            if final_rec_yds_over_variable + 19.5 > 0:
                if final_rec_yds_over_variable == 25:
                    rb_rec_yds_over_percentage = calculate_rec_yds_over_percentage(25)
                    final_rec_yds_variable4 = f"o{final_rec_yds_over_variable + 24.5}"
                else:
                    rb_rec_yds_over_percentage = calculate_rec_yds_over_percentage(20)
                    final_rec_yds_variable4 = f"o{final_rec_yds_over_variable + 19.5}"
                rb_rec_yds_percentage4 = f"{rb_rec_yds_over_percentage:.1f}%"
            else:
                final_rec_yds_variable4 = ''
                rb_rec_yds_percentage4 = ''

            # Over Rush Yards

            # Sorting list of team rush YDs allowed (largest to smallest)
            team_rush_yds_sorted = sorted(result_team_rush_yds, reverse=True)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_rush_yds_over_variable = team_rush_yds_sorted[team_rush_yds_index]
            # Repaeats previous steps for RB
            rb_rush_yds_sorted = sorted(result_rb_rush_yds, reverse=True)
            rb_rush_yds_over_variable = rb_rush_yds_sorted[rb_rush_yds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            min_rush_yds_over_variable = math.floor(min(team_rush_yds_over_variable, rb_rush_yds_over_variable))
            if min_rush_yds_over_variable < 25:
                final_rush_yds_over_variable = 25
            else:
                final_rush_yds_over_variable = math.floor(min_rush_yds_over_variable / 10) * 10
            
            def calculate_rush_yds_over_percentage(stat_number):
                # Finds # of times RB rush YDs greater than or equal to the final_over_variable
                rb_rush_yds_over_count = sum(1 for walks in result_rb_rush_yds if walks >= (final_rush_yds_over_variable + stat_number))
                # Finds % times RB rush YDs greater than or equal to the final_over_variable out of rb_rush_yds_length
                rb_rush_yds_over_percentage = (rb_rush_yds_over_count / rb_rush_yds_length) if rb_rush_yds_length else 0
                rb_rush_yds_over_percentage = (rb_rush_yds_over_percentage * 100)
                return rb_rush_yds_over_percentage
            
            # Final result for prime probability
            if final_rush_yds_over_variable - .5 > 0:
                rb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(0)
                rb_rush_yds_percentage = f"{rb_rush_yds_over_percentage:.1f}%"
                final_rush_yds_variable = f"o{final_rush_yds_over_variable - .5}"
                if rb_rush_yds_over_percentage < (percent_threshold * 100):
                    final_rush_yds_variable = ''
                    rb_rush_yds_percentage = ''
            else:
                final_rush_yds_variable = ''
                rb_rush_yds_percentage = ''

            # Final result for prime probability -2
            if final_rush_yds_over_variable - 20.5 > 0:
                rb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(-20)
                rb_rush_yds_percentage1 = f"{rb_rush_yds_over_percentage:.1f}%"
                final_rush_yds_variable1 = f"o{final_rush_yds_over_variable - 20.5}"
                
            else:
                final_rush_yds_variable1 = ''
                rb_rush_yds_percentage1 = ''

            # Final result for prime probability -1
            if final_rush_yds_over_variable - 10.5 > 0:
                rb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(-10)
                rb_rush_yds_percentage2 = f"{rb_rush_yds_over_percentage:.1f}%"
                final_rush_yds_variable2 = f"o{final_rush_yds_over_variable - 10.5}"
                
            else:
                final_rush_yds_variable2 = ''
                rb_rush_yds_percentage2 = ''

            # Final result for prime probability +1
            if final_rush_yds_over_variable + 9.5 > 0:
                if final_rush_yds_over_variable == 25:
                    rb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(15)
                    final_rush_yds_variable3 = f"o{final_rush_yds_over_variable + 14.5}"
                else:
                    rb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(10)
                    final_rush_yds_variable3 = f"o{final_rush_yds_over_variable + 9.5}"
                rb_rush_yds_percentage3 = f"{rb_rush_yds_over_percentage:.1f}%"
            else:
                final_rush_yds_variable3 = ''
                rb_rush_yds_percentage3 = ''

            # Final result for prime probability +2
            if final_rush_yds_over_variable + 19.5 > 0:
                if final_rush_yds_over_variable == 25:
                    rb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(25)
                    final_rush_yds_variable4 = f"o{final_rush_yds_over_variable + 24.5}"
                else:
                    rb_rush_yds_over_percentage = calculate_rush_yds_over_percentage(20)
                    final_rush_yds_variable4 = f"o{final_rush_yds_over_variable + 19.5}"
                rb_rush_yds_percentage4 = f"{rb_rush_yds_over_percentage:.1f}%"
            else:
                final_rush_yds_variable4 = ''
                rb_rush_yds_percentage4 = ''

        # Calculate Under probabilities for all stat categories
        elif over_under == 'under':
            # Under Rush Attempts

            # Sorting list of team rush atts allowed (smallest to largest)
            team_rush_att_sorted = sorted(result_team_rush_att, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_rush_att_under_variable = team_rush_att_sorted[team_rush_att_index]
            # Repaeats previous steps for RB
            rb_rush_att_sorted = sorted(result_rb_rush_att, reverse=False)
            rb_rush_att_under_variable = rb_rush_att_sorted[rb_rush_att_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            final_rush_att_under_variable = math.floor(max(team_rush_att_under_variable, rb_rush_att_under_variable))
            
            def calculate_rush_att_under_percentage(stat_number):
                # Finds # of times RB rush atts less than or equal to the final_under_variable
                rb_rush_att_under_count = sum(1 for SO in result_rb_rush_att if SO <= (final_rush_att_under_variable + stat_number))
                # Finds % times RB rush atts less than or equal to the final_under_variable out of rb_rush_att_length
                rb_rush_att_under_percentage = (rb_rush_att_under_count / rb_rush_att_length) if rb_rush_att_length else 0
                rb_rush_att_under_percentage = (rb_rush_att_under_percentage * 100)
                return rb_rush_att_under_percentage
            
            # Final result for prime probability
            if final_rush_att_under_variable + .5 > 0:
                rb_rush_att_under_percentage = calculate_rush_att_under_percentage(0)
                rb_rush_att_percentage = f"{rb_rush_att_under_percentage:.1f}%"
                final_rush_att_variable = f"u{final_rush_att_under_variable + .5}"
            else:
                final_rush_att_variable = ''
                rb_rush_att_percentage = ''

            # Final result for prime probability -2
            if final_rush_att_under_variable - 1.5 > 0:
                rb_rush_att_under_percentage = calculate_rush_att_under_percentage(-2)
                rb_rush_att_percentage1 = f"{rb_rush_att_under_percentage:.1f}%"
                final_rush_att_variable1 = f"u{final_rush_att_under_variable - 1.5}"
            else:
                final_rush_att_variable1 = ''
                rb_rush_att_percentage1 = ''

            # Final result for prime probability -1
            if final_rush_att_under_variable - .5 > 0:
                rb_rush_att_under_percentage = calculate_rush_att_under_percentage(-1)
                rb_rush_att_percentage2 = f"{rb_rush_att_under_percentage:.1f}%"
                final_rush_att_variable2 = f"u{final_rush_att_under_variable - .5}"
            else:
                final_rush_att_variable2 = ''
                rb_rush_att_percentage2 = ''

            # Final result for prime probability +1
            if final_rush_att_under_variable + 1.5 > 0:
                rb_rush_att_under_percentage = calculate_rush_att_under_percentage(1)
                rb_rush_att_percentage3 = f"{rb_rush_att_under_percentage:.1f}%"
                final_rush_att_variable3 = f"u{final_rush_att_under_variable + 1.5}"
            else:
                final_rush_att_variable3 = ''
                rb_rush_att_percentage3 = ''

            # Final result for prime probability +2
            if final_rush_att_under_variable + 2.5 > 0:
                rb_rush_att_under_percentage = calculate_rush_att_under_percentage(2)
                rb_rush_att_percentage4 = f"{rb_rush_att_under_percentage:.1f}%"
                final_rush_att_variable4 = f"u{final_rush_att_under_variable + 2.5}"
            else:
                final_rush_att_variable4 = ''
                rb_rush_att_percentage4 = ''

            # under Receiving Yards
            
            # Sorting list of team rec YDs allowed (smallest to largest)
            team_rec_yds_sorted = sorted(result_team_rec_yds, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_rec_yds_under_variable = team_rec_yds_sorted[team_rec_yds_index]
            # Repaeats previous steps for RB
            rb_rec_yds_sorted = sorted(result_rb_rec_yds, reverse=False)
            rb_rec_yds_under_variable = rb_rec_yds_sorted[rb_rec_yds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            if team_rec_yds_under_variable < rb_rec_yds_under_variable:
                max_rec_yds_under_variable = team_rec_yds_under_variable
            else:
                max_rec_yds_under_variable = rb_rec_yds_under_variable
            final_rec_yds_under_variable = math.floor(max_rec_yds_under_variable / 10) * 10
            
            def calculate_rec_yds_under_percentage(stat_number):
                # Finds # of times RB rec YDs less than or equal to the final_under_variable
                rb_rec_yds_under_count = sum(1 for hits in result_rb_rec_yds if hits <= (final_rec_yds_under_variable + stat_number))
                # Finds % times RB rec YDs less than or equal to the final_under_variable out of rb_rec_yds_length
                rb_rec_yds_under_percentage = (rb_rec_yds_under_count / rb_rec_yds_length) if rb_rec_yds_length else 0
                rb_rec_yds_under_percentage = (rb_rec_yds_under_percentage * 100)
                return rb_rec_yds_under_percentage
            
            # Final result for prime probability
            if final_rec_yds_under_variable + .5 > 0:
                rb_rec_yds_under_percentage = calculate_rec_yds_under_percentage(0)
                rb_rec_yds_percentage = f"{rb_rec_yds_under_percentage:.1f}%"
                final_rec_yds_variable = f"u{final_rec_yds_under_variable + .5}"
                if rb_rec_yds_under_percentage < (percent_threshold * 100):
                    final_rec_yds_variable = ''
                    rb_rec_yds_percentage = ''
            else:
                final_rec_yds_variable = ''
                rb_rec_yds_percentage = ''

            # Final result for prime probability -2
            if final_rec_yds_under_variable - 19.5 > 0:
                rb_rec_yds_under_percentage = calculate_rec_yds_under_percentage(-20)
                rb_rec_yds_percentage1 = f"{rb_rec_yds_under_percentage:.1f}%"
                final_rec_yds_variable1 = f"u{final_rec_yds_under_variable - 19.5}"
            else:
                final_rec_yds_variable1 = ''
                rb_rec_yds_percentage1 = ''

            # Final result for prime probability -1
            if final_rec_yds_under_variable - 9.5 > 0:
                rb_rec_yds_under_percentage = calculate_rec_yds_under_percentage(-10)
                rb_rec_yds_percentage2 = f"{rb_rec_yds_under_percentage:.1f}%"
                final_rec_yds_variable2 = f"u{final_rec_yds_under_variable - 9.5}"
            else:
                final_rec_yds_variable2 = ''
                rb_rec_yds_percentage2 = ''

            # Final result for prime probability +1
            if final_rec_yds_under_variable + 10.5 > 0:
                rb_rec_yds_under_percentage = calculate_rec_yds_under_percentage(10)
                rb_rec_yds_percentage3 = f"{rb_rec_yds_under_percentage:.1f}%"
                final_rec_yds_variable3 = f"u{final_rec_yds_under_variable + 10.5}"
            else:
                final_rec_yds_variable3 = ''
                rb_rec_yds_percentage3 = ''

            # Final result for prime probability +2
            if final_rec_yds_under_variable + 20.5 > 0:
                rb_rec_yds_under_percentage = calculate_rec_yds_under_percentage(20)
                rb_rec_yds_percentage4 = f"{rb_rec_yds_under_percentage:.1f}%"
                final_rec_yds_variable4 = f"u{final_rec_yds_under_variable + 20.5}"
            else:
                final_rec_yds_variable4 = ''
                rb_rec_yds_percentage4 = ''

            # under Rush Yards

            # Sorting list of team rush YDs allowed (smallest to largest)
            team_rush_yds_sorted = sorted(result_team_rush_yds, reverse=False)
            # Selecting integer in list that is in the above mentioned position (7th position # = 3)
            team_rush_yds_under_variable = team_rush_yds_sorted[team_rush_yds_index]
            # Repaeats previous steps for RB
            rb_rush_yds_sorted = sorted(result_rb_rush_yds, reverse=False)
            rb_rush_yds_under_variable = rb_rush_yds_sorted[rb_rush_yds_index]
            # Selecting the smallest of the two above integers selected (allows for lowest possible outcome # to be used)
            if team_rush_yds_under_variable < rb_rush_yds_under_variable:
                max_rush_yds_under_variable = team_rush_yds_under_variable
            else:
                max_rush_yds_under_variable = rb_rush_yds_under_variable
            final_rush_yds_under_variable = math.floor(max_rush_yds_under_variable / 10) * 10
            
            def calculate_rush_yds_under_percentage(stat_number):
                # Finds # of times RB rush YDs less than or equal to the final_under_variable
                rb_rush_yds_under_count = sum(1 for walks in result_rb_rush_yds if walks <= (final_rush_yds_under_variable + stat_number))
                # Finds % times RB rush YDs less than or equal to the final_under_variable out of rb_rush_yds_length
                rb_rush_yds_under_percentage = (rb_rush_yds_under_count / rb_rush_yds_length) if rb_rush_yds_length else 0
                rb_rush_yds_under_percentage = (rb_rush_yds_under_percentage * 100)
                return rb_rush_yds_under_percentage
            
            # Final result for prime probability
            if final_rush_yds_under_variable + .5 > 0:
                rb_rush_yds_under_percentage = calculate_rush_yds_under_percentage(0)
                rb_rush_yds_percentage = f"{rb_rush_yds_under_percentage:.1f}%"
                final_rush_yds_variable = f"u{final_rush_yds_under_variable + .5}"
                if rb_rush_yds_under_percentage < (percent_threshold * 100):
                    final_rush_yds_variable = ''
                    rb_rush_yds_percentage = ''
            else:
                final_rush_yds_variable = ''
                rb_rush_yds_percentage = ''

            # Final result for prime probability -2
            if final_rush_yds_under_variable - 19.5 > 0:
                rb_rush_yds_under_percentage = calculate_rush_yds_under_percentage(-20)
                rb_rush_yds_percentage1 = f"{rb_rush_yds_under_percentage:.1f}%"
                final_rush_yds_variable1 = f"u{final_rush_yds_under_variable - 19.5}"
            else:
                final_rush_yds_variable1 = ''
                rb_rush_yds_percentage1 = ''

            # Final result for prime probability -1
            if final_rush_yds_under_variable - 9.5 > 0:
                rb_rush_yds_under_percentage = calculate_rush_yds_under_percentage(-10)
                rb_rush_yds_percentage2 = f"{rb_rush_yds_under_percentage:.1f}%"
                final_rush_yds_variable2 = f"u{final_rush_yds_under_variable - 9.5}"
            else:
                final_rush_yds_variable2 = ''
                rb_rush_yds_percentage2 = ''

            # Final result for prime probability +1
            if final_rush_yds_under_variable + 10.5 > 0:
                rb_rush_yds_under_percentage = calculate_rush_yds_under_percentage(10)
                rb_rush_yds_percentage3 = f"{rb_rush_yds_under_percentage:.1f}%"
                final_rush_yds_variable3 = f"u{final_rush_yds_under_variable + 10.5}"
            else:
                final_rush_yds_variable3 = ''
                rb_rush_yds_percentage3 = ''

            # Final result for prime probability +2
            if final_rush_yds_under_variable + 20.5 > 0:
                rb_rush_yds_under_percentage = calculate_rush_yds_under_percentage(20)
                rb_rush_yds_percentage4 = f"{rb_rush_yds_under_percentage:.1f}%"
                final_rush_yds_variable4 = f"u{final_rush_yds_under_variable + 20.5}"
            else:
                final_rush_yds_variable4 = ''
                rb_rush_yds_percentage4 = ''

    except (ValueError, SyntaxError) as e:
        print(f"Data Conversion Error: {e}")

    results = {
        'RushYds': {
            'percentage': rb_rush_yds_percentage,
            'final_variable': final_rush_yds_variable,
            'percentage1': rb_rush_yds_percentage1,
            'final_variable1': final_rush_yds_variable1,
            'percentage2': rb_rush_yds_percentage2,
            'final_variable2': final_rush_yds_variable2,
            'percentage3': rb_rush_yds_percentage3,
            'final_variable3': final_rush_yds_variable3,
            'percentage4': rb_rush_yds_percentage4,
            'final_variable4': final_rush_yds_variable4,
        },
        'RushAtt': {
            'percentage': rb_rush_att_percentage,
            'final_variable': final_rush_att_variable,
            'percentage1': rb_rush_att_percentage1,
            'final_variable1': final_rush_att_variable1,
            'percentage2': rb_rush_att_percentage2,
            'final_variable2': final_rush_att_variable2,
            'percentage3': rb_rush_att_percentage3,
            'final_variable3': final_rush_att_variable3,
            'percentage4': rb_rush_att_percentage4,
            'final_variable4': final_rush_att_variable4,
        },
        'RecYds': {
            'percentage': rb_rec_yds_percentage,
            'final_variable': final_rec_yds_variable,
            'percentage1': rb_rec_yds_percentage1,
            'final_variable1': final_rec_yds_variable1,
            'percentage2': rb_rec_yds_percentage2,
            'final_variable2': final_rec_yds_variable2,
            'percentage3': rb_rec_yds_percentage3,
            'final_variable3': final_rec_yds_variable3,
            'percentage4': rb_rec_yds_percentage4,
            'final_variable4': final_rec_yds_variable4,
        }
    }

    return json.dumps(results)

if __name__ == '__main__':
    primary_full_url = sys.argv[1]
    opp_full_url = sys.argv[2]
    over_under = sys.argv[3]
    percent_threshold = sys.argv[4]
    game_threshold = sys.argv[5]

    result = calculate_rb_data(primary_full_url, opp_full_url, over_under, percent_threshold, game_threshold)
    print(result)
