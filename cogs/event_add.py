import discord
from discord import app_commands, ui,  Interaction, Embed, TextStyle, Color
from discord.ext import commands
from matty_db import Database
from datetime import datetime
from cal_functions import GoogleCalendarEvents


class AddEvent(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.db = Database()

    admin = app_commands.Group(name="modals", description="Frequently Asked Questions")

    @admin.command(name="test", description="Add a question & answer to FAQs (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def testadd(self, interaction: Interaction) -> None:
        await interaction.response.send_modal(Modal1()) 
    @testadd.error
    async def testadd(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 


class Modal1(ui.Modal, title="Add an Event (Page 1 of 2)"):
    event_name = ui.TextInput(label="Event Name", style=TextStyle.short, required=True)
    description = ui.TextInput(label="Description", style=TextStyle.long, required=True)
    

    async def on_submit(self, interaction: Interaction):
        embed = Embed(title="Is this event information is correct? (Page 1 of 2)", description="", color=discord.Color.green())
        embed.add_field(name="Event Name", value=self.event_name, inline=False)
        embed.add_field(name="Description", value=self.description, inline=False)
        view = Buttons1(self.event_name, self.description, interaction)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class Buttons1(ui.View):
    def __init__(self, event_name, description, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_name = event_name
        self.description = description
        self.interaction = interaction

    @discord.ui.button(label="Yes, continue", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        event_name = self.event_name
        description = self.description
        await interaction.response.send_modal(Modal2(event_name,description))
        
    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"Event was not created because the action was cancelled.", color = discord.Color.red())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self) 


class Modal2(ui.Modal, title="Add an Event (Page 2 of 2)"):
    def __init__(self, event_name, description, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_name = event_name
        self.description= description

    location = ui.TextInput(label="Location", style=TextStyle.short, required=True)
    start_date = ui.TextInput(label="Start Date", style=TextStyle.short, required=True)
    start_time = ui.TextInput(label="Start Time", style=TextStyle.short, required=True)
    end_date = ui.TextInput(label="End Date", style=TextStyle.short, required=True)
    end_time = ui.TextInput(label="End Time", style=TextStyle.short, required=True)

    async def on_submit(self, interaction: Interaction):
        embed2 = Embed(title="Is this event information correct? (Page 2 of 2)", description="", color=discord.Color.green())
        embed2.add_field(name="Location", value=self.location, inline=False)
        embed2.add_field(name="Start date", value=self.start_date, inline=False)
        embed2.add_field(name="Start time", value=self.start_time, inline=False)
        embed2.add_field(name="End date", value=self.end_date, inline=False)
        embed2.add_field(name="End time", value=self.end_time, inline=False)
        view2 = Buttons2(self.event_name, self.description, self.location, self.start_date, self.start_time, self.end_date, self.end_time, interaction)
        await interaction.response.edit_message(embed=embed2, view=view2)


class Buttons2(ui.View):
    def __init__(self, event_name, description, location, start_date, start_time, end_date, end_time, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_name = event_name
        self.description = description
        self.location = location
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.interaction = interaction

    @discord.ui.button(label="Yes, continue", style=discord.ButtonStyle.green)
    async def next(self, interaction: Interaction, button: ui.Button):
        event_name = self.event_name
        description = self.description
        location = self.location
        start_date = self.start_date
        start_time = self.start_time
        end_date = self.end_date
        end_time = self.end_time
        
        embed3 = Embed(title=f"Confirm all event details are correct", description="", color=discord.Color.green())
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=f"`{event_name}`", value=description, inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="📍 Location", value=location, inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="📅 Start date", value=start_date, inline=True)
        embed3.add_field(name="⏰ Start time", value=start_time, inline=True)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="📅 End date", value=end_date, inline=True)
        embed3.add_field(name="⏰ End time", value=end_time, inline=True)
        view3 = Buttons3(self.event_name, self.description, self.location, self.start_date, self.start_time, self.end_date, self.end_time, interaction)
        await interaction.response.edit_message(embed=embed3, view=view3)

    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"Event was not created because the action was cancelled.", color = discord.Color.red())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self) 


class Buttons3(ui.View):
    def __init__(self, event_name, description, location, start_date, start_time, end_date, end_time, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_name = event_name
        self.description = description
        self.location = location
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.interaction = interaction
        
    @discord.ui.button(label="Add Event to Calendar", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        server_id = interaction.guild_id
        creator = interaction.user.name
        timestamp = datetime.now()
        datecreated = timestamp.strftime(f"%m/%d/%Y")

        try:  
            event_link, event_id = GoogleCalendarEvents.AddToCalendar(self.event_name, self.location, self.description, self.start_date, self.start_time, self.end_date, self.end_time)
        
            sql = "INSERT INTO events_db(event_id, server_id, event_name, description, location, start_date, start_time, end_date, end_time, event_link, creator, datecreated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (event_id, server_id, self.event_name.value, self.description.value, self.location.value, self.start_date.value, self.start_time.value, self.end_date.value, self.end_time.value, event_link, creator, datecreated)
            self.db.query_input(sql,val)


            embed4 = Embed(title="Success! A new event has been added.", description="To send an invitation for this event, type command **/event-- invite**",color = Color.green())
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=f"`{self.event_name}`", value=self.description, inline=False)
            embed4.add_field(name="📍 Location", value=self.location, inline=False)
            embed4.add_field(name="📅 Start date", value=self.start_date, inline=True)
            embed4.add_field(name="⏰ Start time", value=self.start_time, inline=True)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name="📅 End date", value=self.end_date, inline=True)
            embed4.add_field(name="⏰ End time", value=self.end_time, inline=True)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name="Link to Google Calendar:", value=f"{event_link}", inline=False)
            embed4.set_footer(text=f"Created by {creator} on {datecreated}")

            for child in self.children: 
                child.disabled = True
            await interaction.response.edit_message(embed=embed4, view=self)

        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.edit_message("Oops! Something went wrong while adding a new event.")
        




       

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"Event was not created because the action was cancelled.", color = discord.Color.red())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self) 
        

