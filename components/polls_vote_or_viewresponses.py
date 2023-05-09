import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database



class PollVoteDropdownMenu(ui.Select):
    def __init__(self, server_id, call):
        self.db = Database()
        self.call = call
        rows = self.db.query_fetch("SELECT poll_title, poll_id FROM polls_db WHERE server_id = ? ORDER BY start_date ASC", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no polls", value="none")]

        if call =='membervote': 
            super().__init__(placeholder="Select a poll to vote in", options=options)
        elif call =='votes': 
            super().__init__(placeholder="Select a poll to view its votes", options=options)


    async def callback(self, interaction: Interaction):
        poll_id = self.values[0]
        call = self.call

        if poll_id == "none":
            await interaction.response.defer()
            return
        
        else:
            if call == 'membervote': 
                embed = PollVoteEmbed(poll_id)
                view = PollVoteButtons(poll_id, call)
                await interaction.response.edit_message(embed=embed, view=view)
            elif call == 'votes':
                embed = PollVoteEmbed(poll_id)
                await interaction.response.edit_message(embed=embed)



class PollVoteView(ui.View):
    def __init__(self, server_id, call, *, timeout = None):
         super().__init__(timeout=timeout)
         self.add_item(PollVoteDropdownMenu(server_id, call))         



class PollVoteButtons(ui.View):
    def __init__(self, poll_id, call, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.poll_id = poll_id
        self.call = call
        

    @discord.ui.button(label="Vote 1", style=discord.ButtonStyle.green)
    async def accepted(self, interaction: Interaction, button: ui.Button):
        username = interaction.user.name
        vote = "Vote 1"
        if await self.update_vote(username, vote):
            poll_id = self.poll_id
            call = self.call

            if call == 'memberrsvp':
                embed2 = Embed(title="Thank you for your vote!", description=f"We appreciate your input, {username}! Thank you for responding to this event.", color = Color.blue())
                embed2.add_field(name=" ", value=" ", inline=False)
                for child in self.children: 
                    child.disabled = True
                await interaction.response.edit_message(embed=embed2, view=self)               
        else:
            embed = Embed(title="", description=f"Oops! Something went wrong. Try again or contact support.", color = discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @discord.ui.button(label="Vote 2", style=discord.ButtonStyle.red)
    async def declined(self, interaction: Interaction, button: ui.Button):
        username = interaction.user.name
        vote = "Vote 2"
        if await self.update_vote(username, vote):
            poll_id = self.poll_id
            call = self.call

            if call == 'memberrsvp':
                response_embed = Embed(title="Thank you for your vote!", description=f"Thank you for responding to this event.", color = Color.blue())
                for child in self.children: 
                    child.disabled = True
                await interaction.response.edit_message(embed=response_embed, view=self)               
        


    @discord.ui.button(label="Vote 3", style=discord.ButtonStyle.grey)
    async def tentative(self, interaction: Interaction, button: ui.Button):
        username = interaction.user.name
        vote = "Vote 3"
        if await self.update_vote(username, vote):
            poll_id = self.poll_id
            call = self.call
           
            if call == 'memberrsvp':
                response_embed = Embed(title="Thank you for your vote!", description=f"Hope to see you next time, {username}! Thank you for responding to this event.", color = Color.blue())
                for child in self.children: 
                    child.disabled = True
                await interaction.response.edit_message(embed=response_embed, view=self)


    @discord.ui.button(label="Vote 4", style=discord.ButtonStyle.grey)
    async def tentative(self, interaction: Interaction, button: ui.Button):
        username = interaction.user.name
        vote = "Vote 4"
        if await self.update_vote(username, vote):
            poll_id = self.poll_id
            call = self.call

            if call == 'memberrsvp':
                response_embed = Embed(title="Thank you for your vote!", description=f"Hope to see you next time, {username}! Thank you for responding to this event.", color = Color.blue())
        

    async def update_vote(self, username, vote):
        poll_check = self.db.query_fetch("SELECT poll_id FROM polls_db WHERE poll_id = ?", (self.poll_id,))
        if not poll_check:
            return False
        
        vote_check = self.db.query_fetch("SELECT vote_id FROM votes_db WHERE vote_id = ? AND username = ?", (self.poll_id, username))
        if vote_check:
            sql = "UPDATE votes_db SET vote = ? WHERE poll_id = ? AND username = ?"
            val = (vote, self.poll_id, username)
            self.db.query_input(sql, val)
        else:
            sql = "INSERT INTO votes_db (poll_id, username, vote) VALUES (?, ?, ?)"
            val = (self.poll_id, username, vote)
            self.db.query_input(sql, val)
        return True



class PollVoteEmbed(Embed):
    def __init__(self, poll_id):
        super().__init__()
        self.db = Database()
        self.poll_id = poll_id
        

        selection = self.db.query_fetch("SELECT poll_title, description, start_date, start_time, end_date, end_time FROM polls_db WHERE poll_id = ?", (self.poll_id,))
        poll_title = selection[0][0]
        description = selection[0][1]
        start_date = selection[0][3]
        start_time = selection[0][4]
        end_date = selection[0][5]
        end_time = selection[0][6]

        choice_one = self.db.query_fetch("SELECT COUNT(*) FROM votes_db WHERE poll_id = ? AND vote = ?" , (poll_id, '1',))
        choice_two = self.db.query_fetch("SELECT COUNT(*) FROM votes_db WHERE poll_id = ? AND vote = ?" , (poll_id, '2',))
        choice_three = self.db.query_fetch("SELECT COUNT(*) FROM votes_db WHERE poll_id = ? AND vote = ?" , (poll_id, '3',))
        choice_four = self.db.query_fetch("SELECT COUNT(*) FROM votes_db WHERE poll_id = ? AND vote = ?" , (poll_id, '4',))

        one_count = choice_one[0][0]
        two_count = choice_two[0][0]
        three_count = choice_three[0][0]
        four_count = choice_four[0][0]

        super().__init__(title=f"✉️  You are invited to vote in a poll: `{poll_title}`", description=description, color=Color.blue())
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="⏰ Starts: ", value=f"{start_date} at {start_time}", inline = True)
        self.add_field(name="⏰ Ends:", value=f"{end_date} at {end_time}", inline = True)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="Vote 1", value=str(one_count), inline = True)
        self.add_field(name="Vote 2", value=str(two_count), inline = True)
        self.add_field(name="Vote 3", value=str(three_count), inline = True)
        self.add_field(name="Vote 4", value=str(four_count), inline = True)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=f"`Please vote by selecting an option below!`", value=" ", inline=False)
        



