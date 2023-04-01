from discord import Interaction
from discord.app_commands import check

import utils.checks as checks
from utils.exceptions import *


def bot_owner():
    async def predicate(ineraction: Interaction):
        if checks.bot_owner(ineraction):
            return True
        else:
            raise NotBotOwner()
    return check(predicate)


def guild_owner():
    async def predicate(ineraction: Interaction):
        if checks.guild_owner(ineraction):
            return True
        else:
            raise NotGuildOwner()
    return check(predicate)


def guild_admin():
    async def predicate(ineraction: Interaction):
        if checks.guild_admin(ineraction):
            return True
        else:
            raise NotGuildAdmin()
    return check(predicate)


def nsfw():
    async def predicate(interaction: Interaction):
        if checks.is_nsfw(interaction):
            return True
        else:
            raise NotNSFW()
    return check(predicate)
