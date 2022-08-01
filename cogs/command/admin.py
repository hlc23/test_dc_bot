import datetime
import time
import discord
from core.cog_class import Cog_basic

class Admin(Cog_basic):

    adminCmdGroup = discord.SlashCommandGroup(name="admin", description="Admin commands")

    @adminCmdGroup.command(name="join", description="ONLY ADMIN:Let someone in.")
    async def join(self, ctx:discord.ApplicationContext, member:discord.Member):
        if ctx.author.guild_permissions.administrator is False:
            embed = discord.Embed(title="您無使用此指令的權限", colour=discord.Colour.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        self.guild = self.bot.get_guild(self.config["HLCT_guild"])
        normal_role = self.guild.get_role(969962597061373994)
        border_channel = self.bot.get_channel(self.config["border_channel"])
        await member.add_roles(normal_role)
        embed=discord.Embed(title="成員加入", description=member.mention)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=member.name)
        await border_channel.send(embed=embed)
        await ctx.respond(f"{member.mention} 已成功加入", ephemeral=True)

    @adminCmdGroup.command(name="status", description="ONLY ADMIN:bot status.")
    async def status(
        self,
        ctx:discord.ApplicationContext,
        status:discord.Option(description="bot status", choices=["online", "offline", "idle", "dnd", "invisible"])
        ):
        if ctx.author.guild_permissions.administrator is False:
            embed = discord.Embed(title="您無使用此指令的權限", colour=discord.Colour.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        if status == "online":
            await self.bot.change_presence(status=discord.Status.online)
            await ctx.respond("Change success", ephemeral=True)
            return
        elif status == "offline":
            await self.bot.change_presence(status=discord.Status.offline)
            await ctx.respond("Change success", ephemeral=True)
            return
        elif status == "idle":
            await self.bot.change_presence(status=discord.Status.idle)
            await ctx.respond("Change success", ephemeral=True)
            return
        elif status == "dnd":
            await self.bot.change_presence(status=discord.Status.dnd)
            await ctx.respond("Change success", ephemeral=True)
            return
        elif status == "invisible":
            await self.bot.change_presence(status=discord.Status.invisible)
            await ctx.respond("Change success", ephemeral=True)
            return

    @adminCmdGroup.command(name="mute", description="Mute member")
    async def mute(
        self, 
        ctx:discord.ApplicationContext, 
        member:discord.Member,
        reason: str,
        seconds:discord.Option(int, min_value=1, max_value=59, required=False),
        minutes: discord.Option(int, min_value=1, max_value=59, required=False),
        hours: discord.Option(int, min_value=1, max_value=23, required=False),
        days: discord.Option(int, min_value=1, max_value=30, required=False)
        ):
        if (member.guild_permissions.administrator):
            await ctx.respond("無法禁言管理員||我看你是想太多||", ephemeral=True)
            await ctx.author.timeout_for(datetime.timedelta(minutes=2), reason="嘗試禁言管理員")
            embed = discord.Embed(title="禁言", description=f"{ctx.author.mention}已被禁言", colour=discord.Colour.brand_red())
            embed.add_field(name="開始時間", value=f"<t:{int(time.mktime(datetime.datetime.now().timetuple()))}:f> <t:{int(time.mktime(datetime.datetime.now().timetuple()))}:R>")
            embed.add_field(name="結束時間", value=f"<t:{int(time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=2)).timetuple()))}:f> <t:{int(time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=2)).timetuple()))}:R>")
            embed.add_field(name="原因", value="嘗試禁言管理員")
            await ctx.channel.send(embed=embed)
            return
        if ctx.author.guild_permissions.administrator is False:
            embed = discord.Embed(title="您無使用此指令的權限", colour=discord.Colour.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        if (seconds is None) and (minutes is None) and (hours is None) and (days is None):
            await ctx.respond("時間不得為0", ephemeral=True)
            return
        muteTime = datetime.timedelta(seconds=seconds or 0, minutes=minutes or 0, hours=hours or 0, days=days or 0)
        await member.timeout_for(muteTime, reason=reason)
        await ctx.respond(f"禁言成功", ephemeral=True)
        embed = discord.Embed(title="禁言", description=f"{member.mention}已被禁言", colour=discord.Colour.brand_red())
        embed.add_field(name="開始時間", value=f"<t:{int(time.mktime(datetime.datetime.now().timetuple()))}:f> <t:{int(time.mktime(datetime.datetime.now().timetuple()))}:R>")
        embed.add_field(name="結束時間", value=f"<t:{int(time.mktime((datetime.datetime.now() + muteTime).timetuple()))}:f> <t:{int(time.mktime((datetime.datetime.now() + muteTime).timetuple()))}:R>")
        embed.add_field(name="原因", value=reason)
        await ctx.channel.send(embed=embed)
        return


def setup(bot: discord.Bot):
    bot.add_cog(Admin(bot))
