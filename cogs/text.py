from discord.ext import commands
import discord


class Text:
    """General purpose text responses,"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mimic(self, ctx, *, content: str):
        """Repeat after me!"""
        await ctx.send(content=content)

    @commands.command()
    async def repeat(self, ctx, times: int, *, content: str):
        """Repeat after me many times! max of 10 times."""
        if times <= 5:
            for i in range(times):
                await ctx.send(content=content)
        else:
            await ctx.send('dude, chill (too many times, max of 10)')


def setup(bot):
    bot.add_cog(Text(bot))
