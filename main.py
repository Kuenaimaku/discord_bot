from discord.ext import commands
from discord.utils import find
import configparser
import discord

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



@bot.event
async def on_member_join(member):
    # Add the regular role to whoever joins
    regular = find(lambda r: r.name.lower() == 'hidden leaf dojo(regulars/followers)', member.guild.roles)
    await member.add_roles(regular)

initial_extensions = [
    'cogs.tags',
    'cogs.image',
    'cogs.text'
]

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    bot.run(parser.get('discord', 'token'))
