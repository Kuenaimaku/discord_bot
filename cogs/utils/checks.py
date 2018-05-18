from discord.ext import commands
import discord.utils


def check_permissions(ctx, perms):
    msg = ctx.message
    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True
    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None


def is_in_channel(channel_names):
    def predicate(ctx):
        channel = str(ctx.message.channel.name).lower()
        if channel is None:
            return False
        return channel in channel_names.lower()
    return commands.check(predicate)


def has_role(role_name):
    def predicate(ctx):
        role_list=[]
        roles = ctx.message.author.roles
        for x in roles:
            role_list.append(x.name)
        if roles is None:
            return False
        return role_name in role_list
    return commands.check(predicate)


def mod_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name in ('Bot Mod', 'Bot Admin'), **perms)