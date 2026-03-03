import discord
import os
import dotenv
import logging

from core.bot import Mybot
from discord.ext import commands
from discord import Embed

dotenv.load_dotenv()


def setup_logging():
    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )


logger = logging.getLogger(__name__)

def main():
    setup_logging()
    bot = Mybot(debug_guilds=[967615452341739621], intents=discord.Intents.all(), command_prefix="!")

    @bot.event
    async def on_ready():
        logger.info("===============")
        logger.info("%s v%s is ready and online!", bot.user, bot.VERSION)
        logger.info("===============")
        embed = Embed(title="Bot is ready!", description=f"{bot.user} v{bot.VERSION} is ready and online!")
        # await bot.owner.send(embed=embed)
        return

    @bot.slash_command(name = "reload", description = "Reload bot")
    @commands.has_permissions(administrator=True)
    async def reload(ctx:discord.ApplicationContext):
        # reload env variables
        dotenv.load_dotenv()
        success, error = bot.reload_cogs()
        await ctx.send(f"Successfully reloaded {len(success)} cogs.")
        return

    @bot.event
    async def on_error(ctx, error):
        await bot.owner.send(f"Error: {error}")
        
    @bot.slash_command(name="cogs", description="List loaded cogs")
    async def cogs(ctx: discord.ApplicationContext):
        loaded_cogs = bot.list_cogs()
        if not loaded_cogs:
            await ctx.send("No cogs are currently loaded.")
            return
        
        embed = Embed(title="Loaded Cogs", description="\n".join(loaded_cogs))
        await ctx.send_response(embed=embed)

    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
