import discord
from discord import app_commands, ui,  Interaction, SelectOption,  Embed, TextStyle, Color
from discord.ext import commands
from matty_db import Database
from datetime import datetime
from cal_functions import GoogleCalendarEvents



class EventModifyView(ui.View):
    def __init__(self, server_id, *, timeout = None):
         super().__init__(timeout=timeout)
         self.add_item(EventModifyDropdownMenu(server_id))


class EventModifyDropdownMenu(ui.Select):
    def __init__(self, server_id):
        self.db = Database()

        rows = self.db.query_fetch("SELECT event_name, event_id FROM events_db WHERE server_id = ?", (server_id,))

        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no events", value="none")]

        super().__init__(placeholder="Select an event to modify", options=options)


    async def callback(self, interaction: Interaction):
        event_id = self.values[0]

        if event_id == "none":
            await interaction.response.defer()
            return
        
        else:
            embed2 = EventModifyEmbed(event_id)
            view2=EventModifyView2(event_id)
            await interaction.response.edit_message(embed=embed2,view=view2)



class EventModifyView2(ui.View):
    def __init__(self, event_id, *, timeout = None):
         super().__init__(timeout=timeout)
         self.add_item(EventModifyDropdownMenu2(event_id)) 


class EventModifyDropdownMenu2(ui.Select):
    def __init__(self, event_id):
        self.db = Database()
        self.event_id = event_id

        options = [
            SelectOption(label="Event Name", value="event_name"), 
            SelectOption(label="Description", value="description"),
            SelectOption(label="Location", value="location"),
            SelectOption(label="Start Date or Time ", value="start"),
            SelectOption(label="End Date or Time", value="end")]

        super().__init__(placeholder="Select a field to modify", options=options)


    async def callback(self, interaction: Interaction):
        event_id = self.event_id
        
        if self.values[0] == "event_name":
            await interaction.response.send_modal(EventNameModal(event_id))
        if self.values[0] == "description":
            await interaction.response.send_modal(DescriptionModal(event_id))


    

class EventNameModal(ui.Modal, title="Modify an Event"):
    def __init__(self, event_id, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id

    new_event_name = ui.TextInput(label="New event name:", style=TextStyle.short, required=True)

    async def on_submit(self, interaction: Interaction):
        selection = self.db.query_fetch("SELECT event_name FROM events_db WHERE event_id = ?", (self.event_id,))
        old_event_name = selection[0][0]

        embed3 = Embed(title="✏️ Would you like to save this modification?", description="", color=discord.Color.green())
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="Old Event Name:", value=old_event_name, inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="New Event Name:", value=self.new_event_name.value, inline=False)

        view3 = EventNameButtons(self.event_id, self.new_event_name.value, interaction)
        await interaction.response.edit_message(embed=embed3, view=view3)


class EventNameButtons(ui.View):
    def __init__(self, event_id, new_event_name, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id
        self.new_event_name = new_event_name
        
    @discord.ui.button(label="Yes, modify event", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        event_id = self.event_id
        new_event_name = self.new_event_name
        
        try:
            self.db.query("UPDATE events_db SET event_name = ? WHERE event_id = ?", new_event_name, event_id)
            await GoogleCalendarEvents.ModifyEventCalendar(event_id, new_event_name, 'summary')

            for child in self.children: 
                child.disabled = True

        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while adding a new event.", ephemeral=True)
        
        else:
            embed4 = Embed(title="Success! The event name has been modified.", description=f"", color = discord.Color.green())
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name="", value=f"Would you like to modify another field for this event?")
            view4=ModifyAnotherButtons(event_id)
            
            await interaction.response.edit_message(embed=embed4, view=view4)


    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"This modification was not saved because the action was cancelled", color = discord.Color.red())
        for child in self.children:
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)




class DescriptionModal(ui.Modal, title="Modify an Event"):
    def __init__(self, event_id, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id

    new_description = ui.TextInput(label="New description:", style=TextStyle.short, required=True)

    async def on_submit(self, interaction: Interaction):
        selection = self.db.query_fetch("SELECT description FROM events_db WHERE event_id = ?", (self.event_id,))
        old_description = selection[0][0]

        embed3 = Embed(title="✏️ Would you like to save this modification?", description="", color=discord.Color.green())
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="Old Description:", value=old_description, inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="New Description:", value=self.new_description.value, inline=False)

        view3 = DescriptionButtons(self.event_id, self.new_description.value, interaction)
        await interaction.response.edit_message(embed=embed3, view=view3)


class DescriptionButtons(ui.View):
    def __init__(self, event_id, new_description, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id
        self.new_description = new_description
        
    @discord.ui.button(label="Yes, modify event", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        event_id = self.event_id
        new_description = self.new_description
        
        try:
            self.db.query("UPDATE events_db SET description = ? WHERE event_id = ?", new_description, event_id)
            await GoogleCalendarEvents.ModifyEventCalendar(event_id, new_description, 'description')

            for child in self.children: 
                child.disabled = True

        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while adding a new event.", ephemeral=True)
        
        else:
            embed4 = Embed(title="Success! The description has been modified.", description=f"", color = discord.Color.green())
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name="", value=f"Would you like to modify another field for this event?")
            view4=ModifyAnotherButtons(event_id)
            
            await interaction.response.edit_message(embed=embed4, view=view4)


    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"This modification was not saved because the action was cancelled", color = discord.Color.red())
        for child in self.children:
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)














class ModifyAnotherButtons(ui.View):
    def __init__(self, event_id, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id
        
    @discord.ui.button(label="Yes, modify another field", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        event_id = self.event_id
        embed = EventModifyEmbed(event_id)
        view=EventModifyView2(event_id)
        await interaction.response.edit_message(embed=embed,view=view)

    @discord.ui.button(label="No, I'm done", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        event_id = self.event_id
        embed = EventUpdatedEmbed(event_id)
        for child in self.children:
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)











class EventModifyEmbed(Embed):
    def __init__(self, event_id):
        super().__init__()
        self.db = Database()
        self.event_id = event_id
        

        selection = self.db.query_fetch("SELECT event_name, description, location, start_date, start_time, end_date, end_time FROM events_db WHERE event_id = ?", (self.event_id,))
        event_name = selection[0][0]
        description = selection[0][1]
        location = selection[0][2]
        start_date = selection[0][3]
        start_time = selection[0][4]
        end_date = selection[0][5]
        end_time = selection[0][6]

        super().__init__(title=f"✏️ You are modifying the event: `{event_name}`", description=description, color=Color.blue())
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="⏰ Starts: ", value=f"{start_date} at {start_time}", inline = True)
        self.add_field(name="⏰ Ends:", value=f"{end_date} at {end_time}", inline = True)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="📍 Location", value=location, inline = True)


class EventUpdatedEmbed(Embed):
    def __init__(self, event_id):
        super().__init__()
        self.db = Database()
        self.event_id = event_id
        

        selection = self.db.query_fetch("SELECT event_name, description, location, start_date, start_time, end_date, end_time FROM events_db WHERE event_id = ?", (self.event_id,))
        event_name = selection[0][0]
        description = selection[0][1]
        location = selection[0][2]
        start_date = selection[0][3]
        start_time = selection[0][4]
        end_date = selection[0][5]
        end_time = selection[0][6]

        super().__init__(title=f"✨ Here is the updated information for the event: `{event_name}`", description=description, color=Color.blue())
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="⏰ Starts: ", value=f"{start_date} at {start_time}", inline = True)
        self.add_field(name="⏰ Ends:", value=f"{end_date} at {end_time}", inline = True)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="📍 Location", value=location, inline = True)