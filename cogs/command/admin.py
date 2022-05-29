import discord
from core.cog_class import Cog_basic
from discord.ext import commands
from core.check import is_admin

class Admin(Cog_basic):

    @commands.Command
    @commands.check(is_admin)
    async def say(self, ctx:commands.Context, channel:discord.TextChannel, msg):
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
        await self.delete_message(ctx, reason=None)
        await member.add_roles(normal_role)

def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
