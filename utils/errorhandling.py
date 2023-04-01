import traceback
import datetime
from os import getenv

import discord
from discord.ext import commands
from discord import app_commands, Interaction

from utils.formatters import cooldown_formatter, error_formatter
from utils.exceptions import *


class ErrorHandling(commands.Cog):

    
    
    def __init__(self, bot):
        self.bot = bot
        bot.tree.error(coro = self.__dispatch_to_app_command_handler)
        self.default_error_embed = discord.Embed(
            title="An error occured",
            description="Generating error message",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )

    async def __dispatch_to_app_command_handler(self, interaction: Interaction, error: app_commands.AppCommandError):
        self.bot.dispatch("app_command_error", interaction, error)

    async def __respond_to_interaction(self, interaction: Interaction) -> None:
        try:
            return await interaction.response.send_message(embed=self.default_error_embed, ephemeral=True)
        except discord.errors.InteractionResponded:
            return
    

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: Interaction, error: app_commands.AppCommandError):
        await self.__respond_to_interaction(interaction)
        edit = interaction.edit_original_response

        if isinstance(error, app_commands.CommandNotFound):
            embed = discord.Embed(
                    title="This is weird...",
                    description="The command either does not exist anymore, or something else broke.\n"
                                "Please try again later, maybe it will work again soon.",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
            await edit(embed=embed)

        elif isinstance(error, app_commands.CheckFailure):
            if isinstance(error, NotNSFW):
                embed = discord.Embed(
                    title='You are horny!',
                    description='This command can only be used in NSFW Channels!',
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                await edit(embed=embed)
            elif isinstance(error, NotBotOwner):
                embed = discord.Embed(
                    title='OwO, what\'s this???',
                    description='This command is an owner only command, and can not be executed by ANYONE else!\n'
                                'Don\'t you try to use it again, because it won\'t work.'
                                'Or else the owner might hurt you! ||jk jk||',
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                await edit(embed=embed)
            elif isinstance(error, NotGuildOwner):
                embed = discord.Embed(
                    title='Oi mate!',
                    description='This command can only be used by the Server Owner!',
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                await edit(embed=embed)
            elif isinstance(error, NotGuildAdmin):
                embed = discord.Embed(
                    title='Oi mate!',
                    description='This command can only be used by Server Admins!',
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                await edit(embed=embed)

        elif isinstance(error, app_commands.CommandOnCooldown):
            cooldown = cooldown_formatter(error.retry_after)
            embed = discord.Embed(
                title='Cooldown',
                description=f'Please wait {cooldown} until you can use the {interaction.command} command again.',
                color=discord.Color.orange(),
                timestamp=datetime.datetime.utcnow()
            )
            await edit(embed=embed)

        else:
            await edit(embed=error_formatter(interaction, f'{type(error).__name__}: {error}', True))
            self.bot.log.error(f'Occurred in {interaction.guild}, in {interaction.channel} by user {interaction.user}')
            self.bot.log.error(f'Ignoring exception in command {interaction.command.name}:') # type: ignore
            error_formatted = traceback.format_exception(type(error), error, error.__traceback__)
            error_concat = ''.join(error_formatted)
            self.bot.log.error(error_concat)
            channel = self.bot.get_channel(int(getenv("error_log_channel"))) # type: ignore
            embed = discord.Embed(
                title='>w< That\'s not good',
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name='Guild', value=interaction.guild)
            embed.add_field(name='Channel', value=interaction.channel)
            embed.add_field(name='Author', value=interaction.user)
            await channel.send(
                f'```py\n{"".join(error_concat)[:1990 if len(error_concat) > 1990 else len(error_concat)]}\n```',
                embed=embed
            )


async def setup(bot):
    await bot.add_cog(ErrorHandling(bot))
