import discord
from discord import app_commands, ui,  Interaction, Embed, Color
from discord.ext import commands
from matty_db import Database
from components.events_add import Modal1
from components.events_clearall import ClearAllEmbed, ClearAllButtons
from components.events_modify import EventModifyView
from components.events_invite_rsvp_or_viewresponses import EventInviteView
from components.events_view import EventsView
import cal_functions




class EventCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = Database()
    
    member = app_commands.Group(name="events-", description="Events")    
    admin = app_commands.Group(name="events--", description="Events")


    @app_commands.command(name="events", description="View all events and event information")
    async def events(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=EventsView(server_id, call='view'), ephemeral=True)

    
    @member.command(name="calendar", description="View the calendar of events")
    async def calendar(self, interaction: Interaction):
        calendar_link = await cal_functions.GoogleCalendarEvents.LinkCalendar()
        embed = discord.Embed(title="📅  To view the calendar of events, follow this link:", description=f"{calendar_link}", color=Color.blue())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    @calendar.error
    async def calendar(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 


    @member.command(name="list", description="View a list of all events")
    async def list(self, interaction: Interaction):
        server_id = interaction.guild_id
        rows = self.db.query_fetch("SELECT event_name, start_date, start_time FROM events_db WHERE server_id = ? ORDER BY start_date", (server_id,))
        if rows:
            embed = Embed(title="List of all events", description="For more information about an event, type command **/events**", color = Color.blue())
            for row in rows:
                event_name = row[0]
                start_date = row[1]
                start_time = row[2]
                embed.add_field(name=f"`{event_name}`", value=f"{start_date} at {start_time}", inline= False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed2 = Embed(title="List of all events", description ="There are currently no events", color=Color.blue())
            await interaction.response.send_message(embed=embed2, ephemeral=True)


    @member.command(name="rsvp", description="RSVP for an event")
    async def viewresponses(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=EventInviteView(server_id, call='memberrsvp'), ephemeral=True)
    @viewresponses.error
    async def viewresponseserror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True) 


    @admin.command(name="add", description="Add a new event (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def add(self, interaction: Interaction):
        await interaction.response.send_modal(Modal1())
    @add.error
    async def adderror(self, interaction:Interaction, error):
        await interaction.response.send_message(embed=AdminErrorEmbed(), ephemeral=True)


    @admin.command(name="clearall", description="Clear all events from the database (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def clearall(self, interaction: Interaction) -> None:
        await interaction.response.send_message(embed=ClearAllEmbed(), view=ClearAllButtons(), ephemeral=True)
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


    @admin.command(name="modify", description = "Modify an event (Admins only)")
    @app_commands.checks.has_role("MattyBotAdmin")
    async def modify(self, interaction: discord.Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=EventModifyView(server_id), ephemeral=True)
    @modify.error
    async def modifyerror(self, interaction:Interaction, error):
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