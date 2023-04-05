import discord
from discord import app_commands, ui,  Interaction, SelectOption,  Embed, TextStyle, Color
from discord.ext import commands
from matty_db import Database
from datetime import datetime
from cal_functions import GoogleCalendarEvents



class EventEditView(ui.View):
    def __init__(self, server_id, *, timeout = None):
         super().__init__(timeout=timeout)
         self.add_item(EventEditDropdownMenu(server_id))


class EventEditDropdownMenu(ui.Select):
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
            embed2 = EventEditEmbed(event_id)
            view2=EventEditView2(event_id)
            await interaction.response.edit_message(embed=embed2,view=view2)



class EventEditView2(ui.View):
    def __init__(self, event_id, *, timeout = None):
         super().__init__(timeout=timeout)
         self.add_item(EventEditDropdownMenu2(event_id)) 


class EventEditDropdownMenu2(ui.Select):
    def __init__(self, event_id):
        self.db = Database()
        event_id = event_id

        options = [
            SelectOption(label="Event Name", value="event_name"), 
            SelectOption(label="Description", value="description"),
            SelectOption(label="Location", value="location"),
            SelectOption(label="Start Date ", value="start_date"),
            SelectOption(label="Start Time", value="start_time"),
            SelectOption(label="End Date", value="end_date"),
            SelectOption(label="End Time", value="end_time")]

        super().__init__(placeholder="Select a field to modify", options=options)


    async def callback(self, interaction: Interaction):
        if self.values[0] == "event_name":
            await interaction.response.send_modal(EventNameModal())


    

class EventNameModal(ui.Modal, title="Modify an Event"):
    event_name = ui.TextInput(label="Event Name", style=TextStyle.short, required=True)

    
    async def on_submit(self, interaction: Interaction):
        embed = Embed(title="Is this correct?", description="", color=discord.Color.blue())
        embed.add_field(name="Event Name", value=self.event_name, inline=False)

        #view = Buttons1(self.event_name)

        await interaction.response.send_message(embed=embed, ephemeral=True)





class Buttons1(ui.View):
    def __init__(self, event_name, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_name = event_name
        self.interaction = interaction

    @discord.ui.button(label="Yes, save this modification", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        #event_name = self.event_name
    
        pass
        #await interaction.response.send_modal(Modal2(event_name, description, location))
        
    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"Event was not modified because the action was cancelled.", color = discord.Color.red())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self) 









class EventEditEmbed(Embed):
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

