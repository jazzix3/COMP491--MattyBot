import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database


class DeleteFaqsEmbed(Embed):
    def __init__(self, question, answer):
        super().__init__(title="❗ Are you sure you want to DELETE this FAQ? ❗", description="", color=Color.orange())
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=f"`{question}`", value=f'{answer}', inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="⚠️ Warning: This action cannot be undone", value=" ", inline=False)


class DeleteFaqsButtons(ui.View):
    def __init__(self, faq_id, question, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.faq_id = faq_id
        self.question = question
        

    @discord.ui.button(label="Yes, delete forever", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        faq_id = self.faq_id
        question = self.question
        self.db.query("DELETE FROM faqs_db WHERE faq_id = ?", faq_id)
        embed = Embed(title="", description=f"Success! `{question}` has been deleted!", color = discord.Color.green())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="No, keep it", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        question = self.question
        embed = Embed(title="", description=f"`{question}` was **not** deleted because the action was cancelled.", color = discord.Color.red())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)