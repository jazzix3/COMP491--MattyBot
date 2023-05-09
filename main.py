import os, os.path
import discord
import dotenv
import time
from discord.ext import commands
from matty_db import Database
from colorama import Back, Fore, Style
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Client(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=intents) 
        self.coglist = ['cogs.archivecommands', 'cogs.eventcommands', 'cogs.exampleDB', 'cogs.faqscommands', 'cogs.pollscommands']

    async def setup_hook(self) -> None:
        for cog in self.coglist:
            await self.load_extension(cog)

    async def on_ready(self):
        prfx = (Fore.WHITE + Style.DIM + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + Back.RESET )
        print(prfx + Style.NORMAL +" Logged in as "  + Fore.YELLOW + self.user.name)
        print(prfx + Style.NORMAL + " Bot ID "  + Fore.YELLOW + str(self.user.id))
        #synced = await self.tree.sync()
        print(prfx + Style.NORMAL + " Number of cogs loaded: "  + Fore.YELLOW + str(len(self.coglist)) + Fore.RESET)
        #print(prfx + " Number of slash commands synced: " + Fore.YELLOW + str(len(synced)))
        CalendarSetup()
        print(prfx + Style.NORMAL + " Logged into Google Calendar id: "  + Fore.YELLOW + "***(will add id later)***")
            





def CalendarSetup():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())



dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

db = Database()
db.startup()    

client = Client()
client.run(TOKEN)