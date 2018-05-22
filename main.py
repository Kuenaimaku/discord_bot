from discord.ext import commands
from discord.utils import find
from cogs.utils import directory
import configparser
import discord
import json
import aiohttp

parser = configparser.ConfigParser()
parser.read('config/userconfig.ini')

description = """Discord Stream Server Manager"""

bot = commands.Bot(command_prefix='~', description=description, self_bot=False)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game('Testing Rewrite'))
    for guild in bot.guilds:
        directory.touch('storage/{0}'.format(guild.id))
        _r = find(lambda r: r.permissions.administrator, guild.roles)
        if type(_r) == discord.Role:
            _r = [_r]
        if _r:
            role_ids = [r.id for r in _r]
            with open('storage/{0}/admin.json'.format(guild.id), 'w') as f:
                json.dump(role_ids, fp=f)


@bot.event
async def on_member_join(member):
    # Add the regular role to whoever joins
    regular = find(lambda r: r.name.lower() == 'hidden leaf dojo(regulars/followers)', member.guild.roles)
    await member.add_roles(regular)


@bot.event
async def on_member_remove(member):
    # Log whoever left to the moderator channel
    audit_channel = find(lambda c: c.name.lower() == 'audit_log', member.guild.channels)
    if audit_channel:
        await audit_channel.send('{0.display_name} ({0.name} #{0.discriminator}) has left the server.'.format(member))

initial_extensions = [
    'cogs.tags',
    'cogs.image',
    'cogs.sound',
    'cogs.text',
    'cogs.kitsu',
    'cogs.pso2'
]

if __name__ == '__main__':
    bot._session = aiohttp.ClientSession()
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    bot.run(parser.get('discord', 'token'))
