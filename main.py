import os
import discord
import tool
import resp
from discord.ext import commands

TOKEN = os.environ['DISCORD_BOT_SECRET']
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
#going to allow us to use client
client = discord.Client(intents=intents)
#adding client.commands to with prefix !
client = commands.Bot(command_prefix='!', intents=intents)


#once loaded this will display in console
@client.event
async def on_ready():
  print(f'Successfully logged in as {client.user}')


#The on_message is going to take in the use message
@client.event
async def on_message(message):
  #checks to see if is the user who sent it rather than the bot
  if message.author == client.user:
    return

  #Going to check to see if the if the message is a command, if   it is it will call it
  #issue here is that cant start a private message
  await client.process_commands(message)

  #This will print the what user send the message, and in what   channel(this for debugging)
  username = str(message.author)
  user_message = str(message.content)
  channel = str(message.channel)
  print(f"{username} said: '{user_message}' ({channel})")

  #start of implementing the private messages
  #if user enters ? before a command it will DM them instead
  #user can then use mattybot in private channel
  if user_message[0] == '?':
    user_message = user_message[1:]  # [1:] Removes the '?'
    await resp.send_message(message, user_message, is_private=True)
  else:
    await resp.send_message(message, user_message, is_private=False)


#message.author.send(response)
#Creating a greading message for leaving and joining
#create a version to get a private DM
#Going to need to find a way to get this private message to work not sure how to do it
@client.event
async def on_member_join(member):
  channel = discord.utils.get(member.guild.channels, name="💬welcome")
  await channel.send(
    f" Welcome to the server {member.mention}.  We are honored to have you!")


@client.event
async def on_member_remove(member):
  channel = discord.utils.get(member.guild.channels, name="💬welcome")
  await channel.send(f" F in the chat for our fallen {member.mention}!")


# Commands
#this will call the drop down menu
@client.command()
async def ask(ctx):
  await ctx.channel.send("Ask away!", view=tool.SelectView())


#this will is just a simple ping pong command
@client.command()
async def hello(ctx):
  await ctx.channel.send(f'Hello! {ctx.author}')


client.run(TOKEN)
