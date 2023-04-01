from discord.app_commands import CheckFailure


class Error(CheckFailure):
    pass


class NotBotOwner(Error):
    pass


class NotGuildOwner(Error):
    pass


class NotGuildAdmin(Error):
    pass


class NotNSFW(Error):
    pass
