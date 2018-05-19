from .utils import directory, checks
from discord.ext import commands
import discord
from urllib import request
import os
import configparser

import async_timeout
import asyncio
import aiohttp


class Image:
    """Moderator-created Image Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot._session

    @commands.group(invoke_without_command=True)
    async def image(self, ctx, name: str = None):
        """"""
        _base_directory = 'storage/{0}/images/'.format(str(ctx.guild.id))
        directory.touch(_base_directory)
        images = directory.list_files(_base_directory)
        filename = next((x for x in images if x == '{0}'.format(name)), None)
        if filename:
                extension = directory.get_extension_from_filename(_base_directory, filename)
                await ctx.send(file=discord.File('{0}{1}{2}'.format(_base_directory, filename, extension)))
        else:
            await ctx.send('Image `{0}` does not exist (did you mean to `create` this audio?).'.format(name))

    @image.command(aliases=['add'])
    @checks.has_role('ANBU( Mods)')
    async def create(self, ctx, name: str):
        """save audio with the name of 'name'"""
        _base_directory = 'storage/{0}/images/'.format(str(ctx.guild.id))
        directory.touch(_base_directory)
        images = directory.list_files(_base_directory)
        filename = next((x for x in images if x == '{0}'.format(name)), None)
        if filename:
            await ctx.send('Image `{0}` already exists (did you mean to `edit` this audio?)'.format(name))
        else:
            for attachment in ctx.message.attachments:
                _url = str(attachment.proxy_url)
                fn, extension = os.path.splitext(_url)
                with async_timeout.timeout(10):
                    async with self.session.get(url=_url) as r:
                        try:
                            with open('{0}{1}{2}'.format(_base_directory, name, extension), "wb") as local_file:
                                local_file.write(await r.read())
                        except(asyncio.TimeoutError, aiohttp.ClientResponseError):
                            pass  # raise client error
            await ctx.send('Image `{0}` created.'.format(name))

    @image.command(aliases=['remove'])
    @checks.has_role('ANBU( Mods)')
    async def delete(self, ctx, name: str):
        """remove audio 'name' if it exists"""
        _base_directory = 'storage/{0}/images/'.format(str(ctx.guild.id))
        directory.touch(_base_directory)
        images = directory.list_files(_base_directory)
        filename = next((x for x in images if x == '{0}'.format(name)), None)
        if filename:
            extension = directory.get_extension_from_filename(_base_directory, filename)
            directory.remove_file('{0}{1}{2}'.format(_base_directory, filename, extension))
            await ctx.send('Image `{0}` deleted.'.format(name))
        else:
            await ctx.send('Image `{0}` not found.'.format(name))

    @image.command(aliases=['update'])
    @checks.has_role('ANBU( Mods)')
    async def edit(self, ctx, name: str):
        """edit audio 'name' with attached audio"""
        _base_directory = 'storage/{0}/images/'.format(str(ctx.guild.id))
        directory.touch(_base_directory)
        images = directory.list_files(_base_directory)
        filename = next((x for x in images if x == '{0}'.format(name)), None)
        if filename:
            for attachment in ctx.message.attachments:
                _url = str(attachment.proxy_url)
                fn, extension = os.path.splitext(_url)
                with async_timeout.timeout(10):
                    async with self.session.get(url=_url) as r:
                        try:
                            with open('{0}{1}{2}'.format(_base_directory, name, extension), "wb") as local_file:
                                local_file.write(await r.read())
                        except(asyncio.TimeoutError, aiohttp.ClientResponseError):
                            pass  # raise client error
                await ctx.send('Image `{0}` edited.'.format(name))
        else:
            await ctx.send('Image `{0}` does not exist (did you mean to `create` this audio?)'.format(name))


def setup(bot):
    bot.add_cog(Image(bot))
