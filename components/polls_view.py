import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database
from components.polls_delete import DeletePollEmbed, DeletePollButtons


class PollsDropdownMenu(ui.Select):
    def __init__(self, server_id, call):
        self.db = Database()
        self.call = call
        rows = self.db.query_fetch("SELECT poll_title, poll_id FROM polls_db WHERE server_id = ? ORDER BY start_date ASC", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no polls", value="none")]  

        if call == 'view':
            super().__init__(placeholder="Select a poll to view the poll details", options=options)
        elif call == 'delete': 
            super().__init__(placeholder="Select a poll to delete", options=options)
    
    async def callback(self, interaction: Interaction):
        poll_id = self.values[0]
        if self.values[0] == "none":
            await interaction.response.defer()
            return
        
        selection = self.db.query_fetch("SELECT * FROM polls_db WHERE poll_id = ?", (poll_id,))

        choice_one = self.db.query_fetch("SELECT COUNT(*) FROM votes_db WHERE poll_id = ? AND vote = ?" , (poll_id, '1',))
        choice_two = self.db.query_fetch("SELECT COUNT(*) FROM votes_db WHERE poll_id = ? AND vote = ?" , (poll_id, '2',))
        choice_three = self.db.query_fetch("SELECT COUNT(*) FROM votes_db WHERE poll_id = ? AND vote = ?" , (poll_id, '3',))
        choice_four = self.db.query_fetch("SELECT COUNT(*) FROM votes_db WHERE poll_id = ? AND vote = ?" , (poll_id, '4',))

        
        if selection:
            poll_title = selection[0][1]
            description = selection[0][2]
            start_date = selection[0][3]
            start_time = selection[0][4]
            end_date = selection[0][5]
            end_time = selection[0][6]
            creator = selection[0][7]
            datecreated = selection[0][8]

            one_count = choice_one[0][0]
            two_count = choice_two[0][0]
            three_count = choice_three[0][0]
            four_count = choice_four[0][0]

            if self.call == 'view':
                embed = Embed(title=f"📅  `{poll_title}`", description=description, color = discord.Color.blue())
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name="⏰ Starts: ", value=f"{start_date} at {start_time}", inline = True)
                embed.add_field(name="⏰ Ends:", value=f"{end_date} at {end_time}", inline = True)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name="Vote 1", value=str(one_count), inline = True)
                embed.add_field(name="Vote 2", value=str(two_count), inline = True)
                embed.add_field(name="Vote 3", value=str(three_count), inline = True)
                embed.add_field(name="Vote 4", value=str(four_count), inline = True)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.set_footer(text=f"Created by {creator} on {datecreated}")
                await interaction.response.edit_message(embed=embed)

            elif self.call =='delete':
                embed = DeletePollEmbed(poll_title, description, start_date, start_time, end_date, end_time)
                view = DeletePollButtons(poll_id, poll_title)
                await interaction.response.edit_message(embed=embed, view=view)
                
        else:
            embed = Embed(title="", description=f"Oops! Something went wrong. Try again or contact support.", color = discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class PollsView(ui.View):
     def __init__(self, server_id, call, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(PollsDropdownMenu(server_id, call))


