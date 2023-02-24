import discord
from discord import app_commands, ui,  Interaction, Embed, SelectOption, Color
from discord.ext import commands
from matty_db import Database



class EventInvitation(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = Database()

    @app_commands.command(name="eventinvite", description="Send an invitation to an event")
    async def eventinvite(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=EventInviteView(server_id), ephemeral=True)



class EventInviteMenu(ui.Select):
    def __init__(self, server_id):
        self.db = Database()
        rows = self.db.query_fetch("SELECT event_name, event_id FROM events_db WHERE server_id = ?", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no events", value="none")]        
        super().__init__(placeholder="Select an event to view the event details", options=options)

    async def callback(self, interaction: Interaction):
        if self.values[0] == "none":
            await interaction.response.defer()
            return
        selection = self.db.query_fetch("SELECT event_name, date, time, location, description, creator, datecreated FROM events_db WHERE event_id = ?", (self.values[0],))
        
        if selection:
            event_id = self.values[0]
            event_name = selection[0][0]
            date = selection[0][1]
            time = selection[0][2]
            location = selection[0][3]
            description = selection [0][4]
            creator = selection [0][5]
            datecreated = selection[0][6]

            embed = Embed(title=event_name, description=description, color = Color.blue())
            embed.add_field(name="When", value=f"{date} at {time}", inline = True)
            embed.add_field(name="Where", value=location, inline = False)
            embed.add_field(name=" ", value=" ", inline=False)
            embed.add_field(name="Attending ✅ ", value=" ", inline = True)
            embed.add_field(name="Can't Go ❌", value=" ", inline = True)
            embed.add_field(name="Maybe ❔", value=" ", inline = True)
            embed.add_field(name=" ", value=" ", inline=False)
            embed.add_field(name=" ", value=" ", inline=False)
            embed.set_footer(text=f"Created by {creator} on {datecreated}")
            view = EventInviteButtons(event_id)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True)



class EventInviteView(ui.View):
     def __init__(self, server_id, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(EventInviteMenu(server_id))

class EventInviteButtons(ui.View):
    def __init__(self, event_id, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id
        

    @discord.ui.button(label="Attending", style=discord.ButtonStyle.green)
    async def accepted(self, interaction: Interaction, button: ui.Button):
        username = interaction.user.name
        response = "accepted"
        if await self.update_response(username, response):
            await interaction.response.send_message(content="You are going!", ephemeral=True)
        else:
            await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True)


    @discord.ui.button(label="Can't Go", style=discord.ButtonStyle.red)
    async def declined(self, interaction: Interaction, button: ui.Button):
        username = interaction.user.name
        response = "declined"
        if await self.update_response(username, response):
            await interaction.response.send_message(content="You are not going.", ephemeral=True)
        else:
            await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True)

    @discord.ui.button(label="Maybe", style=discord.ButtonStyle.grey)
    async def tentative(self, interaction: Interaction, button: ui.Button):
        username = interaction.user.name
        response = "tentative"
        if await self.update_response(username, response):
            await interaction.response.send_message(content="You might go.", ephemeral=True)
        else:
            await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True)


    async def update_response(self, username, response):
        # Check if the event_id exists in the events_db table (to make sure foreign keys match)
        event_check = self.db.query_fetch("SELECT event_id FROM events_db WHERE event_id = ?", (self.event_id,))
        if not event_check:
            return False
        
        # Check if the user has already responded for this event
        response_check = self.db.query_fetch("SELECT response_id FROM responses_db WHERE event_id = ? AND username = ?", (self.event_id, username))
        if response_check:
            # User has already responded, update the response
            sql = "UPDATE responses_db SET response = ? WHERE event_id = ? AND username = ?"
            val = (response, self.event_id, username)
            self.db.query_input(sql, val)
        else:
            # User has not responded yet, insert the response
            sql = "INSERT INTO responses_db (event_id, username, response) VALUES (?, ?, ?)"
            val = (self.event_id, username, response)
            self.db.query_input(sql, val)
        return True




async def setup(client: commands.Bot) -> None:
    await client.add_cog(EventInvitation(client))