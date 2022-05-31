from core.cog_class import Cog_basic
from discord.ext import commands
import discord

class Dynamic(Cog_basic):
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel == self.bot.get_channel(self.config["dynamic_door"]):
            self.guild = self.guild
            new_channel = await self.guild.create_voice_channel(name=f"{member.display_name}的語音頻道",category=after.channel.category)
            new_channel:discord.VoiceChannel
            await member.move_to(new_channel)
            permission = discord.PermissionOverwrite()
            permission.manage_channels = True
            permission.priority_speaker = True
            permission.stream = True
            permission.view_channel = True
            permission.connect = True
            permission.speak = True
            permission.mute_members = True
            permission.deafen_members = True
            permission.move_members = True
            await new_channel.set_permissions(member, overwrite=permission)
            return
        if before == None:
            return
        if (len(before.channel.members) == 0) and (before.channel != self.bot.get_channel(self.config["dynamic_door"])):
            await before.channel.delete()
            return


def setup(bot: commands.Bot):
    bot.add_cog(Dynamic(bot))
