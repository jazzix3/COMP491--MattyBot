import discord
from discord import ui, TextStyle, Interaction, Embed, Color
from matty_db import Database 
from cal_functions import GoogleCalendarEvents




class ClearAllEmbed(Embed):
    def __init__(self):
        super().__init__(title="❗ Are you sure you want to `CLEAR all` events? ❗", description="", color=Color.orange())
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value="This will delete all events from the database and calendar **forever**", inline=False)
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value="⚠️ Warning: Action cannot be undone", inline=False)



class ClearAllButtons(ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()

    @discord.ui.button(label="Yes, clear all events", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        try:
            self.db.query("DELETE FROM events_db")
            await GoogleCalendarEvents.ClearCalendar()
        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while clearing all events.", ephemeral=True)
        else:
            embed = Embed(title=" ", description="Success! All events have been cleared from the database and calendar", color=Color.green())
            for child in self.children:
                child.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"events were **NOT** cleared because the action was cancelled.", color = discord.Color.red())
        for child in self.children: 
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)