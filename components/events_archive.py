import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database



class ArchiveEventEmbed(Embed):
    def __init__(self, event_name, description, location, start_date, start_time, end_date, end_time):
        super().__init__(title="❗ Are you sure you want to `ARCHIVE` this event? ❗", description="", color=Color.blue())
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=f"📅  `{event_name}`", value=description)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="⏰ Starts: ", value=f"{start_date} at {start_time}", inline = True)
        self.add_field(name="⏰ Ends:", value=f"{end_date} at {end_time}", inline = True)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="📍 Location", value=location, inline = True)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="This action will move the event to the archive. Archived events can be viewed using command **/archive**", value=" ", inline=False)



class ArchiveEventButtons(ui.View):
    def __init__(self, event_id, event_name, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id
        self.event_name = event_name
        

    @discord.ui.button(label="Yes, move it", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        event_id = self.event_id
        event_name = self.event_name
        self.db.query("INSERT INTO archive_db SELECT * FROM events_db WHERE event_id = ?", event_id)
        self.db.query("DELETE FROM events_db WHERE event_id = ?", event_id)
        
        embed = Embed(title="", description=f"`{event_name}` has been archived!", color = discord.Color.green())
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)


    @discord.ui.button(label="No, keep it", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        event_name = self.event_name
        embed = Embed(title="", description=f"`{event_name}` was **not** archived because the action was cancelled.", color = discord.Color.red())
        for child in self.children: 
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)