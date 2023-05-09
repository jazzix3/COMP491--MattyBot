import discord
from discord import app_commands, ui,  Interaction, Embed, Color
from discord.ext import commands
from matty_db import Database
from components.polls_view import PollsView
from components.polls_add import Modal1
from components.polls_clearall import ClearAllButtons, ClearAllEmbed
from components.polls_vote_or_viewresponses import PollVoteView


class PollsCommands(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.db = Database()
        

    member = app_commands.Group(name="polls-", description="Polls") 
    admin = app_commands.Group(name="polls--", description="Polls")

    @app_commands.command(name="polls", description="View all polls")
    async def polls(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=PollsView(server_id, call='view'), ephemeral=True)


    @member.command(name="list", description="View a list of all polls")
    async def list(self, interaction: Interaction) -> None:
        server_id = interaction.guild_id
        rows = self.db.query_fetch("SELECT poll_title FROM polls_db WHERE server_id = ?", (server_id,))
        if rows:
            embed = Embed(title="List of all polls", description="For more information about a poll, type command **/polls**", color = Color.orange())
            count = 1
            for row in rows:
                poll_title = row[0]
                embed.add_field(name=f"{count} - {poll_title}", value="\n", inline= False)
                count += 1
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed2 = Embed(title="List of all polls", description ="There are currently no polls", color=Color.orange())
            await interaction.response.send_message(embed=embed2, ephemeral=True)

    @member.command(name="vote", description="Vote in a poll")
    async def viewvotes(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=PollVoteView(server_id, call='memberrsvp'), ephemeral=True)
    @viewvotes.error
    async def viewvoteserror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 


    @admin.command(name="add", description="Add a new poll (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def add(self, interaction: Interaction) -> None:
        await interaction.response.send_modal(Modal1()) 
    @add.error
    async def add(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 

    @admin.command(name="clearall", description="Clear all polls from the database (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def clearall(self, interaction: Interaction) -> None:
        await interaction.response.send_message(embed=ClearAllEmbed(), view=ClearAllButtons(), ephemeral=True)
    @clearall.error
    async def clearallerror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 

    @admin.command(name="viewvotes", description="View all votes for a poll (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def viewvotes(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=PollVoteView(server_id, call='votes'), ephemeral=True)
    @viewvotes.error
    async def viewvoteserror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True)

    @admin.command(name="delete", description = "Delete a poll from the database (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def delete(self, interaction: discord.Interaction) -> None:
        server_id = interaction.guild_id
        await interaction.response.send_message(view=PollsView(server_id, call='delete'), ephemeral=True)
    @delete.error
    async def deleteerror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 



class AdminErrorEmbed(Embed):
    def __init__(self):
        super().__init__(title="", description=f"You must have the role `MattyBotAdmin` to use that command", color=Color.red())
        

async def setup(client: commands.Bot) -> None:
    await client.add_cog(PollsCommands(client))