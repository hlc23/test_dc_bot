import json
from typing import List, Tuple
from discord.ext.commands import Bot
from discord import User
from utils.file import get_cogs, load_config

class Mybot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = load_config()
        self.AUTHOR_ID: int = self.config["author_id"]
        self.VERSION = self.config["version"]
        self.loaded_cogs = []
        self.load_cogs()
        
    def load_cogs(self) -> Tuple[List[str], List[str]]:
        '''
        Load cogs from cogs.json file
        
        Returns a tuple containing two lists:
        - The first list contains the names of the successfully loaded cogs.
        - The second list contains the names of the cogs that failed to load.
        '''
        cogs = get_cogs()
        error = []
        for cog in cogs:
            try:
                self.load_extension(f"cogs.{cog}")
                self.loaded_cogs.append(cog)
            except:
                error.append(cog)
        return (self.loaded_cogs, error)

    def reload_cogs(self) -> Tuple[List[str], List[str]]:
        '''
        Reloads all the loaded cogs in the bot.

        Returns:
        - success (List[str]): A list of cogs that were successfully reloaded.
        - error (List[str]): A list of cogs that encountered an error during reloading.
        '''
        success = []
        error = []
        for cog in self.loaded_cogs:
            try:
                self.reload_extension(f"cogs.{cog}")
                success.append(cog)
            except:
                error.append(cog)
        return success, error
    
    def unload_cog(self, cog: str):
        """
        Unloads a cog from the bot.

        Parameters:
        - cog (str): The name of the cog to unload.

        Returns:
        - bool: True if the cog was successfully unloaded, False otherwise.
        """
        try:
            self.unload_extension(f"cogs.{cog}")
            self.loaded_cogs.remove(cog)
        except:
            return False
        return True

    @property
    def owner(self) -> User:
        return self.get_user(self.AUTHOR_ID)
