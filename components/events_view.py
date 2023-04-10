import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database
from components.events_delete import DeleteEventEmbed, DeleteEventButtons
from components.events_archive import ArchiveEventEmbed, ArchiveEventButtons


class EventsDropdownMenu(ui.Select):
    def __init__(self, server_id, call):
        self.db = Database()
        self.call = call
        rows = self.db.query_fetch("SELECT event_name, event_id FROM events_db WHERE server_id = ? ORDER BY start_date ASC", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no events", value="none")]  

        if call == 'view':
            super().__init__(placeholder="Select an event to view the event details", options=options)
        elif call == 'delete': 
            super().__init__(placeholder="Select an event to delete", options=options)
        elif call == 'archive': 
            super().__init__(placeholder="Select an event to move to the archive", options=options)
    
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
                embed = DeleteEventEmbed(event_name, description, location, start_date, start_time, end_date, end_time)
                view = DeleteEventButtons(event_id, event_name)
                await interaction.response.edit_message(embed=embed, view=view)

            elif self.call =='archive':
                embed = ArchiveEventEmbed(event_name, description, location, start_date, start_time, end_date, end_time)
                view = ArchiveEventButtons(event_id, event_name)
                await interaction.response.edit_message(embed=embed, view=view)
                
        else:
            embed = Embed(title="", description=f"Oops! Something went wrong. Try again or contact support.", color = discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class EventsView(ui.View):
     def __init__(self, server_id, call, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(EventsDropdownMenu(server_id, call))


