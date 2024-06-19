# Discord Bot for Player Statistics

This project is a Discord bot that retrieves and calculates basketball player statistics from the [Ball Don't Lie API](https://www.balldontlie.io/). The bot can calculate probabilities of a player achieving specific stats in a game, based on their historical performance.

## Features

- Fetch player information based on their name.
- Calculate averages of specified statistics over the last 5 games.
- Calculate season and playoff averages.
- Compute the probability of a player achieving a specified stat value in a game.
- Handle multiple statistical categories like points, assists, rebounds, steals, blocks, free throws made (FTM), and three-pointers made (3PM).

## Prerequisites

- Python 3.8 or higher
- `discord.py` library
- `requests` library
- `numpy` library

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/discord-bot.git
   cd discord-bot
   ```

2. Install the required libraries:
   ```sh
   pip install discord.py requests numpy
   ```

3. Create a `config.py` file with your Discord bot token:
   ```python
   TOKEN = 'your_discord_bot_token_here'
   ```

## Running the Bot

To run the bot, execute the following command:
```sh
python bot.py
```

## Usage

### Commands

The bot responds to commands prefixed with `!`. The main command is `!stats`.

#### `!stats [player_name] [stat_category] [stat_value]`

- **player_name**: The name of the player (e.g., "LeBron James").
- **stat_category**: The statistical category to query (e.g., "points", "assists", "rebounds").
- **stat_value**: The target value for the specified statistical category.

**Example**:
```sh
!stats LeBron James points 25
```

This command will calculate and display the probability of LeBron James scoring 25 or more points in a game, based on his historical performance.

### Statistical Categories

The bot supports the following statistical categories:

- points
- assists
- rebounds
- steals
- blocks
- ftm (free throws made)
- 3pm (three-pointers made)

### Error Handling

The bot handles various error scenarios, including:
- Invalid player names.
- Invalid statistical categories.
- Errors in retrieving data from the API.

## Dependencies

- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [requests](https://docs.python-requests.org/en/latest/)
- [numpy](https://numpy.org/doc/stable/)


## Acknowledgments

- [Ball Don't Lie API](https://www.balldontlie.io/) for providing the basketball data.
