import discord
import datetime
from core.bot import Mybot
from core.cog_class import Cog_basic
from discord.utils import format_dt
from discord import Embed

class Basic(Cog_basic):

    @discord.slash_command(name="ping", description="Ping the bot.")
    async def ping(self, ctx):
        await ctx.respond(f"延遲:{round(self.bot.latency*1000)} ms", ephemeral=True)

    @discord.slash_command(name="me", description="查看伺服器上的個人資料")
    async def me(self, ctx:discord.ApplicationContext):
        embed=Embed(title=ctx.author.name, description=ctx.author.mention)
        joinDate = ctx.author.joined_at.date()
        joinTime = ctx.author.joined_at.time()

        jT = datetime.datetime(joinDate.year, joinDate.month, joinDate.day, joinTime.hour, joinTime.minute, joinTime.second)

        embed.add_field(name="加入時間", value=f"{format_dt(jT, 'f')}\n{format_dt(jT, 'R')}", inline=False)
        embed.add_field(name="狀態", value=ctx.author.activity, inline=False)
        embed.add_field(name="最高身分組", value=ctx.author.top_role, inline=False)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        await ctx.respond(embed=embed, ephemeral=True)

    @discord.slash_command(name="show", description="查看他人在伺服器上的個人資料")
    async def show(
        self, 
        ctx:discord.ApplicationContext,
        member:discord.Option(discord.Member, "查看的對象") # type: ignore
        ):
        member:discord.Member = member
        embed=Embed(title=member.name, description=member.mention)
        joinDate = member.joined_at.date()
        joinTime = member.joined_at.time()

        jT = datetime.datetime(joinDate.year, joinDate.month, joinDate.day, joinTime.hour, joinTime.minute, joinTime.second)

        embed.add_field(name="加入時間", value=f"{format_dt(jT, 'f')}\n{format_dt(jT, 'R')}", inline=False)
        embed.add_field(name="狀態", value=member.activity, inline=False)
        embed.add_field(name="最高身分組", value=member.top_role, inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="about", description="關於機器人")
    async def about(self, ctx:discord.ApplicationContext):
        embed = Embed(title="About", description=f"A simple discord bot developed by {self.bot.owner.mention}")
        embed.add_field(name="Version", value=self.bot.VERSION)
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot: Mybot):
    bot.add_cog(Basic(bot))
