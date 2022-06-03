import discord
from core.cog_class import Cog_basic
from discord.ext import commands
from core.check import is_admin

class Admin(Cog_basic):

    @commands.Command
    @commands.check(is_admin)
    async def say(self, ctx:commands.Context, channel:discord.TextChannel, *, msg):
        await self.delete_message(ctx, reason=None)
        await channel.send(msg)
    
    @commands.Command
    @commands.check(is_admin)
    async def role(self, ctx:commands.Context, member:discord.Member, role:discord.Role):
        await self.delete_message(ctx, reason=None)
        await member.add_roles(role)

    @commands.Command
    @commands.check(is_admin)
    async def join(self, ctx:commands.Context, member:discord.Member):
        normal_role = self.guild.get_role(969962597061373994)
        border_channel = self.bot.get_channel(self.config["border_channel"])
        await self.delete_message(ctx, reason=None)
        await member.add_roles(normal_role)
        embed=discord.Embed(title="成員加入", description=member.mention)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=member.name)
        await border_channel.send(embed=embed)

    @commands.Command
    @commands.check(is_admin)
    async def poll(self, ctx:commands.Context, question:str, *, option:str):
        embed = discord.Embed(title=question)
        text = ""
        alphabet = "🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹"
        options = option.split(" ")
        for i in range(len(options)):
            text += f"{alphabet[i]}{options[i]}\n"
        embed.description = text
        await ctx.message.delete()
        msg = await ctx.send(content=f"投票發起人:{ctx.author.mention}",embed=embed)
        for t in range(len(options)):
            await msg.add_reaction(alphabet[t])


def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
