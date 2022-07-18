import discord
from core.cog_class import Cog_basic

class Dvc(Cog_basic):

    @discord.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        
        if after.channel is not None:
            if after.channel.id == self.config["dvc"]:
                guild = self.bot.get_guild(self.config["HLCT_guild"])
                new_channel = await guild.create_voice_channel(name=f"{member.display_name}的語音頻道",category=after.channel.category)
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
        if before.channel is None:
            return
        if (len(before.channel.members) == 0) and (before.channel.id != self.config["dvc"]):
            await before.channel.delete()
            return


def setup(bot: discord.Bot):
    bot.add_cog(Dvc(bot))
