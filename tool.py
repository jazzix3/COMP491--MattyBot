#this is the drop down menu code (command)
import discord

class Select(discord.ui.Select):
     def __init__(self):
         options=[
             discord.SelectOption(label="Hello!",emoji="👌"),
             discord.SelectOption(label="Game Hours",emoji="✨"),
             discord.SelectOption(label="Game Room Location",emoji="🎭")
             ]
         super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)

     async def callback(self, interaction: discord.Interaction):
         if self.values[0] == "Hello!":
             await interaction.response.send_message(content="Hello there!!!",ephemeral=False)

         elif self.values[0] == "Game Hours":
             await interaction.response.send_message("The game room hours are from 10am Monday through Friday \nBUT sometimes our teams will be practicing on certain Mondays,Tuesdays, Fridays and if they are, the Game Room would start wrapping up around 5:30 to prep for our teams from 6-8pm!",ephemeral=False)

         elif self.values[0] == "Game Room Location":
             await interaction.response.send_message("The USU Games Room is located in the lower level of the East Conference Center, across from the Student Recreation Center. \nFor more information visit the website\nhttps://www.csun.edu/src/games-room%27%27",ephemeral=False)
           
class SelectView(discord.ui.View):
     def __init__(self, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(Select())