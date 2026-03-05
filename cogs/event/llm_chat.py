import logging

import discord
from discord.ext import commands
import aiohttp
import dotenv
import os
import asyncio
from urllib.parse import urlparse

dotenv.load_dotenv()

logger = logging.getLogger(__name__)


def normalize_ollama_url(raw_url: str) -> str:
    url = (raw_url or "").strip().strip('"').strip("'")
    if not url:
        return "http://localhost:11434/api/generate"
    parsed = urlparse(url)
    path = (parsed.path or "").rstrip("/")
    if path in ("", "/"):
        return url.rstrip("/") + "/api/generate"
    if path.endswith("/api/generate") or path.endswith("/api/chat"):
        return url
    return url

class LLMChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open("./data/prompt.txt", "r", encoding="utf-8") as f:
                self.PROMPT_TEMPLATE = f.read()
        except FileNotFoundError:
            logger.warning("./data/prompt.txt not found, using empty template")
            self.PROMPT_TEMPLATE = ""
        
        self.ollama_url = normalize_ollama_url(os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate"))
        self.model = os.getenv("OLLAMA_MODEL", "llama2")
        self.ollama_username = os.getenv("OLLAMA_USERNAME")
        self.ollama_password = os.getenv("OLLAMA_PASSWORD")
        self.request_timeout = int(os.getenv("OLLAMA_TIMEOUT", "180"))
        self.thinking_emoji = "🤔"
        self.timeout_emoji = ":x:"
        
        logger.info(f"LLMChat initialized - OLLAMA_URL: {self.ollama_url}, Model: {self.model}")
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.guild is None: # Ignore DMs
            return
        if message.author.bot: # Ignore messages from other bots
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
                    
                    if len(response) > 2000:
                        response = response[:1997] + "..."
                    
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
        
        if message.mentions: # replace mentions with usernames for better context
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
        
        payload = {
            "model": self.model,
            "prompt": f"{self.PROMPT_TEMPLATE}\n\n{reply}Response for {message.author.mention}:\n```{prompt}```",
            "stream": False
        }
        auth = None
        if self.ollama_username is not None and self.ollama_password is not None:
            auth = aiohttp.BasicAuth(login=self.ollama_username, password=self.ollama_password)
        
        async with aiohttp.ClientSession() as session:
            timeout = aiohttp.ClientTimeout(total=self.request_timeout)
            try:
                async with session.post(self.ollama_url, json=payload, timeout=timeout, auth=auth) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("response", "No response generated")
                    else:
                        error_text = (await resp.text())[:300]
                        raise Exception(f"Ollama API error: {resp.status} at {self.ollama_url} | {error_text}")
            except asyncio.TimeoutError:
                logger.error(f"Timeout connecting to Ollama at {self.ollama_url}")
                raise
            except OSError as e:
                logger.error(f"Network error connecting to Ollama at {self.ollama_url}: {e}")
                raise Exception(f"Cannot connect to Ollama: {e}")
            except Exception as e:
                logger.error(f"Error in generate_response: {type(e).__name__}: {e}")
                raise

def setup(bot: discord.Bot):
    if (
        os.getenv("OLLAMA_URL") is None or
        os.getenv("OLLAMA_MODEL") is None
    ):
        logger.info("OLLAMA_URL and OLLAMA_MODEL environment variables must be set for LLMChat cog.")
        return
    bot.add_cog(LLMChat(bot))
