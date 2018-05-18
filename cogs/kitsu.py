from .utils import kitsu_client
from discord.ext import commands
import discord
import configparser


class Kitsu:
    """Various features enabled by the use of the kitsu API."""
    def __init__(self, bot):
        parser = configparser.ConfigParser()
        parser.read('config/userconfig.ini')
        self.bot = bot
        self.kitsu_client = kitsu_client.KitsuClient(client_id=parser.get('kitsu', 'client_id'),
                                                     client_secret=parser.get('kitsu', 'client_secret'))

    @commands.group()
    async def kitsu(self, ctx):
        """"""
        if ctx.invoked_subcommand is None:
            await ctx.message.channel.send("Incorrect kitsu subcommand passed.")

    @kitsu.command()
    async def user(self, ctx, content: str = None):
        """"""
        if content:
            user = await self.kitsu_client.get_users(username=content)
            await ctx.message.channel.send(content)
        else:
            await ctx.message.channel.send("No kitsu username was passed.")

def setup(bot):
    bot.add_cog(Kitsu(bot))
