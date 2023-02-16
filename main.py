import os
import discord
import dotenv
import sqlite3
from datetime import datetime
from discord.ext import commands
from discord import ui, app_commands


dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

class Client(discord.Client):
  def __init__(self) -> None:
      intents = discord.Intents.default()
      intents.message_content = True
      super().__init__(command_prefix='!', intents=intents) 
      self.tree = app_commands.CommandTree(self)    # Enables slash commands

  async def setup_hook(self) -> None:
      await self.tree.sync()    # Syncs the application command with Discord
      print(f'Successfully synced slash commands')

  async def on_ready(self):     
    print(f'Successfully logged in as {client.user}')   # Prints message in console if online
    db = sqlite3.connect('db.sqlite')   # Establish database connection and creates tables
    cursor = db.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS faq_db(
        faq_id INTEGER PRIMARY KEY AUTOINCREMENT,
        questions TEXT,
        answers TEXT,
        creator TEXT,
        datecreated TEXT)
        ''')
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS events_db(
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT,
        date TEXT,
        time TEXT,
        location TEXT,
        description TEXT,
        creator TEXT,
        datecreated TEXT)
        ''')
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS responses_db(
        response_id INTEGER PRIMARY KEY,
        event_id INT NOT NULL,
        username TEXT NOT NULL,
        response TEXT NOT NULL,
        FOREIGN KEY(event_id) REFERENCES events_db(event_id))
        ''')
    db.commit()
    db.close()

client = Client()

class AddFaqModal(discord.ui.Modal, title='Add to FAQ'):
    question = discord.ui.TextInput(label='Question', style=discord.TextStyle.short, required=True)
    answer = discord.ui.TextInput(label="Answer:", style=discord.TextStyle.long, required=True)

    async def on_submit(self, interaction: discord.Interaction):
      creator = interaction.user.name
      timestamp = datetime.now()
      datecreated = timestamp.strftime(f"%m/%d/%Y")
      
      db = sqlite3.connect('db.sqlite')
      cursor = db.cursor()
      sql = "INSERT INTO faq_db(questions, answers, creator, datecreated) VALUES (?, ?, ?, ?)"
      val = (self.question.value, self.answer.value, creator, datecreated)
      cursor.execute(sql, val)
      db.commit()
      
      embed = discord.Embed(title="Success! A new FAQ has been added.", description="", color = discord.Color.green())
      embed.add_field(name="Question", value=f'{self.question}', inline=False)
      embed.add_field(name="Answer", value=f'{self.answer}', inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.set_footer(text=f"Created by {creator} on {datecreated}")
      await interaction.response.send_message(embed=embed, ephemeral=True)
      db.close()
      
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
      await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)



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
    rows = cursor.fetchall()
    if rows:
        embed = discord.Embed(title="List of all FAQ", description="To ask a question, type command **/viewfaq**", color = discord.Color.orange())
        count = 1
        for row in rows:
            question = row[0]
            embed.add_field(name=f'{count}- {question}', value='\n', inline= False)
            count += 1
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed2 = discord.Embed(title="List of all FAQ", description ="There are currently no FAQ", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed2, ephemeral=True)
    db.close()


### Possibly delete??? 
# Do we need this command since we have /viewfaq?
@client.tree.command(name="listanswers", description="View a list of all answers from FAQ")
async def listanswers(interaction:discord.Interaction):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      SELECT answers FROM faq_db
        ''')
    embed = discord.Embed(title="List of all answers", description="Answers to the FAQ", color = discord.Color.orange())
    rows = cursor.fetchall()
    count = 1
    if rows:
      for row in rows:
        answer = row[0]
        embed.add_field(name=f'{count}- {answer}', value='\n', inline= False)
        count += 1
      await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed2 = discord.Embed(title="List of all answers", description ="There are currently no FAQ", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed2)
    db.close()


@client.tree.command(name="clearallfaq", description="Clear all FAQ from the database")
async def clearallfaq(interaction: discord.Interaction):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      DELETE FROM faq_db
        ''')
    embed = discord.Embed(title="Clear all FAQ", description="Success! All FAQ have been cleared from the database", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, ephemeral=True)
    db.commit()
    db.close()

### Need to catch error if user input is invalid. 
# Should we use drop down instead?
# Or possibly DM user (to prevent user from sending their response message into the channel) 
# is there a way to hide their response?
@client.tree.command(name="deletefaq", description = "Delete a FAQ from the database")
async def deletefaq(interaction: discord.Interaction):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      SELECT faq_id, questions questions FROM faq_db
        ''')
    
    embed = discord.Embed(title="Delete a FAQ", description="Enter the number of the FAQ to delete", color = discord.Color.orange())
    rows = cursor.fetchall()
    count = 1
    if rows:
      for row in rows:
        question = row[1]
        embed.add_field(name=f'{count}- {question}', value='\n', inline= False)
        count += 1
      await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
      embed2 = discord.Embed(title="Delete a FAQ", description ="There are currently no FAQ", color=discord.Color.orange())
      await interaction.response.send_message(embed=embed2, ephemeral=True)

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    selection = await client.wait_for('message', check=check, timeout=60)
    selected_index = int(selection.content) - 1
    selected_row = rows[selected_index]
    cursor.execute('''
      DELETE FROM faq_db WHERE faq_id = ?
      ''', (selected_row[0],))
    
    embed3 = discord.Embed(title="Delete a FAQ", description=f"Success! FAQ #{int(selection.content)} has been deleted.", color = discord.Color.green())
    await interaction.followup.send(embed=embed3, ephemeral=True)
    db.commit()
    db.close()



