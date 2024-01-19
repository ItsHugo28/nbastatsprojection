import requests
import json
import numpy as np

player_name = input("Enter the name of the player: ")
stat_category = input("Enter the statistical category (points, assists, rebounds, steals, blocks): ")
stat_value = float(input(f"Enter the number of {stat_category}: "))

stat_mappings = {
    "points": "pts",
    "assists": "ast",
    "rebounds": "reb",
    "steals": "stl",
    "blocks": "blk"
}




if stat_category not in stat_mappings:
    print(f"Error: {stat_category} is not a valid statistical category.")
    exit()

stat_key = stat_mappings[stat_category]

player_stats_url = f"https://www.balldontlie.io/api/v1/players?search={player_name}"

try:

    player_response = requests.get(player_stats_url)
    player_response.raise_for_status()
    player_data = json.loads(player_response.text)["data"][0]

    player_id = player_data["id"]
    print(player_id)
    game_stats_url = f"https://www.balldontlie.io/api/v1/stats?seasons[]=2023&player_ids[]={player_id}&per_page=100"
    response = requests.get(game_stats_url)
    game_response = requests.get(game_stats_url)
    game_response.raise_for_status()
    game_data = json.loads(game_response.text)["data"]

    # Remove games with 0 minutes played
    game_data = [game for game in game_data if int(game["min"]) > 0]

    # Get player's past 5 games stats
    past_games_url = f"https://www.balldontlie.io/api/v1/season_averages?seasons[]=2023&player_ids[]={player_id}&per_page=5"
    past_response = requests.get(past_games_url)
    past_response.raise_for_status()
    past_data = json.loads(past_response.text)["data"]
    past_stat_values = []
    for game in past_data:
        past_stat_values.append(game[stat_key])
    past_avg_stat = np.mean(past_stat_values)

    # Get player's average versus a specific team
    team_stats_url = f"https://www.balldontlie.io/api/v1/stats?seasons[]=2023&player_ids[]={player_id}&per_page=100"
    team_response = requests.get(team_stats_url)
    team_response.raise_for_status()
    team_data = json.loads(team_response.text)["data"]

    team_data = [game for game in team_data if int(game["min"]) > 0]
    team_stat_values = []

    for game in team_data:
        team_stat_values.append(game[stat_key])
    team_avg_stat = np.mean(team_stat_values)

    stat_values = []
    for game in game_data:
        stat_values.append(game[stat_key])

    avg_stat = np.mean(stat_values)
    std_dev = np.std(stat_values)
    # Combine past 5 games average with overall average and average versus specific team
    sorted_values = stat_values[-3:]
    print(sorted_values)
    print(team_stat_values)
    sorted_value = np.mean(sorted_values)
    combined_avg_stat = (sorted_value + team_avg_stat) / 2
    if stat_value >= combined_avg_stat:
        z_score = (stat_value - combined_avg_stat) / std_dev
        prob = round((1 - 0.5 * (1 + np.math.erf(z_score / np.sqrt(2)))) * 100, 2)
        print(f"The probability of {player_name} getting {stat_category} of {stat_value} or more is {prob}%")
    else:
        z_score = (combined_avg_stat - stat_value) / std_dev
        prob = round((0.5 * (1 + np.math.erf(z_score / np.sqrt(2)))) * 100, 2)
        print(f"The probability of {player_name} getting {stat_category} of {stat_value} or more is {prob}%")

except requests.exceptions.HTTPError as err:
    print(f"Error: {err}")
except requests.exceptions.RequestException as err:
    print(f"Error getting data: {err}")
except (ValueError, KeyError, IndexError):
    print("Error: player not found")