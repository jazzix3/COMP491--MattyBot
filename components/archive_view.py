import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database
from components.archive_restore import RestoreEventEmbed, RestoreEventButtons


class ArchiveDropdownMenu(ui.Select):
    def __init__(self, server_id, call):
        self.db = Database()
        self.call = call
        rows = self.db.query_fetch("SELECT event_name, event_id FROM archive_db WHERE server_id = ? ORDER BY start_date ASC", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no events", value="none")]  

        if call == 'view':
            super().__init__(placeholder="Select an event to view the event details", options=options)
        elif call == 'restore': 
            super().__init__(placeholder="Select an event to restore from the archive", options=options)

    
    async def callback(self, interaction: Interaction):
        event_id = self.values[0]
        if self.values[0] == "none":
            await interaction.response.defer()
            return
        
        selection = self.db.query_fetch("SELECT * FROM archive_db WHERE event_id = ?", (event_id,))

        
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


            if self.call == 'view':
                embed = Embed(title=f"📁  `{event_name}` (Archived)", description=description, color = discord.Color.dark_blue())
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
                embed.add_field(name="Link to Google Calendar:", value=f"{event_link}", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.set_footer(text=f"Created by {creator} on {datecreated}")
                await interaction.response.edit_message(embed=embed)

            elif self.call =='restore':
                embed = RestoreEventEmbed(event_name, description, location, start_date, start_time, end_date, end_time)
                view = RestoreEventButtons(event_id, event_name)
                await interaction.response.edit_message(embed=embed, view=view)

                
        else:
            embed = Embed(title="", description=f"Oops! Something went wrong. Try again or contact support.", color = discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class ArchiveView(ui.View):
     def __init__(self, server_id, call, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(ArchiveDropdownMenu(server_id, call))


