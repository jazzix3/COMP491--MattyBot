import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database



class EventInviteMenu(ui.Select):
    def __init__(self, server_id, call):
        self.db = Database()
        self.call = call
        rows = self.db.query_fetch("SELECT event_name, event_id FROM events_db WHERE server_id = ?", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no events", value="none")]

        if call == 'invite':
            super().__init__(placeholder="Select an event to send an invitation", options=options)
        elif call =='responses': 
            super().__init__(placeholder="Select an event to view its RSVP responses", options=options)        


    async def callback(self, interaction: Interaction):
        event_id = int(self.values[0])

        if self.values[0] == "none":
            await interaction.response.defer()
            return
        
        else:
            if self.call == 'invite':   
                embed = EventInviteEmbed(event_id=event_id)
                view = EventInviteButtons(event_id)
                await interaction.response.send_message(embed=embed, view=view)
            elif self.call == 'responses':
                embed = EventResponsesEmbed(event_id=event_id)
                await interaction.response.edit_message(embed=embed)



class EventInviteView(ui.View):
    def __init__(self, server_id, call, *, timeout = None):
         super().__init__(timeout=timeout)
         self.add_item(EventInviteMenu(server_id, call))         



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
            event_id = self.event_id
            new_embed = EventInviteEmbed(event_id=event_id)
            new_view = EventInviteButtons(event_id)
            await interaction.response.edit_message(embed=new_embed, view=new_view)
            response_embed = Embed(title="✅ You are attending!", description=f"See you there, {username}! Thank you for responding to this event.", color = Color.blue())
            await interaction.followup.send(embed=response_embed, ephemeral=True)
        else:
            await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True)


    @discord.ui.button(label="Can't Go", style=discord.ButtonStyle.red)
    async def declined(self, interaction: Interaction, button: ui.Button):
        username = interaction.user.name
        response = "declined"
        if await self.update_response(username, response):
            event_id = self.event_id
            new_embed = EventInviteEmbed(event_id=event_id)
            new_view = EventInviteButtons(event_id)
            await interaction.response.edit_message(embed=new_embed, view=new_view)
            response_embed = Embed(title="❌ Sorry you can't go!", description=f"Hope to see you next time, {username}! Thank you for responding to this event.", color = Color.blue())
            await interaction.followup.send(embed=response_embed, ephemeral=True)
        else:
            await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True)


    @discord.ui.button(label="Maybe", style=discord.ButtonStyle.grey)
    async def tentative(self, interaction: Interaction, button: ui.Button):
        username = interaction.user.name
        response = "tentative"
        if await self.update_response(username, response):
            event_id = self.event_id
            new_embed = EventInviteEmbed(event_id=event_id)
            new_view = EventInviteButtons(event_id)
            await interaction.response.edit_message(embed=new_embed, view=new_view)
            response_embed = Embed(title="❔ We marked you as 'maybe', and we hope you can make it!", description="Update your RSVP anytime using command **/event RSVP**. Thank you for responding to this event.", color = Color.blue())
            await interaction.followup.send(embed=response_embed, ephemeral=True)
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



class EventInviteEmbed(Embed):
    def __init__(self, event_id):
        super().__init__()
        self.db = Database()
        self.event_id = event_id
        

        selection = self.db.query_fetch("SELECT event_name, date, time, location, description, creator, datecreated FROM events_db WHERE event_id = ?", (self.event_id,))
        event_name = selection[0][0]
        date = selection[0][1]
        time = selection[0][2]
        location = selection[0][3]
        description = selection[0][4]
        creator = selection[0][5]
        datecreated = selection[0][6]

        accepted_rows = self.db.query_fetch("SELECT COUNT(*) FROM responses_db WHERE event_id = ? AND response = ?", (self.event_id, 'accepted',))
        declined_rows = self.db.query_fetch("SELECT COUNT(*) FROM responses_db WHERE event_id = ? AND response = ?", (self.event_id, 'declined',))
        tentative_rows = self.db.query_fetch("SELECT COUNT(*) FROM responses_db WHERE event_id = ? AND response = ?", (self.event_id, 'tentative',))
        accepted_count = accepted_rows[0][0]
        declined_count = declined_rows[0][0]
        tentative_count = tentative_rows[0][0]

        super().__init__(title=f"✉️  You are invited to the event: `{event_name}`", description=description, color=Color.blue())
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="⏰ When", value=f"{date} at {time}", inline=True)
        self.add_field(name="📍 Where", value=location, inline=True)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="Attending ✅ ", value=str(accepted_count), inline=True)
        self.add_field(name="Can't Go ❌", value=str(declined_count), inline=True)
        self.add_field(name="Maybe ❔", value=str(tentative_count), inline=True)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=f"`Please let us know if you can make it by selecting an option below!`", value=" ", inline=False)
        



class EventResponsesEmbed(Embed):
    def __init__(self, event_id):
        super().__init__()
        self.db = Database()
        self.event_id = event_id
        
        selection = self.db.query_fetch("SELECT event_name, date, time FROM events_db WHERE event_id = ?", (self.event_id,))
        event_name = selection[0][0]
        date = selection[0][1]
        time = selection[0][2]

        accepted_rows = self.db.query_fetch("SELECT username FROM responses_db WHERE event_id = ? AND response = ?", (self.event_id, 'accepted',))
        accepted_users = [row[0] for row in accepted_rows]
        accepted_string = "\n".join(accepted_users) if accepted_users else "[No one]"

        declined_rows = self.db.query_fetch("SELECT username FROM responses_db WHERE event_id = ? AND response = ?", (self.event_id, 'declined',))
        declined_users = [row[0] for row in declined_rows]
        declined_string = "\n".join(declined_users) if declined_users else "[No one]"

        tentative_rows = self.db.query_fetch("SELECT username FROM responses_db WHERE event_id = ? AND response = ?", (self.event_id, 'tentative',))
        tentative_users = [row[0] for row in tentative_rows]
        tentative_string = "\n".join(tentative_users) if tentative_users else "[No one]"

        super().__init__(title=f"RSVP responses for {event_name} on {date} at {time}", color=Color.blue())
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="Attending ✅ ", value=accepted_string, inline=True)
        self.add_field(name="Can't Go ❌", value=declined_string, inline=True)
        self.add_field(name="Maybe ❔", value=tentative_string, inline=True)