### EVENT COMMANDS ###

class AddEventModal(discord.ui.Modal, title='Add an Event'):
    event_name = discord.ui.TextInput(label='Name of event:', style=discord.TextStyle.short, required=True)
    date = discord.ui.TextInput(label="Start date:", style=discord.TextStyle.short, required=True)
    time = discord.ui.TextInput(label="Start time:", style=discord.TextStyle.short, required=True)
    location = discord.ui.TextInput(label="Location:", style=discord.TextStyle.short, required=True)
    description = discord.ui.TextInput(label="Description:", style=discord.TextStyle.long, required=True)

    async def on_submit(self, interaction: discord.Interaction):
      creator = interaction.user.name
      timestamp = datetime.now()
      datecreated = timestamp.strftime(f"%m/%d/%Y")

      db = sqlite3.connect('db.sqlite')
      cursor = db.cursor()
      sql = "INSERT INTO events_db(event_name, date, time, location, description, creator, datecreated) VALUES (?, ?, ?, ?, ?, ?, ?)"
      val = (self.event_name.value, self.date.value, self.time.value, self.location.value, self.description.value, creator, datecreated)
      cursor.execute(sql, val)
      db.commit()
   
      embed = discord.Embed(title="Success! A new event has been added.", description="To send an invitation for this event, type command **/eventinvite**", color = discord.Color.green())
      embed.add_field(name="Name of Event", value=f'{self.event_name}', inline=False)
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


@client.tree.command(name="addevent", description="Add an event")
async def addevent(interaction: discord.Interaction):
    await interaction.response.send_modal(AddEventModal())


@client.tree.command(name="listevents", description="View a list of all Events")
async def listevents(interaction:discord.Interaction):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      SELECT event_name, date, time FROM events_db
        ''')
    embed = discord.Embed(title="List of all events", description="For more information about an event, type command **/viewevents**", color = discord.Color.blue())
    rows = cursor.fetchall()
    count = 1
    if rows:
      for row in rows:
        event_name = row[0]
        date = row[1]
        time = row[2]
        embed.add_field(name=f'{count}- {event_name}', value=f'{date} at {time}', inline= False)
        count += 1
      await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
      embed2 = discord.Embed(title="List of all events", description ="There are currently no events", color=discord.Color.blue())
      await interaction.response.send_message(embed=embed2, ephemeral=True)
    db.commit()
    db.close()


@client.tree.command(name="clearallevents", description="Clear all events from the database")
async def clearallevents(interaction: discord.Interaction):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      DELETE FROM events_db
        ''')

    embed = discord.Embed(title="Clear all events", description="Success! All events have been cleared from the database", color = discord.Color.green())
    await interaction.response.send_message(embed=embed, ephemeral=True)
    db.commit()
    db.close()

