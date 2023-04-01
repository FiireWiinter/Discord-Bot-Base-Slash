# Discord Bot Base for Slash commands
This is a pre written base for easy cloning (or using GitHubs Template function) to get you started with Discord slash commands.

## Requirements
- Python 3.8 or up
- (A PostgreSQL database if you want to use one)
- Enough Sanity to write slash commands

## Setup
Please run the following command to install all requirements for the bot itself to work. (You will still have to install Python and PostgreSQL yourself)
```
pip install -r requirements.txt
```

Rename the [.env example file](config/.env.example) in `config/` to `.env`

After that go to the [Discord Developer Portal](https://discord.com/developers), create a new Application, add a Bot and copy the Bot Token to the [.env file](config/.env).

## To use PostgreSQL
Uncomment the following Lines in `main.py`. This will connect you to your PostgreSQL database, which you can access through `Bot.pool`.

- Line 8
- Line 40
- Line 94 - 100
- Line 102
- Line 112
