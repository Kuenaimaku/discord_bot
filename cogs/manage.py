from .utils import directory, checks
from discord.ext import commands
import discord
import configparser

class Tag:
    """Moderator-created Text Commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def manage(self, ctx):
        """"""
        if ctx.invoked_subcommand is None:
            await self.bot.say('No subcommand provided.')

    @manage.commmand()
    async def add_role(self, ctx, name: str):
        """Add role to list of editors for the bot"""
        # Get role based on name
        # Read in mod role json file from /storage
        # compare role to list of mod ids
        # if absent, add it

    @manage.command()
    async def remove_role(self, ctx, name: str):
        """remove role to list of editors for the bot"""
        # Get role based on name
        # Read in mod role json file from /storage
        # compare role to list of mod ids
        # if absent, add it



def setup(bot):
    bot.add_cog(Tag(bot))
