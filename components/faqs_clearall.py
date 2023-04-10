import discord
from discord import ui, TextStyle, Interaction, Embed, Color
from matty_db import Database 
from cal_functions import GoogleCalendarEvents



class ClearAllEmbed(Embed):
    def __init__(self):
        super().__init__(title="❗ Are you sure you want to `CLEAR all` FAQs? ❗", description="", color=Color.orange())
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value="This will delete all FAQs from the database and calendar **forever**", inline=False)
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value="⚠️ Warning: Action cannot be undone", inline=False)


class ClearAllButtons(ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()

    @discord.ui.button(label="Yes, clear all FAQs", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        self.db.query("DELETE FROM faqs_db")
        embed = Embed(title=" ", description="Success! All FAQs have been cleared from the database", color=Color.green())
        for child in self.children: 
            child.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"FAQs were **NOT** cleared because the action was cancelled.", color = discord.Color.red())
        for child in self.children: 
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)