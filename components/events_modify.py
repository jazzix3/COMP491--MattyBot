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

        rows = self.db.query_fetch("SELECT event_name, event_id FROM events_db WHERE server_id = ? ORDER BY start_date ASC", (server_id,))

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
            SelectOption(label="Date and Time", value="dateTime")]

        super().__init__(placeholder="Select a field to modify", options=options)


    async def callback(self, interaction: Interaction):
        event_id = self.event_id
        
        if self.values[0] == "event_name":
            await interaction.response.send_modal(EventNameModal(event_id))
        elif self.values[0] == "description":
            await interaction.response.send_modal(DescriptionModal(event_id))
        elif self.values[0] == "location":
            await interaction.response.send_modal(LocationModal(event_id))
        elif self.values[0] == "dateTime":
            await interaction.response.send_modal(DateTimeModal(event_id))

    

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

        view3 = ModifyButtons(self.event_id, self.new_event_name.value, 'event_name', interaction)
        await interaction.response.edit_message(embed=embed3, view=view3)



class DescriptionModal(ui.Modal, title="Modify an Event"):
    def __init__(self, event_id, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id

    new_description = ui.TextInput(label="New description:", style=TextStyle.paragraph, required=True)

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

        view3 = ModifyButtons(self.event_id, self.new_description.value, 'description', interaction)
        await interaction.response.edit_message(embed=embed3, view=view3)


class LocationModal(ui.Modal, title="Modify an Event"):
    def __init__(self, event_id, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id

    new_location = ui.TextInput(label="New location:", style=TextStyle.short, required=True)

    async def on_submit(self, interaction: Interaction):
        selection = self.db.query_fetch("SELECT location FROM events_db WHERE event_id = ?", (self.event_id,))
        old_location = selection[0][0]

        embed3 = Embed(title="✏️ Would you like to save this modification?", description="", color=discord.Color.green())
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="Old Location:", value=old_location, inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="New Location:", value=self.new_location.value, inline=False)

        view3 = ModifyButtons(self.event_id, self.new_location.value, 'location', interaction)
        await interaction.response.edit_message(embed=embed3, view=view3)


class DateTimeModal(ui.Modal, title="Modify an Event"):
    def __init__(self, event_id, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id

    new_start_date = ui.TextInput(label="New Start Date (e.g. 2023-05-19)", style=TextStyle.short, required=True, min_length=10, max_length=10, placeholder="YYYY-MM-DD")
    new_start_time = ui.TextInput(label="New Start Time (e.g. 08:00 = 8:00 AM)", style=TextStyle.short, required=True, min_length=5, max_length=5, placeholder= "HH:MM")
    new_end_date = ui.TextInput(label="New End Date (e.g. 2023-05-19)", style=TextStyle.short, required=True, min_length=10, max_length=10, placeholder="YYYY-MM-DD")
    new_end_time = ui.TextInput(label="New End Time (e.g. 16:00 = 4:00 PM)", style=TextStyle.short, required=True, min_length=5, max_length=5, placeholder= "HH:MM")

    async def on_submit(self, interaction: Interaction):
        selection = self.db.query_fetch("SELECT start_date, start_time, end_date, end_time FROM events_db WHERE event_id = ?", (self.event_id,))
        old_start_date = selection[0][0]
        old_start_time = selection[0][1]
        old_end_date = selection[0][2]
        old_end_time = selection[0][3]

        embed3 = Embed(title="✏️ Would you like to save this modification?", description="", color=discord.Color.green())
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="Old Start Date and Time:", value=f"{old_start_date} at {old_start_time}", inline=True)
        embed3.add_field(name="Old End Date and Time:", value=f"{old_end_date} at {old_end_time}", inline=True)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="New Start Date and Time:", value=f"{self.new_start_date.value} at {self.new_start_time.value}", inline=True)
        embed3.add_field(name="New End Date and Time:", value=f"{self.new_end_date.value} at {self.new_end_time.value}", inline=True)


        view3 = ModifyDateTimeButtons(self.event_id, self.new_start_date.value, self.new_start_time.value, self.new_end_date.value, self.new_end_time.value, interaction)
        await interaction.response.edit_message(embed=embed3, view=view3)





class ModifyButtons(ui.View):
    def __init__(self, event_id, new_value, field, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id
        self.new_value = new_value
        self.field = field
        
    @discord.ui.button(label="Yes, modify event", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        event_id = self.event_id
        new_value = self.new_value
        field = self.field
        
        try:
            self.db.query(f"UPDATE events_db SET {field} = ? WHERE event_id = ?", new_value, event_id)

            if field == "event_name":
                await GoogleCalendarEvents.ModifyEventCalendar(event_id, new_value, 'summary')
            else:
                await GoogleCalendarEvents.ModifyEventCalendar(event_id, new_value, field)

            for child in self.children: 
                child.disabled = True

        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while adding a new event.", ephemeral=True)
        
        else:
            embed4 = Embed(title=f"Success! The event's `{field}` has been modified.", description=f"", color = discord.Color.green())
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name="", value=f"✏️  Would you like to modify another field for this event?")
            view4=ModifyAnotherButtons(event_id)
            
            await interaction.response.edit_message(embed=embed4, view=view4)

    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"This modification was not saved because the action was cancelled", color = discord.Color.red())
        for child in self.children:
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)



class ModifyDateTimeButtons(ui.View):
    def __init__(self, event_id, new_start_date, new_start_time, new_end_date, new_end_time, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id
        self.new_start_date = new_start_date
        self.new_start_time = new_start_time
        self.new_end_date = new_end_date
        self.new_end_time = new_end_time
        
    @discord.ui.button(label="Yes, modify event", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        event_id = self.event_id
        new_start_date = self.new_start_date
        new_start_time = self.new_start_time
        new_end_date = self.new_end_date
        new_end_time = self.new_end_time
        
        try:
            self.db.query(f"UPDATE events_db SET start_date  = ? WHERE event_id = ?", new_start_date, event_id)
            self.db.query(f"UPDATE events_db SET start_time  = ? WHERE event_id = ?", new_start_time, event_id)
            self.db.query(f"UPDATE events_db SET end_date  = ? WHERE event_id = ?", new_end_date, event_id)
            self.db.query(f"UPDATE events_db SET end_time  = ? WHERE event_id = ?", new_end_time, event_id)
        
            await GoogleCalendarEvents.ModifyDateTimeCalendar(event_id, new_start_date, new_start_time, new_end_date, new_end_time)

            for child in self.children: 
                child.disabled = True

        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while adding a new event.", ephemeral=True)
        
        else:
            embed4 = Embed(title=f"Success! The event's `Date and Time` have been modified.", description=f"", color = discord.Color.green())
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name="", value=f"✏️  Would you like to modify another field for this event?")
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