### Need to catch error if user input is invalid. 
# Should we use drop down instead?
# Or possibly DM user (to prevent user from sending their response message into the channel) 
# is there a way to hide their response?
@client.tree.command(name="deleteevent", description = "Delete an event from the database")
async def deleteevent(interaction: discord.Interaction):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      SELECT event_name FROM events_db
        ''')
    embed = discord.Embed(title="Delete an event", description="Enter the number of the event to delete", color = discord.Color.orange())
    rows = cursor.fetchall()
    count = 1
    if rows:
      for row in rows:
        event_name = row[0]
        embed.add_field(name=f'{count}- {event_name}', value=f'\n', inline= False)
        count += 1
      await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
      embed2 = discord.Embed(title="Delete an event", description ="There are currently no events", color=discord.Color.blue())
      await interaction.response.send_message(embed=embed2, ephemeral=True)


    def check(m):
      return m.author == interaction.user and m.channel == interaction.channel

    selection = await client.wait_for('message', check=check, timeout=60)
    selected_index = int(selection.content) - 1
    selected_row = rows[selected_index]
    cursor.execute('''
      DELETE FROM events_db WHERE event_name=?
      ''', (selected_row[0],))

    embed3 = discord.Embed(title="Delete an event", description=f"Success! Event #{int(selection.content)}- {event_name} has been deleted.", color = discord.Color.green())
    await interaction.followup.send(embed=embed3, ephemeral=True)
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
      return
    cursor.execute('''
      SELECT answers, creator, datecreated FROM faq_db WHERE questions = ?''', [(self.values[0])])
    selected_answer = cursor.fetchone()
    question = self.values[0]
    answer = selected_answer[0]
    creator = selected_answer[1]
    datecreated = selected_answer[2]


    if selected_answer:
      embed = discord.Embed(title=f"{question}", description=f"{answer}", color = discord.Color.yellow())
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.set_footer(text=f"Created by {creator} on {datecreated}")
      await interaction.response.edit_message(embed=embed)
    else:
      await interaction.response.send_message(content="Oops! Something went wrong",ephemeral=True)
    db.close()

      
class FaqSelectView(discord.ui.View):
     def __init__(self, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(FaqSelectMenu())


@client.tree.command(name="viewfaq", description="View menu of FAQ")
async def viewfaq(interaction: discord.Interaction):
  await interaction.response.send_message(view = FaqSelectView(), ephemeral=True)




  ### EVENTS SELECT MENU ###
class EventSelectMenu(discord.ui.Select):
  def __init__(self):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      SELECT event_name FROM events_db
      ''')
    rows = cursor.fetchall()
    if rows :
      options = [discord.SelectOption(label=row[0]) for row in rows]
    else:
      options = [discord.SelectOption(label="There are currently no events", value="none")]
    super().__init__(placeholder="Select an event to view the event details",options=options)


  async def callback(self, interaction: discord.Interaction):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    if self.values[0] == "none":
        await interaction.response.defer()
        return
    
    cursor.execute('''
      SELECT event_name, date, time, location, description, creator, datecreated FROM events_db WHERE event_name = ?
      ''', [(self.values[0])])
    selected_event = cursor.fetchone()
    event_name = selected_event[0]
    date = selected_event[1]
    time = selected_event[2]
    location = selected_event[3]
    description = selected_event[4]
    creator = selected_event[5]
    datecreated = selected_event[6]
    

    if selected_event:
      embed = discord.Embed(title=f"{event_name}", description=f"{description}", color = discord.Color.blue())
      embed.add_field(name="When", value=f"{date} at {time}", inline = True)
      embed.add_field(name="Where", value=f"{location}", inline = False)
      embed.add_field(name="Attending ✅ ", value=" ", inline = True)
      embed.add_field(name="Can't Go ❌", value=" ", inline = True)
      embed.add_field(name="Maybe ❔", value=" ", inline = True)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.set_footer(text=f"Created by {creator} on {datecreated}")
      await interaction.response.edit_message(embed=embed)
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
# Need to delete/disable original message with drop down to prevent sending more than 1 invite at a time
class EventInviteMenu(discord.ui.Select):
  def __init__(self):
    db = sqlite3.connect('db.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      SELECT event_name FROM events_db
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
      return
    cursor.execute('''
      SELECT event_name, date, time, location, description FROM events_db WHERE event_name = ?
      ''', [(self.values[0])])
    selected_event = cursor.fetchone()


    if selected_event:
      embed = discord.Embed(title=f"{selected_event[0]}", description=f"{selected_event[4]}", color = discord.Color.blue())
      embed.add_field(name="When", value=f"{selected_event[1]} at {selected_event[2]}", inline = False)
      embed.add_field(name="Where", value=f"{selected_event[3]}", inline = False)
      embed.add_field(name="Attending ✅ ", value=" ", inline = True)
      embed.add_field(name="Can't Go ❌", value=" ", inline = True)
      embed.add_field(name="Maybe ❔", value=" ", inline = True)
      embed.add_field(name=" ", value=" ", inline = False)
      embed.add_field(name=" ", value=" ", inline = False)
      embed.add_field(name=" ", value=f"{interaction.user.name} sent an event invitation. Please RSVP by selecting an option below:", inline = False)
      view = EventInviteButtons(selected_event=selected_event)
      await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
    else:
      await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True) 
    db.close()
      

class EventInviteButtons(discord.ui.View):
    def __init__(self, *, selected_event, timeout=None):
        super().__init__(timeout=timeout)
        self.selected_event = selected_event
    
    @discord.ui.button(label="Attending", style=discord.ButtonStyle.green)
    async def attending(self, interaction:discord.Interaction, button: discord.ui.Button):
      pass
    
    @discord.ui.button(label="Can't go", style=discord.ButtonStyle.red)
    async def cantgo(self, interaction:discord.Interaction, Button: discord.ui.Button):
      pass
    
    @discord.ui.button(label="Maybe", style=discord.ButtonStyle.grey)
    async def maybe(self, interaction:discord.Interaction, Button: discord.ui.Button):
      pass

class EventInviteView(discord.ui.View):
  def __init__(self, *, timeout=180):
    super().__init__(timeout=timeout)
    self.add_item(EventInviteMenu())
        

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