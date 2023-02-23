import discord
from discord import app_commands, ui,  Interaction, Embed, SelectOption, Color
from discord.ext import commands
from matty_db import Database



class EventInvitation(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = Database()

    @app_commands.command(name="eventinvite", description="View all events")
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
        selection = self.db.query_fetch('''
            SELECT event_name, date, time, location, description, creator, datecreated FROM events_db WHERE event_id = ?
            ''', (self.values[0],))
        
        if selection:
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
            view = EventInviteButtons()
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True)



class EventInviteView(ui.View):
     def __init__(self, server_id, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(EventInviteMenu(server_id))

class EventInviteButtons(ui.View):
    def __init__(self, *, timeout=None, db=None):
        super().__init__(timeout=timeout)
        self.db = db

    @discord.ui.button(label="Attending", style=discord.ButtonStyle.green)
    async def accepted(self, interaction: Interaction, button: ui.Button):
        pass

    @discord.ui.button(label="Can't Go", style=discord.ButtonStyle.red)
    async def declined(self, interaction: Interaction, button: ui.Button):
        pass

    @discord.ui.button(label="Maybe", style=discord.ButtonStyle.grey)
    async def tentative(self, interaction: Interaction, button: ui.Button):
        pass



async def setup(client: commands.Bot) -> None:
    await client.add_cog(EventInvitation(client))