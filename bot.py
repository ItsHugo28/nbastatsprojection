import discord
from discord.ext import commands
from config import TOKEN
import requests
import json
import numpy as np
import os

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def stats(ctx, *args):
    player_name = " ".join(args[:-2])
    stat_category = args[-2]
    stat_value = args[-1]
    player_name = player_name.title()
    stat_value = float(stat_value)
    stat_mappings = {
        "points": "pts",
        "assists": "ast",
        "rebounds": "reb",
        "steals": "stl",
        "blocks": "blk",
        "ftm": "ftm",
        "3pm": "fg3m"
    }

    if stat_category not in stat_mappings:
        await ctx.send(f"Error: {stat_category} is not a valid statistical category.")
        return

    stat_key = stat_mappings[stat_category]
    first_name, last_name = player_name.split()
    player_stats_url = f"https://api.balldontlie.io/v1/players?first_name={first_name}&last_name={last_name}&per_page=100"

    headers = {"Authorization": f"API_KEY"}

    try:

        player_response = requests.get(player_stats_url, headers=headers)
        player_response.raise_for_status()
        player_data = json.loads(player_response.text)["data"][0]

        player_id = player_data["id"]

        game_stats_url = f"https://api.balldontlie.io/v1/stats?seasons[]=2023&player_ids[]={player_id}&per_page=100"
        response = requests.get(game_stats_url, headers=headers)
        game_response = requests.get(game_stats_url, headers=headers)
        game_response.raise_for_status()
        game_data = json.loads(game_response.text)["data"]

        # Remove games with 0 minutes played
        game_data = [game for game in game_data if int(game["min"]) > 0]

        # Sort games by date
        game_data.sort(key=lambda x: x["game"]["date"])

        # Get player's past 5 games stats
        past_games_url = f"https://api.balldontlie.io/v1/season_averages?season=2023&player_ids[]={player_id}&per_page=5"
        past_response = requests.get(past_games_url, headers=headers)
        past_response.raise_for_status()
        past_data = json.loads(past_response.text)["data"]
        past_stat_values = []
        for game in past_data:
            past_stat_values.append(game[stat_key])
        past_avg_stat = np.mean(past_stat_values)

        # Get player's average versus a specific team
        team_stats_url = f"https://api.balldontlie.io/v1/stats?seasons[]=2023&player_ids[]={player_id}&per_page=100"
        team_response = requests.get(team_stats_url, headers=headers)
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

        # Display last 3 games
        last3_values = stat_values[-5:]
        last3 = ", ".join(map(str, last3_values[::-1]))  # join values in reverse order
        sorted_value = np.mean(last3_values)

        combined_avg_stat = (sorted_value + team_avg_stat) / 2
        team_avg_stat = round(team_avg_stat, 2)
        sorted_value = round(sorted_value, 2)
        player_name = player_name.replace("_", " ")

        if stat_value >= combined_avg_stat:
            z_score = (stat_value - combined_avg_stat) / std_dev
            prob = round((1 - 0.5 * (1 + np.math.erf(z_score / np.sqrt(2)))) * 100, 2)
            message = f"```The probability of {player_name} getting {stat_category} of {stat_value} or more is {prob}%\n\n{player_name} Season + Playoff average is {team_avg_stat} {stat_category}\n\n{player_name} last 5 games average is {sorted_value} {stat_category}\n\nLast 5 games: {last3}```"
            await ctx.send(message)
        else:
            z_score = (combined_avg_stat - stat_value) / std_dev
            prob = round((0.5 * (1 + np.math.erf(z_score / np.sqrt(2)))) * 100, 2)
            message = f"```The probability of {player_name} getting {stat_category} of {stat_value} or more is {prob}%\n\n{player_name} Season + Playoff average is {team_avg_stat} {stat_category}\n\n{player_name} last 5 games average is {sorted_value} {stat_category}\n\nLast 5 games: {last3}```"
            await ctx.send(message)

    except requests.exceptions.HTTPError as err:
        await ctx.send(f"Error: {err}")
    except requests.exceptions.RequestException as err:
        await ctx.send(f"Error getting data: {err}")
    except (ValueError, KeyError, IndexError):
        await ctx.send("Error: player not found")


bot.run(TOKEN)