class VoteResponsesEmbed(Embed):
    def __init__(self, poll_id):
        super().__init__()
        self.db = Database()
        self.poll_id = poll_id
        
        selection = self.db.query_fetch("SELECT poll_title, start_date, start_time, end_date, end_time FROM polls_db WHERE poll_id = ?", (self.poll_id,))
        poll_title = selection[0][0]
        start_date = selection[0][1]
        start_time = selection[0][2]
        end_date = selection[0][3]
        end_time = selection[0][4]

        one_count = self.db.query_fetch("SELECT username FROM votes_db WHERE poll_id = ? AND vote = ?", (self.poll_id, 'Vote 1',))
        one_users = [row[0] for row in one_count]
        one_string = "\n".join(one_users) if one_users else "[No one]"

        two_count = self.db.query_fetch("SELECT username FROM votes_db WHERE poll_id = ? AND vote = ?", (self.poll_id, 'Vote 2',))
        two_users = [row[0] for row in two_count]
        two_string = "\n".join(two_users) if two_users else "[No one]"

        three_count = self.db.query_fetch("SELECT username FROM votes_db WHERE poll_id = ? AND vote = ?", (self.poll_id, 'Vote 3',))
        three_users = [row[0] for row in three_count]
        three_string = "\n".join(three_users) if three_users else "[No one]"

        four_count = self.db.query_fetch("SELECT username FROM votes_db WHERE poll_id = ? AND vote = ?", (self.poll_id, 'Vote 4',))
        four_users = [row[0] for row in four_count]
        four_string = "\n".join(four_users) if four_users else "[No one]"

        super().__init__(title=f"📬  Vote responses for `{poll_title}`", color=Color.blue())
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="⏰ Starts: ", value=f"{start_date} at {start_time}", inline = True)
        self.add_field(name="⏰ Ends:", value=f"{end_date} at {end_time}", inline = True)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name=" ", value=" ", inline=False)
        self.add_field(name="Vote 1", value=str(one_count), inline = True)
        self.add_field(name="Vote 2", value=str(two_count), inline = True)
        self.add_field(name="Vote 3", value=str(three_count), inline = True)
        self.add_field(name="Vote 4", value=str(four_count), inline = True)