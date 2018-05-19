from .utils import kitsu_client, season
from discord.ext import commands
from datetime import datetime
import aiohttp
import discord
import configparser


class Kitsu:
    """Various features enabled by the use of the kitsu API."""
    def __init__(self, bot):
        parser = configparser.ConfigParser()
        parser.read('config/userconfig.ini')
        self.bot = bot
        self.kitsu_client = kitsu_client.KitsuClient(client_id=parser.get('kitsu', 'client_id'),
                                                     client_secret=parser.get('kitsu', 'client_secret'),
                                                     session=self.bot._session)

    @commands.group()
    async def kitsu(self, ctx):
        """"""
        if ctx.invoked_subcommand is None:
            await ctx.message.channel.send("Incorrect kitsu subcommand passed.")

    # @kitsu.command()
    # async def user(self, ctx, name: str = None):
    #     """"""
    #     if name:
    #         user = await self.kitsu_client.get_users(username=name)
    #         await ctx.message.channel.send(user)
    #     else:
    #         await ctx.message.channel.send("No kitsu username was passed.")

    @kitsu.command()
    async def anime(self, ctx, *, text: str = None):
        """Returns first Anime found base on name."""
        if text:
            anime = await self.kitsu_client.get_anime(text=text)
        else:
            await ctx.message.channel.send("No kitsu text was passed.")
        anime['categories'] = await self.kitsu_client._fetch(anime['relationships']['categories']['links']['related'])
        anime['categories'] = ', '.join([c['attributes']['title'] for c in anime['categories']])
        if anime['attributes']['startDate']:
            anime['attributes']['startDate'] = datetime.strptime(anime['attributes']['startDate'], '%Y-%m-%d').date()
        if anime['attributes']['endDate']:
            anime['attributes']['endDate'] = datetime.strptime(anime['attributes']['endDate'], '%Y-%m-%d').date()
        anime
        _e = discord.Embed(title='{0} [{1}]'.format(anime['attributes']['titles']['en_jp'], anime['attributes']['subtype'].capitalize()),
                           description=anime['attributes']['titles']['ja_jp'], color=discord.Color.dark_orange(),
                           url='https://kitsu.io/anime/{0}'.format(anime['attributes']['slug']))
        _e.set_thumbnail(url='https://pbs.twimg.com/profile_images/807964865511862278/pIYOVdsl_400x400.jpg')
        _e.add_field(name='Synopsis', value='{0}...'.format(anime['attributes']['synopsis'][:400]), inline=False)
        _e.add_field(name='Status: {0}'.format(anime['attributes']['status'].capitalize()),
                     value='📅 {0} {1}\n🎞️ {2} Episodes'.format(
                         season.get_season(anime['attributes']['startDate']).capitalize(),
                         anime['attributes']['startDate'].strftime('%Y'), anime['attributes']['episodeCount']))
        _e.add_field(name='Kitsu Rankings',
                     value='❤️#{0} (Most Popular)\n⭐ #{1} (Highest Rated) '.format(
                         anime['attributes']['popularityRank'], anime['attributes']['ratingRank']))
        _e.set_footer(text='{0}'.format(anime['categories']))
        _e.set_image(url=anime['attributes']['posterImage']['original'])
        await ctx.message.channel.send(embed=_e)

    @kitsu.command()
    async def manga(self, ctx, *, text: str = None):
        """Returns first Anime found base on name."""
        if text:
            manga = await self.kitsu_client.get_manga(text=text)
        else:
            await ctx.message.channel.send("No kitsu text was passed.")
        manga['categories'] = await self.kitsu_client._fetch(manga['relationships']['categories']['links']['related'])
        manga['categories'] = ', '.join([c['attributes']['title'] for c in manga['categories']])
        if manga['attributes']['startDate']:
            manga['attributes']['startDate'] = datetime.strptime(manga['attributes']['startDate'], '%Y-%m-%d').date()
        if manga['attributes']['endDate']:
            manga['attributes']['endDate'] = datetime.strptime(manga['attributes']['endDate'], '%Y-%m-%d').date()
        manga
        _e = discord.Embed(title='{0} [{1}]'.format(manga['attributes']['canonicalTitle'],
                                                    manga['attributes']['subtype'].capitalize()),
                           description=manga['attributes']['serialization'], color=discord.Color.dark_orange(),
                           url='https://kitsu.io/manga/{0}'.format(manga['attributes']['slug']))
        _e.set_thumbnail(url='https://pbs.twimg.com/profile_images/807964865511862278/pIYOVdsl_400x400.jpg')
        _e.add_field(name='Synopsis', value='{0}...'.format(manga['attributes']['synopsis'][:400]), inline=False)
        _e.add_field(name='Status: {0}'.format(manga['attributes']['status'].capitalize()),
                     value='📅 {0} {1}\n📚️ {2} Chapters'.format(
                         season.get_season(manga['attributes']['startDate']).capitalize(),
                         manga['attributes']['startDate'].strftime('%Y'), manga['attributes']['chapterCount']))
        _e.add_field(name='Kitsu Rankings',
                     value='❤️#{0} (Most Popular)\n⭐ #{1} (Highest Rated) '.format(
                         manga['attributes']['popularityRank'], manga['attributes']['ratingRank']))
        _e.set_footer(text='{0}'.format(manga['categories']))
        _e.set_image(url=manga['attributes']['posterImage']['original'])
        await ctx.message.channel.send(embed=_e)


def setup(bot):
    bot.add_cog(Kitsu(bot))
