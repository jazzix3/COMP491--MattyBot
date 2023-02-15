import os
import discord
import dotenv
import sqlite3
from datetime import datetime
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
    db = sqlite3.connect('db.sqlite') # Establish database connection and creates tables
    cursor = db.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS faq_db(
        id integer PRIMARY KEY AUTOINCREMENT,
        questions TEXT,
        answers TEXT,
        creator TEXT,
        datecreated TEXT
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
        description TEXT,
        creator TEXT,
        datecreated TEXT,
        accepted_users TEXT,
        declined_users TEXT,
        tentative_users TEXT
        )
        ''')
    db.commit()
    db.close()

class AddFaqModal(discord.ui.Modal, title='Add to FAQ'):
    question = discord.ui.TextInput(label='Question', style=discord.TextStyle.short, required=True)
    answer = discord.ui.TextInput(label="Answer:", style=discord.TextStyle.long, required=True)

    async def on_submit(self, interaction: discord.Interaction):
      creator = interaction.user
      timestamp = datetime.now()
      datecreated = timestamp.strftime(f"%m/%d/%Y")
      
      db = sqlite3.connect('db.sqlite')
      cursor = db.cursor()
      sql = "INSERT INTO faq_db(questions, answers, creator, datecreated) VALUES (?, ?, ?, ?)"
      val = (f'{self.question}', f'{self.answer}', f'{creator}', f'{datecreated}')
      cursor.execute(sql, val)
      db.commit()
      db.close()
      
      embed = discord.Embed(title="Success! A new FAQ has been added.", description="", color = discord.Color.green())
      embed.add_field(name="Question", value=f'{self.question}', inline=False)
      embed.add_field(name="Answer", value=f'{self.answer}', inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.set_footer(text=f"Created by {creator} on {datecreated}")

      await interaction.response.send_message(embed=embed, ephemeral=True)
      
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
      await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)


class AddEventModal(discord.ui.Modal, title='Add an Event'):
    name = discord.ui.TextInput(label='Name of event:', style=discord.TextStyle.short, required=True)
    date = discord.ui.TextInput(label="Start date:", style=discord.TextStyle.short, required=True)
    time = discord.ui.TextInput(label="Start time:", style=discord.TextStyle.short, required=True)
    location = discord.ui.TextInput(label="Location:", style=discord.TextStyle.short, required=True)
    description = discord.ui.TextInput(label="Description:", style=discord.TextStyle.long, required=True)

    async def on_submit(self, interaction: discord.Interaction):
      creator = interaction.user
      timestamp = datetime.now()
      datecreated = timestamp.strftime(f"%m/%d/%Y")

      db = sqlite3.connect('db.sqlite')
      cursor = db.cursor()
      sql = "INSERT INTO events_db(name, date, time, location, description, creator, datecreated) VALUES (?, ?, ?, ?, ?, ?, ?)"
      val = (f'{self.name}', f'{self.date}', f'{self.time}', f'{self.location}',f'{self.description}', f'{creator}', f'{datecreated}')
      cursor.execute(sql, val)
      db.commit()
   
      embed = discord.Embed(title="Success! A new event has been added.", description="Here are the details:", color = discord.Color.green())
      embed.add_field(name="Name of Event", value=f'{self.name}', inline=False)
      embed.add_field(name="Start date", value=f'{self.date}', inline=True)
      embed.add_field(name="Start time", value=f'{self.time}', inline=True)
      embed.add_field(name="Location", value=f'{self.location}', inline=False)
      embed.add_field(name="Description", value=f'{self.description}\n\n', inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.set_footer(text=f"Created by {creator} on {datecreated}")
      
      await interaction.response.send_message(embed=embed, ephemeral=True)
      db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
      await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)



client = Client()



### FAQ COMMANDS ###

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

  embed = discord.Embed(title="Success! All FAQ have been cleared from the database", description="", color = discord.Color.green())
  await interaction.response.send_message(embed=embed, ephemeral=True)
  db.commit()
  db.close()


@client.tree.command(name="deletefaq", description = "Delete a FAQ from the database")
async def deletefaq(interaction: discord.Interaction):
  db = sqlite3.connect('db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    SELECT questions FROM faq_db
      ''')
  
  embed = discord.Embed(title="Delete a FAQ", description="Enter the number of the FAQ to delete", color = discord.Color.orange())
  rows = cursor.fetchall()
  count = 1
  for row in rows:
    question = row[0]
    embed.add_field(name=f'{count}- {question}', value='\n', inline= False)
    count += 1
  await interaction.response.send_message(embed=embed, ephemeral=True)

  def check(m):
      return m.author == interaction.user and m.channel == interaction.channel

  selection = await client.wait_for('message', check=check)
  selected_index = int(selection.content) - 1
  selected_row = rows[selected_index]
  cursor.execute('''
    DELETE FROM faq_db WHERE questions=?
    ''', (selected_row[0],))
  
  embed2 = discord.Embed(title=f"Success! FAQ #{int(selection.content)}- {question} has been deleted.", description="", color = discord.Color.green())
  await interaction.followup.send(embed=embed2, ephemeral=True)
  db.commit()
  db.close() 




