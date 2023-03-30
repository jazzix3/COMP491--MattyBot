import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database


class FaqsDropdownMenu(ui.Select):
    def __init__(self, server_id, call):
        self.db = Database()
        self.call = call

        rows = self.db.query_fetch("SELECT question, faq_id FROM faqs_db WHERE server_id = ?", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no FAQ", value="none")] 

        if call == 'view':
            super().__init__(placeholder="Select a question to view the answer", options=options)
        elif call == 'delete': 
            super().__init__(placeholder="Select a FAQ to delete", options=options)

    async def callback(self, interaction: Interaction):
        faq_id = self.values[0]
        if faq_id == "none":
            await interaction.response.defer()
            return
        
        selection = self.db.query_fetch("SELECT question, answer, creator, datecreated FROM faqs_db WHERE faq_id = ?", (faq_id,))

        if selection:
            question = selection[0][0]
            answer = selection[0][1]
            creator = selection[0][2]
            datecreated = selection[0][3]
            if self.call == 'view':
                embed = Embed(title=f"`{question}`", description=answer, color=Color.orange())
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.set_footer(text=f"Created by {creator} on {datecreated}")
                await interaction.response.edit_message(embed=embed)
            elif self.call == 'delete':
                embed2 = Embed(title="❗ Are you sure you want to DELETE this FAQ? ❗", description="", color=Color.orange())
                embed2.add_field(name=" ", value=" ", inline=False)
                embed2.add_field(name=" ", value=" ", inline=False)
                embed2.add_field(name=f"`{question}`", value=answer, inline=False)
                embed2.add_field(name="", value=" ", inline=False)
                embed2.add_field(name="", value=" ", inline=False)
                embed2.set_footer(text="⚠️ This action cannot be undone")
                view = DeleteFaqsButtons(faq_id, question)
                await interaction.response.edit_message(embed=embed2, view=view)
        else:
            embed = Embed(title="", description=f"Oops! Something went wrong. Try again or contact support.", color = discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class FaqsView(ui.View):
     def __init__(self, server_id, call, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(FaqsDropdownMenu(server_id, call))


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




