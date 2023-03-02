import os
import discord
import dotenv
import time
from discord.ext import commands
from matty_db import Database
from colorama import Back, Fore, Style



class Client(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=intents) 
        self.coglist = ['cogs.faqs', 'cogs.events', 'cogs.eventinvite', 'cogs.exampleDB']

    async def setup_hook(self) -> None:
        for cog in self.coglist:
            await self.load_extension(cog)

    async def on_ready(self):
        prfx = (Style.BRIGHT + Back.BLACK + Fore.GREEN + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + Back.RESET + Fore.WHITE)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        synced = await self.tree.sync()
        print(prfx + " Number of cogs loaded: " + Fore.YELLOW + str(len(self.coglist)) )
        print(prfx + " Number of slash commands synced: " + Fore.YELLOW + str(len(synced)))
        


dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

db = Database()
db.startup()    

client = Client()
client.run(TOKEN)