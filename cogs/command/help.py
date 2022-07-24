import discord
from core.cog_class import Cog_basic
from discord import OptionChoice

class Help(Cog_basic):

    @discord.slash_command(name="help", description="show help information")
    async def help(
        self, 
        ctx: discord.ApplicationContext,
        cmd: discord.Option(choices=["help", "ping", "me", "show", "pixiv" ,"translator"], required=False)
        ):
        """
        Shows help information for a specific command.

        Parameters
        ----------
        ctx : discord.ApplicationContext
            The application context.
        cmd : str
            The name of the command.
        """
        if cmd is None:
            self.guild = self.bot.get_guild(self.config["HLCT_guild"])
            await ctx.respond(f"Hi! {self.guild.get_member(970189566487171122).mention} is a bot for programming exercise.\n Try `/help [cmd]` to get commands information")
            return

        if cmd == "help":
            embed = discord.Embed(
                title="help",
                colour=discord.Colour.green(),
                description="顯示特定指令說明\n\n`/help [cmd]`\n\ncmd:欲查詢的指令")
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            await ctx.respond(embed=embed)
            return
        elif cmd == "ping":
            embed = discord.Embed(
                title="ping",
                colour=discord.Colour.green(),
                description="顯示機器人延遲\n\n`/ping`")
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            await ctx.respond(embed=embed)
            return
        elif cmd == 'me':
            embed = discord.Embed(
                title="me",
                colour=discord.Colour.green(),
                description="顯示使用者的資訊(僅自己可見)\n\n`/me`")
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            await ctx.respond(embed=embed)
        elif cmd == "show":
            embed = discord.Embed(
                title="show",
                colour=discord.Colour.green(),
                description="顯示特定成員資訊\n\n`/show [member]`\n\ncmd:欲查詢的對象")
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            await ctx.respond(embed=embed)
        elif cmd == "pixiv":
            embed = discord.Embed(
                title="pixiv",
                colour=discord.Colour.green(),
                description=f"請求pixiv的推薦內容\n\n`/pixiv`\n\n僅在{self.guild.get_channel(974633423178190909).mention}可用")
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            await ctx.respond(embed=embed)
        elif cmd == "translator":
            embed = discord.Embed(
                title="translator",
                colour=discord.Colour.green(),
                description="使用Microsoft線上翻譯\n\n`/translator [text] [language]`\n\ntext:要翻譯的內容\nlanguage:目標語言")
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            await ctx.respond(embed=embed)


def setup(bot: discord.Bot):
    bot.add_cog(Help(bot))