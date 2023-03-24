import discord
from discord import app_commands, ui,  Interaction, Embed, SelectOption, Color
from discord.ext import commands
from matty_db import Database
from modals import AddEventModal
from views import EventsView
from eventinvite import EventInviteView



class EventCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = Database()
    
    member = app_commands.Group(name="events-", description="Events")    
    admin = app_commands.Group(name="events--", description="Events")


    @app_commands.command(name="events", description="View all events and event informmation")
    async def events(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=EventsView(server_id, call='view'), ephemeral=True)


    @member.command(name="list", description="View a list of all events")
    async def list(self, interaction: Interaction):
        server_id = interaction.guild_id
        rows = self.db.query_fetch("SELECT event_name, date, time FROM events_db WHERE server_id = ? ORDER BY date", (server_id,))
        if rows:
            embed = Embed(title="List of all events", description="For more information about an event, type command **/events**", color = Color.blue())
            for row in rows:
                event_name = row[0]
                date = row[1]
                time = row[2]
                embed.add_field(name=f"`{event_name}`", value=f"{date} at {time}", inline= False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed2 = Embed(title="List of all events", description ="There are currently no events", color=Color.blue())
            await interaction.response.send_message(embed=embed2, ephemeral=True)


    @admin.command(name="add", description="Add a new event (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def add(self, interaction: Interaction):
        await interaction.response.send_modal(AddEventModal())
    @add.error
    async def adderror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True)


    @admin.command(name="clearall", description="Clear all events from the database (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def clearall(self, interaction: Interaction):
        self.db.query("DELETE FROM events_db")
        embed = Embed(title="Clear all events", description="Success! All events have been cleared from the database", color=Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    @clearall.error
    async def clearallerror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True)


    @admin.command(name="delete", description = "Delete an event from the database (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def delete(self, interaction: discord.Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=EventsView(server_id, call='delete'), ephemeral=True)
    @delete.error
    async def deleteerror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True)


    @admin.command(name="invite", description="Send an invitation for an event (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def eventinvite(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=EventInviteView(server_id, call='invite'), ephemeral=True)
    @eventinvite.error
    async def eventerror(self, interaction:Interaction, error):
       await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 


    @admin.command(name="viewresponses", description="View all RSVP responses for an event (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def viewresponses(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=EventInviteView(server_id, call='responses'), ephemeral=True)
    @viewresponses.error
    async def viewresponseserror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 


class AdminErrorEmbed(Embed):
    def __init__(self):
        super().__init__()
        self.db = Database()

        super().__init__(title="", description=f"You must have the role `MattyBotAdmin` to use that command", color=Color.red())

    

async def setup(client: commands.Bot) -> None:
    await client.add_cog(EventCommands(client))