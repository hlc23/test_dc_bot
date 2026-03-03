import discord
from discord.ext import commands
import aiohttp
import dotenv
import os
import asyncio

dotenv.load_dotenv()

with open("./data/prompt.txt", "r", encoding="utf-8") as f:
    PROMPT_TEMPLATE = f.read()

class LLMChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.model = os.getenv("OLLAMA_MODEL", "llama2")
        self.ollama_username = os.getenv("OLLAMA_USERNAME")
        self.ollama_password = os.getenv("OLLAMA_PASSWORD")
        self.request_timeout = int(os.getenv("OLLAMA_TIMEOUT", "30"))
        self.thinking_emoji = "🤔"
        self.timeout_emoji = ":x:"
    
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

            try:
                await message.add_reaction(self.thinking_emoji)
                thinking_reaction_added = True
            except discord.HTTPException:
                pass

            async with message.channel.typing():
                try:
                    response = await self.generate_response(message.content)
                    
                    if len(response) > 2000:
                        response = response[:1997] + "..."
                    
                    await message.reply(response)
                    if thinking_reaction_added:
                        try:
                            await message.remove_reaction(self.thinking_emoji, self.bot.user)
                        except discord.HTTPException:
                            pass
                except asyncio.TimeoutError:
                    if thinking_reaction_added:
                        try:
                            await message.remove_reaction(self.thinking_emoji, self.bot.user)
                        except discord.HTTPException:
                            pass
                    try:
                        await message.add_reaction(self.timeout_emoji)
                    except discord.HTTPException:
                        pass
                    await message.reply("Request timed out, please try again.")
                except Exception as e:
                    if thinking_reaction_added:
                        try:
                            await message.remove_reaction(self.thinking_emoji, self.bot.user)
                        except discord.HTTPException:
                            pass
                    await message.reply(f"Error: {str(e)}")
    
    async def generate_response(self, prompt: str) -> str:
        if not prompt.strip():
            prompt = "Hi, how are you?"
            
        payload = {
            "model": self.model,
            "prompt": f"{PROMPT_TEMPLATE}\n\n```{prompt}```",
            "stream": False
        }
        auth = None
        if self.ollama_username is not None and self.ollama_password is not None:
            auth = aiohttp.BasicAuth(login=self.ollama_username, password=self.ollama_password)
        
        async with aiohttp.ClientSession() as session:
            timeout = aiohttp.ClientTimeout(total=self.request_timeout)
            async with session.post(self.ollama_url, json=payload, timeout=timeout, auth=auth) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("response", "No response generated")
                else:
                    raise Exception(f"Ollama API error: {resp.status}")

async def setup(bot):
    if (
        os.getenv("OLLAMA_URL") is None or
        os.getenv("OLLAMA_MODEL") is None
    ):
        print("OLLAMA_URL and OLLAMA_MODEL environment variables must be set for LLMChat cog.")
        return
    await bot.add_cog(LLMChat(bot))
