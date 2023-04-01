import sys
from os import getenv
import datetime
import time

import discord
from discord.ext import commands
from discord import app_commands, Interaction

from utils.formatters import uptime
from utils.predicates import *


class General(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Some bot statistics')
    async def stats(self, interaction: Interaction):
        embed = discord.Embed(
            title='Stats',
            color=discord.Color.green()
        )
        embed.add_field(
            name='Version',
            value='Python: `{0.major}.{0.minor}.{0.micro}`\n'
                  'discord.py: `{1}`'.format(sys.version_info, discord.__version__),
            inline=True
        )
        stats = f'Servers: {len(self.bot.guilds)}\nUsers: {len(self.bot.users)}'
        embed.add_field(name='Statistics', value=stats, inline=True)
        t_owners = [await self.bot.fetch_user(i) for i in [int(i) for i in getenv("owners").split(",")]] # type: ignore
        f_owners = []
        for user in t_owners:
            f_owners.append(f'{user.name}#{user.discriminator}')
        embed.add_field(name='Owners', value="\n".join(f_owners), inline=True)
        embed.add_field(name='Uptime', value=uptime(interaction), inline=False)
        embed.add_field(name="Version", value=getenv("version"), inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def ping(self, interaction: Interaction):
        embed = discord.Embed(
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow(),
            title="Ping!",
        )
        before = time.monotonic()
        await interaction.response.send_message(embed=embed)
        _ping = (time.monotonic() - before) * 1000
        embed.title = f"Ping! {int(_ping)}"
        await interaction.edit_original_response(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))