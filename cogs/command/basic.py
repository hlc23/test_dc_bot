from core.cog_class import Cog_basic
from discord.ext import commands
import discord

class Basic(Cog_basic):

    @commands.Command
    async def ping(self, ctx):
        await ctx.send(f"延遲:{round(self.bot.latency*1000)} ms")

    @commands.Command
    async def me(self, ctx:commands.Context):
        embed=discord.Embed(title=ctx.author.name, description=ctx.author.mention)
        embed.add_field(name="加入時間", value=ctx.author.joined_at, inline=False)
        embed.add_field(name="狀態", value=ctx.author.activity, inline=False)
        embed.add_field(name="最高身分組", value=ctx.author.top_role, inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.Command
    async def show(self, ctx:commands.Context, member:discord.Member):
        embed=discord.Embed(title=member.name, description=member.mention)
        embed.add_field(name="加入時間", value=member.joined_at, inline=False)
        embed.add_field(name="狀態", value=member.activity, inline=False)
        embed.add_field(name="最高身分組", value=member.top_role, inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Basic(bot))