### EVENT COMMANDS ###

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
  embed = discord.Embed(title="List of all events", description="For more information about an event, type command **/viewevents**", color = discord.Color.blue())
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


@client.tree.command(name="deleteallevents", description="Delete all events from the database")
async def deleteallevents(interaction: discord.Interaction):
  db = sqlite3.connect('db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    DELETE FROM events_db
      ''')

  embed = discord.Embed(title="Success! All events have been cleared from the database", description="", color = discord.Color.green())
  await interaction.response.send_message(embed=embed, ephemeral=True)
  db.commit()
  db.close()


@client.tree.command(name="deleteevent", description = "Delete an event from the database")
async def deleteevent(interaction: discord.Interaction):
  db = sqlite3.connect('db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    SELECT name FROM events_db
      ''')
  embed = discord.Embed(title="Delete an event", description="Enter the number of the event to delete", color = discord.Color.orange())
  rows = cursor.fetchall()
  count = 1
  for row in rows:
    name = row[0]
    embed.add_field(name=f'{count}- {name}', value=f'\n', inline= False)
    count += 1
  
  await interaction.response.send_message(embed=embed, ephemeral=True)

  def check(m):
    return m.author == interaction.user and m.channel == interaction.channel

  selection = await client.wait_for('message', check=check)
  selected_index = int(selection.content) - 1
  selected_row = rows[selected_index]
  cursor.execute('''
    DELETE FROM events_db WHERE name=?
    ''', (selected_row[0],))

  embed2 = discord.Embed(title=f"Success! Event #{int(selection.content)}- {name} has been deleted.", description="", color = discord.Color.green())
  await interaction.followup.send(embed=embed2, ephemeral=True)
  db.commit()
  db.close() 

  


### FAQ SELECT MENU ###
class FaqSelectMenu(discord.ui.Select):
  def __init__(self):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      SELECT questions FROM faq_db
      ''')
    rows = cursor.fetchall()
    if rows:
      options = [discord.SelectOption(label=row[0]) for row in rows]
    else:
      options = [discord.SelectOption(label="There are currently no FAQ", value="none")]
    super().__init__(placeholder="Select a question to view the answer",options=options)
    db.close()

  async def callback(self, interaction: discord.Interaction):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    if self.values[0] == "none":
      await interaction.response.defer()
    db.close()
    return
    cursor.execute('''
      SELECT answers, creator, datecreated FROM faq_db WHERE questions = ?''', [(self.values[0])])
    selected_answer = cursor.fetchone()
    question = self.values[0]
    answer = selected_answer[0]
    creator = selected_answer[1]
    datecreated = selected_answer[2]
    db.close()

    if selected_answer:
      embed = discord.Embed(title=f"{question}", description=f"{answer}", color = discord.Color.yellow())
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.set_footer(text=f"Created by {creator} on {datecreated}")
      await interaction.response.edit_message(embed=embed)
    else:
      await interaction.response.send_message(content="Oops! Something went wrong",ephemeral=True) 

      
class FaqSelectView(discord.ui.View):
     def __init__(self, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(FaqSelectMenu())


@client.tree.command(name="viewfaq", description="View menu of FAQ")
async def viewfaq(interaction: discord.Interaction):
  #embed = discord.Embed(title="Frequently Asked Questions", description="", color = discord.Color.yellow())
  await interaction.response.send_message(view = FaqSelectView(), ephemeral=True)






  ### EVENTS SELECT MENU ###
class EventSelectMenu(discord.ui.Select):
  def __init__(self):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      SELECT name FROM events_db
      ''')
    rows = cursor.fetchall()
    if rows :
      options = [discord.SelectOption(label=row[0]) for row in rows]
    else:
      options = [discord.SelectOption(label="There are currently no events", value="none")]


    super().__init__(placeholder="Select an event to view the event details",options=options)
    db.close()

  async def callback(self, interaction: discord.Interaction):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    if self.values[0] == "none":
        await interaction.response.defer()
        db.close()
        return
    
    cursor.execute('''
      SELECT name, date, time, location, description, creator, datecreated FROM events_db WHERE name = ?
      ''', [(self.values[0])])
    selected_event = cursor.fetchone()
    name = selected_event[0]
    date = selected_event[1]
    time = selected_event[2]
    location = selected_event[3]
    description = selected_event[4]
    creator = selected_event[5]
    datecreated = selected_event[6]
    

    if selected_event:
      embed = discord.Embed(title=f"{name}", description=f"{description}", color = discord.Color.blue())
      embed.add_field(name="When", value=f"{date} at {time}", inline = True)
      embed.add_field(name="Where", value=f"{location}", inline = False)
      embed.add_field(name="Attending ✅ ", value=" ", inline = True)
      embed.add_field(name="Can't Go ❌", value=" ", inline = True)
      embed.add_field(name="Maybe ❔", value=" ", inline = True)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.set_footer(text=f"Created by {creator} on {datecreated}")
      await interaction.response.edit_message(embed=embed)
      db.close()
    else:
      await interaction.response.send_message(content="Oops! Something went wrong",ephemeral=True) 
      db.close()

