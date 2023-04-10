import discord
from discord import app_commands, ui,  Interaction, Embed, Color
from discord.ext import commands
from matty_db import Database
from components.archive_view import ArchiveView


class ArchiveCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = Database()
    
    #member = app_commands.Group(name="archive-", description="Archive")    
    admin = app_commands.Group(name="archive--", description="Archive")


    @app_commands.command(name="archive", description="View all archived events")
    async def archive(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=ArchiveView(server_id, call='view'), ephemeral=True)

    @admin.command(name="restore", description="Restore an event from the archive (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def restore(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=ArchiveView(server_id, call='restore'), ephemeral=True)

    @restore.error
    async def restore(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True)


class AdminErrorEmbed(Embed):
    def __init__(self):
        super().__init__()
        self.db = Database()

        super().__init__(title="", description=f"You must have the role `MattyBotAdmin` to use that command", color=Color.red())

    

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ArchiveCommands(client))