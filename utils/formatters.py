import datetime
import discord
from discord import Interaction
import math


# Date String Formatter
def date_string(time, unit):
    time = int(time)
    if time == 1:
        if unit == 'second':
            return f'1 {unit}'
        else:
            return f'1 {unit},'
    elif time == 0:
        return ''
    else:
        if unit == 'second':
            return f'{time} {unit}s'
        return f'{time} {unit}s,'


# Uptime formatter
def uptime(interaction: Interaction):
    elapsedTime = datetime.datetime.utcnow() - interaction.client.start_time # type: ignore
    days = divmod(elapsedTime.total_seconds(), 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)

    dt = date_string(days[0], 'day')
    ht = date_string(hours[0], 'hour')
    mt = date_string(minutes[0], 'minute')
    st = date_string(seconds[0], 'second')

    times_before = [dt, ht, mt, st]
    times_after = []

    for time_unit in times_before:
        if time_unit == '':
            continue
        else:
            times_after.append(time_unit)

    if len(times_after) == 1:
        return times_after[0]
    else:
        beginning = ' '.join(times_after[:-1])
        end = f' and {times_after[-1]}'

        return f'{beginning}{end}'


# Cooldown formatter
def cooldown_formatter(cooldown):
    cooldown = round(cooldown)
    days = math.floor(cooldown / 86400)
    hours = math.floor(cooldown / 3600) - (days * 24)
    minutes = math.floor(cooldown / 60) - (hours * 60) - (days * 24 * 60)
    seconds = cooldown - (minutes * 60) - (hours * 3600) - (days * 86400)
    dt = date_string(days, 'day')
    ht = date_string(hours, 'hour')
    mt = date_string(minutes, 'minute')
    st = date_string(seconds, 'second')

    times_before = [dt, ht, mt, st]
    times_after = []

    for time_unit in times_before:
        if time_unit == '':
            continue
        else:
            times_after.append(time_unit)

    if len(times_after) == 1:
        return times_after[0]
    else:
        beginning = ' '.join(times_after[:-1])
        end = f' and {times_after[-1]}'

        return f'{beginning}{end}'


def error_formatter(interaction: Interaction, error, notify=True):
    embed = discord.Embed(
        title='God damn it Karen!',
        description=f'An error has occurred in the {interaction.command.name} command!\n' # type: ignore
                    f'{"The devs have been notified!" if notify else ""}',
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(
        name='Error in command',
        value=f'```py\n{error}\n```'
    )

    return embed
