import discord
import os

from core.bot import Mybot
from discord.ext import commands
from discord import Embed

def main():
    bot = Mybot(debug_guilds=[967615452341739621], intents=discord.Intents.all(), command_prefix="!")

    @bot.event
    async def on_ready():
        print("="*15)
        print(f"{bot.user} v{bot.VERSION} is ready and online!")
        print("="*15)
        embed = Embed(title="Bot is ready!", description=f"{bot.user} v{bot.VERSION} is ready and online!")
        await bot.owner.send(embed=embed)
        return

    @bot.slash_command(name = "reload", description = "Reload cog")
    @commands.has_permissions(administrator=True)
    async def reload(ctx:discord.ApplicationContext):
        success, error = bot.reload_cogs()
        await ctx.send(f"Successfully reloaded {len(success)} cogs.")
        return

    @bot.listen()
    async def on_slash_command_error(ctx, error):
        await bot.owner.send(f"Error: {error}")

    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
