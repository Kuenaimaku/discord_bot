from discord.ext import commands
from discord.utils import find

import asyncio

class channels:
    """channel control."""

    def __init__(self, bot):
        self.bot = bot
        self.channel = ["announcements","news","nsfw"]

    @commands.command(pass_context=True)
    async def sub(self, ctx, *, content: str = 'none'):
        """Join the specified channel."""
        if content == 'none' or content.lower() not in self.channel:
            message = ctx.message.channel.send("Invalid channel specified.")
            await asyncio.sleep(5)
            await message.delete()
            await ctx.message.delete()
        else:
            role = find(lambda r: r.name.lower() == content, ctx.message.guild.roles)
            await ctx.message.author.add_roles(role)
            message = await ctx.message.channel.send("You have joined the `{0}` channel.".format(content.lower()))
            await asyncio.sleep(5)
            await message.delete()
            await ctx.message.delete()

    @commands.command(pass_context=True)
    async def unsub(self, ctx, *, content: str = 'none'):
        """Leave the specified channel."""
        if content == 'none' or content.lower()  not in self.channel:
            message = await ctx.message.channel.send("Invalid channel specified.")
            await asyncio.sleep(5)
            await message.delete()
            await ctx.message.delete()
        else:
            role = find(lambda r: r.name.lower() == content.lower(), ctx.message.guild.roles)
            await ctx.message.author.remove_roles(role)
            message = await ctx.message.channel.send("You have left the `{0}` channel.".format(content.lower()))
            await asyncio.sleep(5)
            await message.delete()
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(channels(bot))
