from core.cog_class import Cog_basic
import discord
from util.translator import translations

class Translation(Cog_basic):

	@discord.slash_command(name="translator", description="translation text")
	async def translator(
		self, 
		ctx: discord.ApplicationContext,
		text: str,
		language: discord.Option(choices=[
			discord.OptionChoice(name="繁體中文", value="zh-Hant"),
			discord.OptionChoice(name="簡體中文", value="zh-Hans"),
			discord.OptionChoice(name="English", value="en"),
			discord.OptionChoice(name="Français", value="fr"),
			discord.OptionChoice(name="Italiano", value="it"),
			discord.OptionChoice(name="日本語", value="ja"),
			]) # type: ignore
		):
		data = translations(Lang=language, text=text)
		embed = discord.Embed(title="翻譯", colour=discord.Colour.green(), description=text)
		embed.set_footer(text="By Microsoft translator")
		embed.add_field(name="Result", value=data, inline=False)
		await ctx.respond(embed=embed)

def setup(bot: discord.Bot):
    bot.add_cog(Translation(bot))
