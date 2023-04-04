import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database
from cal_functions import GoogleCalendarEvents


class EventsDropdownMenu(ui.Select):
    def __init__(self, server_id, call):
        self.db = Database()
        self.call = call
        rows = self.db.query_fetch("SELECT event_name, event_id FROM events_db WHERE server_id = ?", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no events", value="none")]  

        if call == 'view':
            super().__init__(placeholder="Select an event to view the event details", options=options)
        else: 
            super().__init__(placeholder="Select an event to delete", options=options)
    
    async def callback(self, interaction: Interaction):
        event_id = self.values[0]
        if self.values[0] == "none":
            await interaction.response.defer()
            return
        
        selection = self.db.query_fetch("SELECT * FROM events_db WHERE event_id = ?", (event_id,))

        accepted_rows = self.db.query_fetch("SELECT COUNT(*) FROM responses_db WHERE event_id = ? AND response = ?" , (event_id, 'accepted',))
        declined_rows = self.db.query_fetch("SELECT COUNT(*) FROM responses_db WHERE event_id = ? AND response = ?" , (event_id, 'declined',))
        tentative_rows = self.db.query_fetch("SELECT COUNT(*) FROM responses_db WHERE event_id = ? AND response = ?" , (event_id, 'tentative',))

        
        if selection:
            event_name = selection[0][2]
            description = selection[0][3]
            location = selection[0][4]
            start_date = selection[0][5]
            start_time = selection[0][6]
            end_date = selection[0][7]
            end_time = selection[0][8]
            event_link = selection[0][9]
            creator = selection[0][10]
            datecreated = selection[0][11]

            accepted_count = accepted_rows[0][0]
            declined_count = declined_rows[0][0]
            tentative_count = tentative_rows[0][0]

            if self.call == 'view':
                embed = Embed(title=f"📅  `{event_name}`", description=description, color = discord.Color.blue())
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name="⏰ Starts: ", value=f"{start_date} at {start_time}", inline = True)
                embed.add_field(name="⏰ Ends:", value=f"{end_date} at {end_time}", inline = True)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name="📍 Location", value=location, inline = True)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name="Attending ✅ ", value=str(accepted_count), inline = True)
                embed.add_field(name="Can't Go ❌", value=str(declined_count), inline = True)
                embed.add_field(name="Maybe ❔", value=str(tentative_count), inline = True)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name="Link to Google Calendar:", value=f"{event_link}", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.set_footer(text=f"Created by {creator} on {datecreated}")
                await interaction.response.edit_message(embed=embed)

            elif self.call =='delete':
                embed2 = Embed(title="❗ Are you sure you want to DELETE this event? ❗", description="", color=Color.blue())
                embed2.add_field(name=" ", value=" ", inline=False)
                embed2.add_field(name=f"📅  `{event_name}`", value=description)
                embed2.add_field(name=" ", value=" ", inline=False)
                embed2.add_field(name=" ", value=" ", inline=False)
                embed2.add_field(name="⏰ Starts: ", value=f"{start_date} at {start_time}", inline = True)
                embed2.add_field(name="⏰ Ends:", value=f"{end_date} at {end_time}", inline = True)
                embed2.add_field(name=" ", value=" ", inline=False)
                embed2.add_field(name=" ", value=" ", inline=False)
                embed2.add_field(name="📍 Location", value=location, inline = True)
                embed2.add_field(name="", value=" ", inline=False)
                embed2.set_footer(text="⚠️ This action cannot be undone")
                view = DeleteEventButtons(event_id, event_name)
                await interaction.response.edit_message(embed=embed2, view=view) 
                
        else:
            embed = Embed(title="", description=f"Oops! Something went wrong. Try again or contact support.", color = discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class EventsView(ui.View):
     def __init__(self, server_id, call, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(EventsDropdownMenu(server_id, call))


class DeleteEventButtons(ui.View):
    def __init__(self, event_id, event_name, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.event_id = event_id
        self.event_name = event_name
        

    @discord.ui.button(label="Yes, delete forever", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        event_id = self.event_id
        event_name = self.event_name
        self.db.query("DELETE FROM events_db WHERE event_id = ?", event_id)
        self.db.query("DELETE FROM responses_db WHERE event_id = ?", event_id)
        await GoogleCalendarEvents.DeleteFromCalendar(event_id)

        embed = Embed(title="", description=f"`{event_name}` has been deleted!", color = discord.Color.green())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="No, keep it", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        event_name = self.event_name
        embed = Embed(title="", description=f"`{event_name}` was **not** deleted because the action was cancelled.", color = discord.Color.red())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self)