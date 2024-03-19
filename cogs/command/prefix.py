from core.cog_class import Cog_basic

import discord
from discord.ext import commands
from random import choice, randint

class Prefix(Cog_basic):

    @commands.command(name="choose", description="Random choose one of the options")
    async def choose(self, ctx: commands.Context, *args):
        if len(args) == 0:
            return
        await ctx.reply(choice(args))
        return

    @commands.command(name="random", description="Random choose a number in range")
    async def random(self, ctx: commands.Context, start: int, end: int):
        if start > end:
            return
        await ctx.reply(randint(start, end))
        return

    @commands.command(name="say", description="Make the bot say something quote from the member who use this command")
    async def say(self, ctx: commands.Context, *, args):
        await ctx.message.delete()
        await ctx.send(f">>> {args}\n   by {ctx.author.mention}")
        return

def setup(bot: commands.Bot):
    bot.add_cog(Prefix(bot))
