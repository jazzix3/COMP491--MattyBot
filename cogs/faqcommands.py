import discord
from discord import app_commands, ui,  Interaction, Embed, SelectOption, Color
from discord.ext import commands
from matty_db import Database
from modals import AddFaqModal
from views import FaqsView



class FAQCommands(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.db = Database()

    member = app_commands.Group(name="faqs-", description="Frequently Asked Questions") 
    admin = app_commands.Group(name="faqs--", description="Frequently Asked Questions")

    @app_commands.command(name="faqs", description="View all frequently asked questions and answers")
    async def faqs(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=FaqsView(server_id, call='view'), ephemeral=True)


    @member.command(name="list", description="View a list of all FAQs")
    async def list(self, interaction: Interaction) -> None:
        server_id = interaction.guild_id
        rows = self.db.query_fetch("SELECT question FROM faqs_db WHERE server_id = ?", (server_id,))
        if rows:
            embed = Embed(title="List of all FAQ", description="To see all FAQs with answers, type command **/faqs**", color = Color.orange())
            count = 1
            for row in rows:
                question = row[0]
                embed.add_field(name=f"{count} - {question}", value="\n", inline= False)
                count += 1
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed2 = Embed(title="List of all FAQ", description ="There are currently no FAQ", color=Color.orange())
            await interaction.response.send_message(embed=embed2, ephemeral=True)


    @admin.command(name="add", description="Add a question & answer to FAQs (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def add(self, interaction: Interaction) -> None:
        await interaction.response.send_modal(AddFaqModal()) 
    @add.error
    async def add(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 


    @admin.command(name="clearall", description="Clear all FAQs from the database (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def clearall(self, interaction: Interaction) -> None:
        self.db.query("DELETE FROM faqs_db")
        embed = Embed(title="Clear all FAQs", description="Success! All FAQs have been cleared from the database", color=Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    @clearall.error
    async def clearallerror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 


    @admin.command(name="delete", description = "Delete a FAQ from the database (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def delete(self, interaction: discord.Interaction) -> None:
        server_id = interaction.guild_id
        await interaction.response.send_message(view=FaqsView(server_id, call='delete'), ephemeral=True)
    @delete.error
    async def deleteerror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 



class AdminErrorEmbed(Embed):
    def __init__(self):
        super().__init__()
        self.db = Database()

        super().__init__(title="", description=f"You must have the role `MattyBotAdmin` to use that command", color=Color.red())
        

async def setup(client: commands.Bot) -> None:
    await client.add_cog(FAQCommands(client))