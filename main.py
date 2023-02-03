import os
import discord
import dotenv
import tool
import resp
import sqlite3
from discord.ext import commands
from discord import ui, app_commands


dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')


class Client(discord.Client):
  def __init__(self) -> None:
      intents = discord.Intents.default()
      super().__init__(command_prefix='!', intents=intents) 
      self.tree = app_commands.CommandTree(self) # Enables slash commands

  async def setup_hook(self) -> None:
      await self.tree.sync() # Syncs the application command with Discord
      print(f'Successfully synced slash commands')

  async def on_ready(self):     
    print(f'Successfully logged in as {client.user}') # Prints message in console if online
    db = sqlite3.connect('faq_db.sqlite') # Establish database connection
    cursor = db.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS faq_db(
        id integer PRIMARY KEY AUTOINCREMENT,
        questions TEXT,
        answers TEXT
        )
        ''')
    db.commit()
    db.close()

class AddFaqModal(discord.ui.Modal, title='Add to FAQ'):
    question = discord.ui.TextInput(label='Question', style=discord.TextStyle.short, required=True)
    answer = discord.ui.TextInput(label="Answer:", style=discord.TextStyle.long, required=True)

    async def on_submit(self, interaction: discord.Interaction):
      db = sqlite3.connect('faq_db.sqlite')
      cursor = db.cursor()
      sql = "INSERT INTO faq_db(questions, answers) VALUES (?, ?)"
      val = (f'{self.question}', f'{self.answer}')
      cursor.execute(sql, val)
      db.commit()
      db.close()
      await interaction.response.send_message(f'New FAQ has been added!\n\nQuestion: **{self.question}**\nAnswer: **{self.answer}**', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
      await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)


client = Client()


@client.tree.command(name="addfaq", description="Add a question & answer to FAQ")
async def addfaq(interaction: discord.Interaction):
    await interaction.response.send_modal(AddFaqModal())


@client.tree.command(name="listfaq", description="View a list of all FAQ")
async def listfaq(interaction:discord.Interaction):
  db = sqlite3.connect('faq_db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    SELECT questions FROM faq_db
      ''')
  result = cursor.fetchall()
  await interaction.response.send_message(f'{result}', ephemeral=True)
  db.commit()
  db.close()



client.run(TOKEN)