class AdminErrorEmbed(Embed):
    def __init__(self):
        super().__init__()
        self.db = Database()

        super().__init__(title="", description=f"You must have the role `MattyBotAdmin` to use that command", color=Color.red())        

async def setup(client: commands.Bot) -> None:
    await client.add_cog(AddEvent(client))



"""
OLD ADD EVENTS CLASS USING DB ONLY--- KEEPING FOR NOW, JUST IN CASE

class AddEventModal(ui.Modal, title="Add an Event"):
    db = Database()
    event_name = ui.TextInput(label="Name of event:", style=TextStyle.short, required=True)
    date = ui.TextInput(label="Start date:", style=TextStyle.short, required=True)
    time = ui.TextInput(label="Start time:", style=TextStyle.short, required=True)
    location = ui.TextInput(label="Location:", style=TextStyle.short, required=True)
    description = ui.TextInput(label="Description:", style=TextStyle.long, required=True)

    async def on_submit(self, interaction: Interaction):
        server_id = interaction.guild_id
        creator = interaction.user.name
        timestamp = datetime.now()
        datecreated = timestamp.strftime(f"%m/%d/%Y")
    
        try:
            sql = "INSERT INTO events_db(server_id, event_name, date, time, location, description, creator, datecreated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            val = (server_id, self.event_name.value, self.date.value, self.time.value, self.location.value, self.description.value, creator, datecreated)
            self.db.query_input(sql, val)

            event_name = self.event_name.value
            location = self.location.value
            description = self.description.value
            GoogleCalendarEvents.AddToCalendar(event_name, location, description)

            embed = Embed(title="Success! A new event has been added.", description="To send an invitation for this event, type command **/eventinvite**",color = Color.green())
            embed.add_field(name="Name of Event", value=self.event_name, inline=False)
            embed.add_field(name="Start date", value=self.date, inline=True)
            embed.add_field(name="Start time", value=self.time, inline=True)
            embed.add_field(name="Location", value=self.location, inline=False)
            embed.add_field(name="Description", value=self.description, inline=False)
            embed.add_field(name=" ", value=" ", inline=False)
            embed.add_field(name=" ", value=" ", inline=False)
            embed.set_footer(text=f"Created by {creator} on {datecreated}")

        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while adding a new event.", ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
"""