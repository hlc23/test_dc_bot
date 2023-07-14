from core.cog_class import Cog_basic
import discord

class Rich(Cog_basic):
    
    @discord.slash_command(name="rich", description="If you consider some msg is rich, then just use this command.")
    async def rich(self,
             ctx: discord.ApplicationContext,
             msg_id: discord.Option(description="The message id you want to consider as rich", type=str, required=True)
             ):
        try:
            msg = await ctx.channel.fetch_message(msg_id)
        except discord.NotFound:
            ctx.respond("The message you want to consider as rich is not found.", ephemeral=True)
            return
        if msg.author == ctx.author:
            ctx.respond("You can't consider your own message as rich.", ephemeral=True)
            return
        for c in ["🇷", "🇮", "🇨", "🇭"]:
            # f":regional_indicator_{c}:"
            await msg.add_reaction(c)
        await ctx.respond("Done.", ephemeral=True)
        return

def setup(bot):
    bot.add_cog(Rich(bot))