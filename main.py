import os
import discord
import dotenv
import sqlite3
from discord.ext import commands #maybe remove?
from discord import ui, app_commands


dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')




class Client(discord.Client):
  def __init__(self) -> None:
      intents = discord.Intents.default()
      intents.message_content = True
      super().__init__(command_prefix='!', intents=intents) 
      self.tree = app_commands.CommandTree(self) # Enables slash commands

  async def setup_hook(self) -> None:
      await self.tree.sync() # Syncs the application command with Discord
      print(f'Successfully synced slash commands')

  async def on_ready(self):     
    print(f'Successfully logged in as {client.user}') # Prints message in console if online
    db = sqlite3.connect('db.sqlite') # Establish database connection
    cursor = db.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS faq_db(
        id integer PRIMARY KEY AUTOINCREMENT,
        questions TEXT,
        answers TEXT
        )
        ''')
    db.commit()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS events_db(
        id integer PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        time TEXT,
        location TEXT,
        description TEXT
        )
        ''')
    db.commit()
    db.close()

class AddFaqModal(discord.ui.Modal, title='Add to FAQ'):
    question = discord.ui.TextInput(label='Question', style=discord.TextStyle.short, required=True)
    answer = discord.ui.TextInput(label="Answer:", style=discord.TextStyle.long, required=True)

    async def on_submit(self, interaction: discord.Interaction):
      db = sqlite3.connect('db.sqlite')
      cursor = db.cursor()
      sql = "INSERT INTO faq_db(questions, answers) VALUES (?, ?)"
      val = (f'{self.question}', f'{self.answer}')
      cursor.execute(sql, val)
      db.commit()
      db.close()
      await interaction.response.send_message(f'Success! A new FAQ has been added!\n\nQuestion: **{self.question}**\nAnswer: **{self.answer}**', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
      await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)


class AddEventModal(discord.ui.Modal, title='Add an Event'):
    name = discord.ui.TextInput(label='Name of event:', style=discord.TextStyle.short, required=True)
    date = discord.ui.TextInput(label="Start date:", style=discord.TextStyle.short, required=True)
    time = discord.ui.TextInput(label="Start time:", style=discord.TextStyle.short, required=True)
    location = discord.ui.TextInput(label="Location:", style=discord.TextStyle.short, required=True)
    description = discord.ui.TextInput(label="Description:", style=discord.TextStyle.long, required=True)

    async def on_submit(self, interaction: discord.Interaction):
      db = sqlite3.connect('db.sqlite')
      cursor = db.cursor()
      sql = "INSERT INTO events_db(name, date, time, location, description) VALUES (?, ?, ?, ?, ?)"
      val = (f'{self.name}', f'{self.date}', f'{self.time}', f'{self.location}',f'{self.description}')
      cursor.execute(sql, val)
      db.commit()
   
      embed = discord.Embed(title="Success! A new event has been added.", description="Here are the details:", color = discord.Color.green())
      embed.add_field(name="Name of Event", value=f'{self.name}', inline=False)
      embed.add_field(name="Start date", value=f'{self.date}', inline=True)
      embed.add_field(name="Start time", value=f'{self.time}', inline=True)
      embed.add_field(name="Location", value=f'{self.location}', inline=False)
      embed.add_field(name="Description", value=f'{self.description}', inline=False)
      
      await interaction.response.send_message(embed=embed, ephemeral=True)
      db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
      await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)


client = Client()


@client.tree.command(name="addfaq", description="Add a question & answer to FAQ")
async def addfaq(interaction: discord.Interaction):
    await interaction.response.send_modal(AddFaqModal())

@client.tree.command(name="listfaq", description="View a list of all FAQ")
async def listfaq(interaction:discord.Interaction):
  db = sqlite3.connect('db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    SELECT questions FROM faq_db
      ''')
  embed = discord.Embed(title="List of all FAQ", description="To ask a question, -- **directions to do something** --", color = discord.Color.blue())
  rows = cursor.fetchall()
  count = 1
  for row in rows:
    question = row[0]
    embed.add_field(name=f'{count}- {question}', value='\n', inline= False)
    count += 1
  
  await interaction.response.send_message(embed=embed, ephemeral=True)
  db.commit()
  db.close()


@client.tree.command(name="addevent", description="Add an event")
async def addevent(interaction: discord.Interaction):
    await interaction.response.send_modal(AddEventModal())


@client.tree.command(name="listevents", description="View a list of all Events")
async def listevents(interaction:discord.Interaction):
  db = sqlite3.connect('db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    SELECT name, date, time FROM events_db
      ''')
  embed = discord.Embed(title="List of all events", description="For more information about an event, -- **directions to do something** --", color = discord.Color.blue())
  rows = cursor.fetchall()
  count = 1
  for row in rows:
    name = row[0]
    date = row[1]
    time = row[2]
    embed.add_field(name=f'{count}- {name}', value=f'{date} at {time}', inline= False)
    count += 1
  
  await interaction.response.send_message(embed=embed, ephemeral=True)
  db.commit()
  db.close()




@client.tree.command(name="listanswers", description="View a list of all answers from FAQ")
async def listanswers(interaction:discord.Interaction):
  db = sqlite3.connect('db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    SELECT answers FROM faq_db
      ''')
  embed = discord.Embed(title="List of all answers", description="Answers to the FAQ", color = discord.Color.blue())
  rows = cursor.fetchall()
  count = 1
  for row in rows:
    answer = row[0]
    embed.add_field(name=f'{count}- {answer}', value='\n', inline= False)
    count += 1

  await interaction.response.send_message(embed=embed, ephemeral=True)
  db.commit()
  db.close()


@client.tree.command(name="deleteallfaq", description="Delete all FAQ from the database")
async def deleteallfaq(interaction: discord.Interaction):
  db = sqlite3.connect('db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    DELETE FROM faq_db
      ''')
  await interaction.response.send_message("Done! All FAQ have been cleared from the database")
  db.commit()
  db.close()


@client.tree.command(name="deleteallevents", description="Delete all events from the database")
async def deleteallevents(interaction: discord.Interaction):
  db = sqlite3.connect('db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    DELETE FROM events_db
      ''')  
  await interaction.response.send_message("Done! All events have been cleared from the database")
  db.commit()
  db.close()


@client.tree.command(name="deletefaq", description = "Delete a FAQ from the database")
async def deletefaq(interaction: discord.Interaction):
  db = sqlite3.connect('db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    SELECT questions FROM faq_db
      ''')
  embed = discord.Embed(title="Delete a FAQ", description="Enter the number of the FAQ to delete", color = discord.Color.blue())
  rows = cursor.fetchall()
  count = 1
  for row in rows:
    question = row[0]
    embed.add_field(name=f'{count}- {question}', value='\n', inline= False)
    count += 1
  await interaction.response.send_message(embed=embed)

  def check(m):
      return m.author == interaction.user and m.channel == interaction.channel

  selection = await client.wait_for('message', check=check)
  selected_index = int(selection.content) - 1
  selected_row = rows[selected_index]
  cursor.execute('''DELETE FROM faq_db WHERE questions=?''', (selected_row[0],))
  
  await interaction.channel.send(f"Done! You deleted FAQ #{int(selection.content)}.")
  db.commit()
  db.close()
  



  





    




client.run(TOKEN)



