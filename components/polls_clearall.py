import discord
from discord import ui, TextStyle, Interaction, Embed, Color
from matty_db import Database 


class ClearAllEmbed(Embed):
    def __init__(self):
        super().__init__(title="❗ Are you sure you want to `CLEAR all` polls? ❗", description="", color=Color.orange())
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value="This will delete all polls from the database **forever**", inline=False)
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value="⚠️ Warning: Action cannot be undone", inline=False)


class ClearAllButtons(ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()

    @discord.ui.button(label="Yes, clear all polls", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        try:
            self.db.query("DELETE FROM polls_db")
        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while clearing all polls.", ephemeral=True)
        else:
            embed = Embed(title=" ", description="Success! All polls have been cleared from the database", color=Color.green())
            for child in self.children:
                child.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"polls were **NOT** cleared because the action was cancelled.", color = discord.Color.red())
        for child in self.children: 
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)