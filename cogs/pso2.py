from collections import OrderedDict
from datetime import datetime, timedelta
from discord.ext import commands
from discord.utils import find

import asyncio
import aiohttp
import async_timeout
import discord

class pso2:
    """Phantasy Star Online 2 tools"""
    def __init__(self, bot):
        self.bot = bot
        self.session = bot._session

    async def _fetch(self, session, url):
        with async_timeout.timeout(10):
            async with session.get(url) as response:
                return await response.json()

    @commands.group()
    async def pso2(self, ctx):
        """Phantasy Star Online 2 commands."""
        if ctx.invoked_subcommand is None:
            await self.bot.say('No subcommand provided.')

    @pso2.command(pass_context=True)
    async def info(self, ctx):
        """Basic information on Download and Installation"""
        em = discord.Embed(title='Phantasy Star Online 2', description='Information', color=0x0D2E35)
        em.set_thumbnail(url='https://pbs.twimg.com/profile_images/579525248644575232/sQRTI87P.png')
        em.add_field(name="Information", value="[News](http://bumped.org/psublog)\n[Reddit](http://reddit.com/r/pso2)\n[PSO-World](http://pso-world.com)\n[Wiki](http://pso2.swiki.jp)")
        em.add_field(name="Downloads", value="[English Launcher](http://arks-layer.com/)\n[Signup Guide](http://arks-layer.com/signup.php)")
        await ctx.send(embed=em)

    @pso2.command(pass_context=True)
    async def status(self, ctx):
        """Return ship status."""
        async with aiohttp.ClientSession() as session:
            status = await self._fetch(session, 'http://kakia.org/pso2_status.json')
        status = OrderedDict(sorted(status.items(), key=lambda item: item[1]["Ship"]))
        em = discord.Embed(title='Phantasy Star Online 2', description='Ship Status', color=0x0D2E35)
        em.set_thumbnail(url='https://pbs.twimg.com/profile_images/579525248644575232/sQRTI87P.png')
        for key, value in status.items():
            if value["StatusValue"] == 1:
                em.add_field(name="{0}: ✅️".format(value["Ship"]), value="\u200b", inline="True")
        await ctx.send(embed=em)

    @pso2.command()
    async def daily(self, ctx):
        """"""
        # http://pso2.rodrigo.li/daily

    @pso2.command()
    async def eq(self, ctx):
        """"""
        # http://pso2.rodrigo.li/eq

    @pso2.command(pass_context=True)
    async def item(self, ctx, *, search_string: str):
        """Item Search"""
        page_control = ["⏮", "⏪", "◀", "⏹", "▶", "⏩", "⏭"]
        current_page = 0
        async with aiohttp.ClientSession() as session:
            item_result = await self._fetch(session, 'http://db.kakia.org/item/search?name={0}'.format(search_string))
        wait_for_response = True
        em = discord.Embed(title='Phantasy Star Online 2', description='Item Search Results', color=0x0D2E35)
        em.set_thumbnail(url='https://pbs.twimg.com/profile_images/579525248644575232/sQRTI87P.png')
        em.add_field(name=item_result[current_page]["EnName"], value=item_result[current_page]["JpName"], inline=False)
        description = "{0} \n---\n {1}".format(item_result[current_page]["EnDesc"],
                                               item_result[current_page]["JpDesc"]).replace("<br>", "\n")
        em.add_field(name="Description", value=description, inline=False)
        price_info = ""
        sorted_price_info = sorted(item_result[current_page]["PriceInfo"], key=lambda k: k["Ship"])
        for dict in sorted_price_info:
            price_info += "Ship {0}: {1:,} ({2})\n".format(str(dict["Ship"]).zfill(2), dict["Price"],
                                                           dict["LastUpdated"])
        em.add_field(name="Price Tracker", value="```{0}```".format(price_info), inline=True)
        em.set_footer(text="Page {} / {}".format(current_page + 1, len(item_result)))
        message = await ctx.message.channel.send(embed=em)
        for emoji in page_control:
            await message.add_reaction(str(emoji))

        def check(r, m):
            return ctx.author == m and r.me
            # User has selected their action based on reaction

        while wait_for_response:
            try:
                reaction, member = await self.bot.wait_for('reaction_add', check=check, timeout=120.0)
                print(reaction)
            except asyncio.TimeoutError:
                wait_for_response = False
                try:
                    await message.clear_reactions()
                except:
                    pass
                finally:
                    break
            try:
                await message.remove_reaction(reaction, member)
            except:
                pass
            if reaction.emoji == "⏮":
                print("GOTO First Page")
                current_page = 0
            elif reaction.emoji == "⏪":
                print("BACK 10 pages")
                current_page -= 10
                if current_page < 0: current_page = 0
            elif reaction.emoji == "◀":
                print("GOTO Previous Page")
                current_page -= 1
                if current_page < 0: current_page = 0
            elif reaction.emoji == "⏹":
                print("Stop Pagination")
                await message.clear_reactions()
                wait_for_response = False
            elif reaction.emoji == "▶":
                print("GOTO Next Page")
                current_page += 1
                if current_page > len(item_result) - 1: current_page = len(item_result) - 1
            elif reaction.emoji == "⏩":
                print("FORWARD 10 Pages")
                current_page += 10
                if current_page > len(item_result) - 1: current_page = len(item_result) - 1
            elif reaction.emoji == "⏭":
                print("GOTO Last Page")
                current_page = len(item_result) - 1
            else:
                pass
            print("{} / {}".format(current_page, len(item_result) - 1))
            em.clear_fields()
            em.add_field(name=item_result[current_page]["EnName"], value=item_result[current_page]["JpName"],
                         inline=False)
            description = "{0} \n---\n {1}".format(item_result[current_page]["EnDesc"],
                                                   item_result[current_page]["JpDesc"]).replace("<br>", "\n")
            em.add_field(name="Description", value=description, inline=False)
            price_info = ""
            sorted_price_info = sorted(item_result[current_page]["PriceInfo"], key=lambda k: k["Ship"])
            if sorted_price_info:
                for dict in sorted_price_info:
                    price_info += "Ship {0}: {1:,} ({2})\n".format(str(dict["Ship"]).zfill(2), dict["Price"],
                                                                   dict["LastUpdated"])
                em.add_field(name="Price Tracker", value="```{0}```".format(price_info), inline=True)
            else:
                em.add_field(name="Price Tracker", value="No pricing information found.", inline=True)
            em.set_footer(text="Page {} / {}".format(current_page + 1, len(item_result)))
            await message.edit(embed=em)



def setup(bot):
    bot.add_cog(pso2(bot))
