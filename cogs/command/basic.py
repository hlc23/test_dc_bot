from core.cog_class import Cog_basic
from discord.utils import format_dt
import discord
import datetime

class Basic(Cog_basic):
    

    @discord.slash_command(name="ping", description="Ping the bot.")
    async def ping(self, ctx):
        await ctx.respond(f"延遲:{round(self.bot.latency*1000)} ms", ephemeral=True)

    @discord.slash_command(name="me", description="查看伺服器上的個人資料")
    async def me(self, ctx:discord.ApplicationContext):
        embed=discord.Embed(title=ctx.author.name, description=ctx.author.mention)
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
        self.member:discord.Member = member
        embed=discord.Embed(title=self.member.name, description=self.member.mention)
        joinDate = ctx.author.joined_at.date()
        joinTime = ctx.author.joined_at.time()

        jT = datetime.datetime(joinDate.year, joinDate.month, joinDate.day, joinTime.hour, joinTime.minute, joinTime.second)

        embed.add_field(name="加入時間", value=f"{format_dt(jT, 'f')}\n{format_dt(jT, 'R')}", inline=False)
        embed.add_field(name="狀態", value=self.member.activity, inline=False)
        embed.add_field(name="最高身分組", value=self.member.top_role, inline=False)
        embed.set_thumbnail(url=self.member.display_avatar.url)
        await ctx.respond(embed=embed)



def setup(bot: discord.Bot):
    bot.add_cog(Basic(bot))
