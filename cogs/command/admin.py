import discord
from core.cog_class import Cog_basic
from discord.ext import commands

def is_admin(ctx):
    for role in ctx.author.roles:
        if 969962769854128240 == role.id:
            return True
    return False


class Admin(Cog_basic):

    @commands.Command
    @commands.check(is_admin)
    async def say(self, ctx:commands.Context, channel:discord.TextChannel, msg):
        await ctx.message.delete()
        await channel.send(msg)


def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))