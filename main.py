import coloredlogs
import yaml
import asyncio
import logging
import datetime
from os import getenv, listdir
from dotenv import load_dotenv
# import asyncpg

import discord
from discord.ext import commands


load_dotenv("./config/.env")


def setup_logger():
    logger = logging.getLogger()
    with open("config/logging.yml", "r") as log_config:
        config = yaml.safe_load(log_config)
    coloredlogs.install(
        level="INFO",
        logger=logger,
        fmt=config["formats"]["console"],
        datefmt=config["formats"]["datetime"],
        level_styles=config["levels"],
        field_styles=config["fields"],
    )
    return logger


class Bot(commands.Bot):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            intents=discord.Intents.default(),
            command_prefix="!",
            help_command=None
        )
        self.start_time = kwargs.pop("start_time")
        # self.pool = kwargs.pop("pool")

        setup_logger()
        self.log = logging.getLogger("Bot")
        self.log.setLevel(logging.INFO)
        self.discord_log = logging.getLogger("discord")
        self.discord_log.setLevel(logging.INFO)
        self.color = discord.Color.purple()

    async def on_connect(self):
        self.log.info("Connected to Discord")
        await self.change_presence(
            activity=discord.Activity(
                name="Starting Up",
                type=discord.ActivityType.playing
            ),
            status=discord.Status.dnd
        )

        # Cog loader
        for file in listdir('./cogs'):
            if file.endswith('.py'):
                if file.startswith("_"):
                    continue
                else:
                    await client.load_extension(f'cogs.{file[:-3]}')
                    client.log.info(f"cogs.{file[:-3]} loaded")

        for file in listdir('./utils'):
            if file.endswith('.py'):
                if file.startswith('_'):
                    continue
                try:
                    await client.load_extension(f'utils.{file[:-3]}')
                    client.log.info(f"utils.{file[:-3]} loaded")
                except commands.NoEntryPointError:
                    pass

    async def on_ready(self):
        self.log.info("Bot is online")
        self.log.info(f"Guild count: {len(self.guilds)}")
        await self.change_presence(
            activity=discord.Game(
                "with buggy code"
            ),
            status=discord.Status.online
        )

        self.log.info("Starting application commands sync")
        synced = await self.tree.sync()
        self.log.info(f"Application commands synced ({len(synced)} commands)")
        

async def run():
    # pool = await asyncpg.create_pool(
    #     host = getenv("db_host"),
    #     port = getenv("db_port"),
    #     user = getenv("db_user"),
    #     password = getenv("db_password"),
    #     database = getenv("db_database")
    # )
    bot = Bot(
        # pool=pool
        start_time=datetime.datetime.utcnow()
    )
    bot.log.info("Bot is setup. Ready for login")
    return bot


async def stop():
    client.log.info("Shutdown received.")
    await client.close()
    # await client.pool.close()
    client.log.info("Goodbye cruel world :(")
    exit(0)


loop = asyncio.get_event_loop()
client = loop.run_until_complete(run())


if __name__ == "__main__":
    try:
        client.log.info("Establishing connection to Discord")
        loop.run_until_complete(client.start(getenv("token"))) # type: ignore
    except KeyboardInterrupt:
        loop.run_until_complete(stop())
    finally:
        loop.close()