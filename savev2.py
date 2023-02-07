import os
import discord
import dotenv
import tool
import resp
import sqlite3
from discord.ext import commands
from discord import ui


dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=discord.Intents().all())


@client.event
async def on_ready():
  # Print message in consol if online
  print(f'Successfully logged in as {client.user}')
  
  # Enable slash commands
  await client.tree.sync()
  print(f'Successfully synced slash commands')

  # Establish database connection
  db = sqlite3.connect('faq_db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS faq_db(
      id integer PRIMARY KEY AUTOINCREMENT,
      question TEXT,
      answer TEXT
      )
      ''')
  db.commit()
  db.close()


class Questionnaire(ui.Modal, title='Questionnaire Response'):
  name = ui.TextInput(label='Name')
  answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

  async def on_submit(self, interaction: discord.Interaction):
    await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)


#class AddFaqModal(ui.Modal, title ="Add FAQ"):
#  question = ui.TextInput(label="Question:", style=discord.TextStyle.short, required=True)
#  answer = ui.TextInput(label="Answer:", style=discord.TextStyle.long, required=True)


@client.tree.command(name="ping", description ="Sends pong")
async def ping(interaction: discord.Interaction):
  await interaction.response.send_message(content="pong")

@client.tree.command(name="modal", description ="Add a FAQ")
async def modal(interaction: discord.Interaction):
  await interaction.response.send_modal(Questionnaire())













client.run(TOKEN)
