# Chia NFT-Portfolio-Analysis
This Discord bot is designed to provide portfolio analysis of Discord users based on their non-fungible token (NFT) holdings on [Mintgarden](https://mintgarden.io/). When a user requests an analysis, the bot fetches data from the Mintgarden API and computes the total value of the user's portfolio, the number of unique NFTs they hold, and the number of collections these NFTs belong to.

The bot presents this information in an easy-to-understand format, which includes a breakdown of the portfolio by collection. Each collection is accompanied by the total value of NFTs from that collection, the number of NFTs, and the percentage of the total portfolio value it represents.

## Setup Instructions

1. Clone the repository to your local machine:
```bash
git clone https://github.com/your-github-username/Mintgarden-Discord-Bot.git
cd Mintgarden-Discord-Bot
```

2. Install the necessary Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up a bot on the Discord developer portal,
get your token and add the bot to your Discord server. Follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html) if you're not sure how to do it.

5. Bot token
Update your-bot-token in the last line of the value.py script with your actual bot token.

6. Run the bot
```bash
python bot.py
```

## Usage Instructions
To use the bot in your Discord server, simply type /value. The bot will then provide a comprehensive portfolio analysis of your NFT holdings on Mintgarden.

## Note
The values provided by this bot are exclusively based on the floor prices from each collection on Mintgarden.

## Contribution
Contributions are always welcome! Please feel free to submit a pull request.
