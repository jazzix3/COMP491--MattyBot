import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database


class DeletePollEmbed(Embed):
    def __init__(self, poll_title, description, start_date, start_time, end_date, end_time):
        super().__init__(title="❗ Are you sure you want to `DELETE` this poll? ❗", description="", color=Color.blue())
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=f"📅  `{poll_title}`", value=description)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="⏰ Starts: ", value=f"{start_date} at {start_time}", inline = True)
        self.add_field(name="⏰ Ends:", value=f"{end_date} at {end_time}", inline = True)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="⚠️ Warning: This action cannot be undone", value=" ", inline=False)



class DeletePollButtons(ui.View):
    def __init__(self, poll_id, poll_title, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.poll_id = poll_id
        self.poll_title = poll_title
        

    @discord.ui.button(label="Yes, delete forever", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        poll_id = self.poll_id
        poll_title = self.poll_title
        self.db.query("DELETE FROM polls_db WHERE poll_id = ?", poll_id)
        self.db.query("DELETE FROM votes_db WHERE poll_id = ?", poll_id)

        embed = Embed(title="", description=f"`{poll_title}` has been deleted!", color = discord.Color.green())
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="No, keep it", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        poll_title = self.poll_title
        embed = Embed(title="", description=f"`{poll_title}` was **not** deleted because the action was cancelled.", color = discord.Color.red())
        for child in self.children: 
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)