class EventSelectView(discord.ui.View):
     def __init__(self, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(EventSelectMenu())


@client.tree.command(name="viewevents", description="View menu of events")
async def viewevents(interaction: discord.Interaction):
  await interaction.response.send_message(view = EventSelectView(), ephemeral=True)



  ### SEND EVENT INVITATION COMMAND ###
# Not functioning yet--- goal is to send an embed to the chat with persistent buttons.
# Buttons should be labeled "attending", "can't go", and "maybe".
# When buttons are pressed, the username should be added to the database for that category.
# Embed should update with list of users according to their selection.
class EventInviteMenu(discord.ui.Select):
  def __init__(self):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      SELECT name FROM events_db
      ''')
    rows = cursor.fetchall()
    if rows:
      options = [discord.SelectOption(label=row[0]) for row in rows]
    else:
      options = [discord.SelectOption(label="There are currently no events", value="none")]
    super().__init__(placeholder="Select an event for the invitation",options=options)
    db.close()

  async def callback(self, interaction: discord.Interaction):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    if self.values[0] == "none":
      await interaction.response.defer()
      db.close()
      return
    cursor.execute('''
      SELECT name, date, time, location, description FROM events_db WHERE name = ?
      ''', [(self.values[0])])
    selected_event = cursor.fetchone()
    name = selected_event[0]
    date = selected_event[1]
    time = selected_event[2]
    location = selected_event[3]
    description = selected_event[4]
    
    if selected_event:
      embed = discord.Embed(title=f"{name}", description=f"{description}", color = discord.Color.blue())
      embed.add_field(name="When", value=f"{date} at {time}", inline = False)
      embed.add_field(name="Where", value=f"{location}", inline = False)
      embed.add_field(name="Attending ✅ ", value=" ", inline = True)
      embed.add_field(name="Can't Go ❌", value=" ", inline = True)
      embed.add_field(name="Maybe ❔", value=" ", inline = True)
      embed.add_field(name=" ", value=" ", inline = False)
      embed.add_field(name=" ", value=" ", inline = False)
      embed.add_field(name=" ", value=f"{interaction.user} sent an event invitation. Please RSVP by selecting an option below:", inline = False)
      await interaction.response.send_message(embed=embed, view= EventInviteButtons(), ephemeral=False)
      db.close()
    else:
      await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True) 
      db.close()

class EventInviteView(discord.ui.View):
  def __init__(self, *, timeout=180):
    super().__init__(timeout=timeout)
    self.add_item(EventInviteMenu())

class EventInviteButtons(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)
    @discord.ui.button(label="Attending", style=discord.ButtonStyle.green)
    async def attending(self, interaction:discord.Interaction, Button: discord.ui.Button):
      db = sqlite3.connect('db.sqlite')
      cursor = db.cursor()
      cursor.execute('''
        SELECT name, date, time, location, description FROM events_db WHERE name = ?
        ''', [(self.values[0])])
      selected_event = cursor.fetchone()
    
    @discord.ui.button(label="Can't go", style=discord.ButtonStyle.red)
    async def cantgo(self, interaction:discord.Interaction, Button: discord.ui.Button):
      pass
    
    @discord.ui.button(label="Maybe", style=discord.ButtonStyle.grey)
    async def maybe(self, interaction:discord.Interaction, Button: discord.ui.Button):
      pass
    
   



@client.tree.command(name="eventinvite", description="Send an invitation for an event")
async def eventinvite(interaction: discord.Interaction):
  await interaction.response.send_message(view = EventInviteView(), ephemeral=True)


### Option to bypass interactions and add reaction instead of using buttons
#@client.tree.command(name="eventinvite", description="Send an event invitation")
#async def eventinvite(interaction: discord.Interaction):
#  embed = discord.Embed(title="Events", description="", color = discord.Color.yellow())
#  message = await interaction.channel.send(embed=embed)
#  await message.add_reaction('✅')
#  await message.add_reaction('❌')
#  await message.add_reaction('❔')










client.run(TOKEN)



