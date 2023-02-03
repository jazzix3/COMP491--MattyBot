import os
import discord
import dotenv
import tool
import resp
import sqlite3
from discord.ext import commands




dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)



@client.event
async def on_ready():
  # Print message in consol if online
  print(f'Successfully logged in as {client.user}')
  
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


@client.event
async def on_message(message):
  # Checks if it the user sent the message rather than the bot
  if message.author == client.user:
    return

  # If message is a command, it will call the function
  ## issue here is that cant start a private message
  
  await client.process_commands(message)

  # Used for debugging---  will print username that send the message and channel sent from
  username = str(message.author)
  user_message = str(message.content)
  channel = str(message.channel)
  print(f"{username} said: '{user_message}' ({channel})")

  # Enables Private messages-- if user enters ? before a command it will DM them instead
  ## user can then use mattybot in private channel
  if user_message[0] == '?':
    user_message = user_message[1:]  # [1:] Removes the '?'
    await resp.send_message(message, user_message, is_private=True)
  else:
    await resp.send_message(message, user_message, is_private=False)


# Enables greeting for users leaving or joining server
@client.event
async def on_member_join(member):
  channel = discord.utils.get(member.guild.channels, name="💬welcome")
  await channel.send(
    f" Welcome to the server {member.mention}.  We are honored to have you!")
@client.event
async def on_member_remove(member):
  channel = discord.utils.get(member.guild.channels, name="💬welcome")
  await channel.send(f" F in the chat for our fallen {member.mention}!")



@client.command()
async def addfaq(ctx):
  db = sqlite3.connect('faq_db.sqlite')
  cursor = db.cursor()
  cursor.execute(''' 
    INSERT INTO faq_db(question, answer) VALUES (?, ?)
    ''', ['Is this working?', 'Yes'])
  db.commit()
  db.close()

@client.command()
async def listfaq(ctx):
  db = sqlite3.connect('faq_db.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    SELECT question FROM faq_db
      ''')
  result = cursor.fetchall()
  await ctx.channel.send(f'{result}')
  db.commit()
  db.close()



# Command calls select menu
@client.command()
async def ask(ctx):
  await ctx.channel.send("Ask away!", view=tool.SelectView())


# Command for simple ping-pong
@client.command()
async def hello(ctx):
  await ctx.channel.send(f'Hello! {ctx.author}')

client.run(TOKEN)
