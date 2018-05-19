from discord.ext import commands
import discord
import random


class Text:
    """General purpose text responses,"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def booty(self, ctx):
        """Degeneracy incarnate.!"""
        await ctx.send(content='booty')

    @commands.command()
    async def mimic(self, ctx, *, content: str):
        """Repeat after me!"""
        await ctx.send(content=content)

    @commands.command()
    async def reverse(self, ctx, *, content: str):
        """Reverse text."""
        await ctx.send(content=content[::-1])

    @commands.command()
    async def repeat(self, ctx, times: int, *, content: str):
        """Repeat after me many times! max of 10 times."""
        if times <= 5:
            for i in range(times):
                await ctx.send(content=content)
        else:
            await ctx.send('dude, chill (too many times, max of 10)')

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)


def setup(bot):
    bot.add_cog(Text(bot))
