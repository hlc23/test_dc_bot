from core.cog_class import Cog_basic
import discord

class Basic(Cog_basic):
    

    @discord.slash_command(name="ping", description="Ping the bot.")
    async def ping(self, ctx):
        await ctx.send(f"延遲:{round(self.bot.latency*1000)} ms")

    @discord.slash_command(name="me", description="查看伺服器上的個人資料")
    async def me(self, ctx:discord.ApplicationContext):
        embed=discord.Embed(title=ctx.author.name, description=ctx.author.mention)
        joinTime = f"{ctx.author.joined_at.date()} {ctx.author.joined_at.time().hour:0>2}:{ctx.author.joined_at.time().minute:0>2}:{ctx.author.joined_at.time().second:0>2}"
        embed.add_field(name="加入時間", value=joinTime, inline=False)
        embed.add_field(name="狀態", value=ctx.author.activity, inline=False)
        embed.add_field(name="最高身分組", value=ctx.author.top_role, inline=False)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="show", description="查看他人在伺服器上的個人資料")
    async def show(
        self, 
        ctx:discord.ApplicationContext,
        member:discord.Option(discord.Member, "查看的對象")
        ):
        self.member:discord.Member = member
        embed=discord.Embed(title=self.member.name, description=self.member.mention)
        joinTime = f"{self.member.joined_at.date()} {self.member.joined_at.time().hour:0>2}:{self.member.joined_at.time().minute:0>2}:{self.member.joined_at.time().second:0>2}"
        embed.add_field(name="加入時間", value=joinTime, inline=False)
        embed.add_field(name="狀態", value=self.member.activity, inline=False)
        embed.add_field(name="最高身分組", value=self.member.top_role, inline=False)
        embed.set_thumbnail(url=self.member.avatar.url)
        await ctx.respond(embed=embed)


def setup(bot: discord.Bot):
    bot.add_cog(Basic(bot))
