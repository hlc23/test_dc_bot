import logging

import discord
from discord.ext import commands
import aiohttp
import dotenv
import os
import asyncio

dotenv.load_dotenv()

logger = logging.getLogger(__name__)


class LLMChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open("./data/prompt.txt", "r", encoding="utf-8") as f:
                self.PROMPT_TEMPLATE = f.read()
        except FileNotFoundError:
            logger.warning("./data/prompt.txt not found, using empty template")
            self.PROMPT_TEMPLATE = ""

        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")
        self.request_timeout = int(os.getenv("OPENROUTER_TIMEOUT", "180"))
        self.thinking_emoji = "🤔"
        self.timeout_emoji = ":x:"

        logger.info(f"LLMChat initialized - OpenRouter Model: {self.model}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.guild is None:  # Ignore DMs
            return
        if message.author.bot:  # Ignore messages from other bots
            return

        if self.bot.user.mentioned_in(message):
            thinking_reaction_added = False
            logger.info("Received message from %s: %s", message.author, message.content)
            try:
                await message.add_reaction(self.thinking_emoji)
                thinking_reaction_added = True
            except discord.HTTPException:
                pass

            async with message.channel.typing():
                try:
                    response = await self.generate_response(message)
                    # cut at last space or newline before 2000 chars to avoid breaking formatting
                    
                    if len(response) > 2000:
                        for cut_point in (response.rfind("\n", 0, 2000), response.rfind(" ", 0, 2000)):
                            if cut_point != -1:
                                await message.reply(response[:cut_point])
                                response = response[cut_point:].lstrip()
                                break
                    else:
                        await message.reply(response)
                    
                    if thinking_reaction_added:
                        try:
                            await message.remove_reaction(self.thinking_emoji, self.bot.user)
                        except discord.HTTPException:
                            pass
                except Exception:
                    if thinking_reaction_added:
                        try:
                            await message.remove_reaction(self.thinking_emoji, self.bot.user)
                            await message.add_reaction(self.timeout_emoji)
                        except discord.HTTPException:
                            pass
                    await message.reply(f"-# {self.bot.user.mention} 好像睡著了...沒有任何回應...")

    async def generate_response(self, message: discord.Message) -> str:
        prompt = message.content

        if message.mentions:  # replace mentions with usernames for better context
            for user in message.mentions:
                prompt = prompt.replace(f"<@{user.id}>", f"@{user.name}")
                prompt = prompt.replace(f"<@!{user.id}>", f"@{user.name}")

        if not prompt.strip():
            prompt = "Hi, how are you?"

        reply = ""
        if message.reference:
            try:
                ref_message = await message.channel.fetch_message(message.reference.message_id)
                reply = f"Previous message:\n{ref_message.author.mention}: {ref_message.content}\n\n"
            except discord.NotFound:
                pass

        messages = [
            {
                "role": "system",
                "content": self.PROMPT_TEMPLATE,
            },
            {
                "role": "user",
                "content": f"{reply}Response for {message.author.mention}:\n```{prompt}```",
            },
        ]

        payload = {
            "model": self.model,
            "messages": messages,
        }

        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            timeout = aiohttp.ClientTimeout(total=self.request_timeout)
            try:
                async with session.post(
                    self.openrouter_url, json=payload, timeout=timeout, headers=headers
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        choice = data["choices"][0]["message"]
                        content = choice.get("content", "")
                        if not content:
                            return "No response generated"
                        return "".join(content) if isinstance(content, list) else content
                    else:
                        error_text = (await resp.text())[:300]
                        raise Exception(
                            f"OpenRouter API error: {resp.status} | {error_text}"
                        )
            except asyncio.TimeoutError:
                logger.error("Timeout connecting to OpenRouter")
                raise
            except OSError as e:
                logger.error(f"Network error connecting to OpenRouter: {e}")
                raise Exception(f"Cannot connect to OpenRouter: {e}")
            except Exception as e:
                logger.error(f"Error in generate_response: {type(e).__name__}: {e}")
                raise


def setup(bot: discord.Bot):
    if os.getenv("OPENROUTER_API_KEY") is None:
        logger.info("OPENROUTER_API_KEY environment variable must be set for LLMChat cog.")
        return
    bot.add_cog(LLMChat(bot))
