import discord
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print('')
    print(f"{client.user} has online.")
    print("="*15)

@client.event
async def on_message(message):
    # 當訊息
    if message.author == client.user:
        return

    if message.content.startswith(f'!Hello'):
        print(f'{message.author} called "!Hello"')
        await message.channel.send('Hello')

client.run(input('enter your bot token\n'))
