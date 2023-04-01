from os import getenv
from discord import Interaction
from discord.abc import GuildChannel
from discord.app_commands import Command


def guild(interaction: Interaction):
    return isinstance(interaction.channel, GuildChannel)


def bot_owner(interaction: Interaction):
    return interaction.user.id in [int(i) for i in getenv("owners").split(",")] # type: ignore


def guild_owner(interaction: Interaction):
    if guild(interaction):
        return interaction.user == interaction.guild.owner # type: ignore


def guild_admin(interaction: Interaction):
    if guild(interaction):
        return interaction.channel.permissions_for(interaction.guild.get_member(interaction.user.id)).administrator # type: ignore
    

def is_nsfw(interaction: Interaction):
    if guild(interaction):
        return interaction.channel.nsfw == True # type: ignore
