from .utils import directory, checks
from discord.ext import commands
import discord
import configparser


class Tag:
    """Moderator-created Text Commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, name: str = None):
        """Text on demand."""
        _base_directory = 'storage/{0}/tags/'.format(str(ctx.guild.id))
        directory.touch(_base_directory)
        tags = directory.list_files(_base_directory)
        file = next((x for x in tags if x == '{0}'.format(name)), None)
        if file:
            with open('{0}{1}.txt'.format(_base_directory, name), "rb") as _f:
                content = _f.read().decode('utf8')
                if content:
                    await ctx.send(content)
        else:
            await ctx.send('Tag `{0}` does not exist (did you mean to `create` this tag?).'.format(name))

    @checks.has_role('ANBU ( Mods)')
    @tag.command(aliases=['add'])
    async def create(self, ctx, name: str, *, content: str):
        """Add content to tag with the name of 'name'"""
        _base_directory = 'storage/{0}/tags/'.format(str(ctx.guild.id))
        directory.touch(_base_directory)
        tags = directory.list_files(_base_directory)
        file = next((x for x in tags if x == '{0}'.format(name)), None)
        if file:
            await ctx.send('Tag `{0}` already exists (did you mean to `edit` this tag?)'.format(name))
        else:
            _f = open('{0}{1}.txt'.format(_base_directory, name), "wb")
            _f.write(content.encode('utf8'))
            _f.close()
            await ctx.send('Tag `{0}` created.'.format(name))

    @checks.has_role('ANBU ( Mods)')
    @tag.command(aliases=['remove'])
    async def delete(self, ctx, name: str):
        """remove tag 'name' if it exists"""
        _base_directory = 'storage/{0}/tags/'.format(str(ctx.guild.id))
        directory.touch(_base_directory)
        tags = directory.list_files(_base_directory)
        file = next((x for x in tags if x == '{0}'.format(name)), None)
        if file:
            directory.remove_file('{0}{1}.txt'.format(_base_directory, name))
            await ctx.send('Tag `{0}` deleted.'.format(name))
        else:
            await ctx.send('Tag `{0}` not found.'.format(name))

    @checks.has_role('ANBU ( Mods)')
    @tag.command(aliases=['update'])
    async def edit(self, ctx, name: str, *, content: str):
        """edit tag 'name' with content 'content'"""
        _base_directory = 'storage/{0}/tags/'.format(str(ctx.guild.id))
        directory.touch(_base_directory)
        tags = directory.list_files(_base_directory)
        file = next((x for x in tags if x == '{0}'.format(name)), None)
        if file:
            _f = open('{0}{1}.txt'.format(_base_directory, name), "wb")
            _f.write(content.encode('utf8'))
            _f.close()
            await ctx.send('Tag `{0}` edited.'.format(name))
        else:
            await ctx.send('Tag `{0}` does not exist (did you mean to `create` this tag?)'.format(name))

    @tag.command(aliases=['list'])
    async def search(self, ctx, name: str=None):
        """Add content to tag with the name of 'name'"""
        _base_directory = 'storage/{0}/tags/'.format(str(ctx.guild.id))
        directory.touch(_base_directory)
        tags = directory.list_files(_base_directory)
        filtered_tags = [x for x in tags if name in '{0}'.format(x)]
        if filtered_tags and len(filtered_tags) > 1:
            await ctx.send('Multiple tags found:\n`{0}`'.format('\n'.join(filtered_tags)))
        elif filtered_tags:
            await ctx.send('One tag found:\n`{0}`'.format('\n'.join(filtered_tags)))
        else:
            await ctx.send('No tags with `{0}` exist.'.format(name))

def setup(bot):
    bot.add_cog(Tag(bot))
