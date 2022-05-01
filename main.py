import discord
import logging

# 設定日誌
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self.prefix = "!"

    # 登入bot提示訊息
    async def on_ready(self):
        print('')
        print(f"{bot.user} has online.")
        print("="*15)

    # 訊息判斷
    async def on_message(self,message):
        # 避免被自己的訊息觸發
        if message.author == self.user:
            return
        
        # 回覆 Hello
        if message.content.startswith(f"{self.prefix}Hello"):
            print(f"{message.author} called 'Hello'")
            await message.reply("Hello")

        # 更改前綴
        if message.content.startswith(f"{self.prefix}set_prefix"):
            new_prefix = message.content.replace(f"{self.prefix}set_prefix ","")
            await message.reply(f"change prefix from {self.prefix} to {new_prefix}")
            self.prefix = new_prefix
            print(f"{message.author} change prefix to '{self.prefix}'")

bot = Bot()
bot.run(input('enter your bot token\n'))
