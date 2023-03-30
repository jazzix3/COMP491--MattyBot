import discord
from discord import ui, TextStyle, Interaction, Embed, Color
from matty_db import Database 
from datetime import datetime



class AddFaqModal(ui.Modal, title="Add to FAQ"):
    db = Database()
    question = ui.TextInput(label="Question", style=TextStyle.short, required=True)
    answer = ui.TextInput(label="Answer:", style=TextStyle.long, required=True)

    async def on_submit(self, interaction: Interaction):
        server_id = interaction.guild_id
        creator = interaction.user.name
        timestamp = datetime.now()
        datecreated = timestamp.strftime(f"%m/%d/%Y")
        
        embed = Embed(title="Success! A new FAQ has been added.", description="To see all FAQs, type command **/FAQs**", color = Color.green())
        embed.add_field(name="Question", value=self.question, inline=False)
        embed.add_field(name="Answer", value=self.answer, inline=False)
        embed.add_field(name=" ", value=" ", inline=False)
        embed.add_field(name=" ", value=" ", inline=False)
        embed.set_footer(text=f"Created by {creator} on {datecreated}")

        try:
            sql = "INSERT INTO faqs_db(server_id, question, answer, creator, datecreated) VALUES (?, ?, ?, ?, ?)"
            val = (server_id, self.question.value, self.answer.value, creator, datecreated)
            self.db.query_input(sql,val)
        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while adding a new FAQ.", ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
      


class ClearAllEmbed(Embed):
    def __init__(self):
        super().__init__(title="❗ Are you sure you want to CLEAR all FAQs? ❗", description="", color=Color.orange())
        self.add_field(name="", value=" ", inline=False)
        self.add_field(name="", value="All questions and answers in the database will be deleted **forever**", inline=False)
        self.add_field(name="", value=" ", inline=False)
        self.set_footer(text="⚠️ This action cannot be undone")


class ClearAllButtons(ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()

    @discord.ui.button(label="Yes, clear all FAQs", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        self.db.query("DELETE FROM faqs_db")
        embed = Embed(title=" ", description="Success! All FAQs have been cleared from the database", color=Color.green())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"FAQs were **NOT** cleared because the action was cancelled.", color = discord.Color.red())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)






           
