import discord
from discord import ui,  Interaction, Embed, SelectOption, Color
from matty_db import Database


class FaqsMenu(ui.Select):
    def __init__(self, server_id, call):
        self.db = Database()
        self.call = call

        rows = self.db.query_fetch("SELECT question, faq_id FROM faqs_db WHERE server_id = ?", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no FAQ", value="none")] 

        if call == 'view':
            super().__init__(placeholder="Select a question to view the answer", options=options)
        elif call == 'delete': 
            super().__init__(placeholder="Select an FAQ to delete", options=options)

    async def callback(self, interaction: Interaction):
        if self.values[0] == "none":
            await interaction.response.defer()
            return
        selection = self.db.query_fetch("SELECT question, answer, creator, datecreated FROM faqs_db WHERE faq_id = ?", (self.values[0],))

        if selection:
            question = selection[0][0]
            answer = selection[0][1]
            creator = selection[0][2]
            datecreated = selection[0][3]
            if self.call == 'view':
                embed = Embed(title=question, description=answer, color=Color.orange())
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.set_footer(text=f"Created by {creator} on {datecreated}")
                await interaction.response.edit_message(embed=embed)
            elif self.call == 'delete': 
                self.db.query("DELETE FROM faqs_db WHERE faq_id = ?", self.values[0])
                embed = Embed(title="", description=f"FAQ `{question}` has been deleted!", color = discord.Color.green())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = Embed(title="", description=f"Oops! Something went wrong. Try again or contact support.", color = discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class FaqsView(ui.View):
     def __init__(self, server_id, call, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(FaqsMenu(server_id, call))




class EventsMenu(ui.Select):
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
        if self.values[0] == "none":
            await interaction.response.defer()
            return
        selection = self.db.query_fetch('''
            SELECT event_name, date, time, location, description, creator, datecreated FROM events_db WHERE event_id = ?
            ''', (self.values[0],))
        accepted_rows = self.db.query_fetch("SELECT COUNT(*) FROM responses_db WHERE event_id = ? AND response = ?" , (self.values[0], 'accepted',))
        declined_rows = self.db.query_fetch("SELECT COUNT(*) FROM responses_db WHERE event_id = ? AND response = ?" , (self.values[0], 'declined',))
        tentative_rows = self.db.query_fetch("SELECT COUNT(*) FROM responses_db WHERE event_id = ? AND response = ?" , (self.values[0], 'tentative',))
        
        
        if selection:
            event_name = selection[0][0]
            date = selection[0][1]
            time = selection[0][2]
            location = selection[0][3]
            description = selection [0][4]
            creator = selection [0][5]
            datecreated = selection[0][6]
            accepted_count = accepted_rows[0][0]
            declined_count = declined_rows[0][0]
            tentative_count = tentative_rows[0][0]
            if self.call == 'view':
                embed = Embed(title=f"📅  `{event_name}`", description=description, color = discord.Color.blue())
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name="⏰ When", value=f"{date} at {time}", inline = True)
                embed.add_field(name="📍 Where", value=location, inline = True)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name="Attending ✅ ", value=str(accepted_count), inline = True)
                embed.add_field(name="Can't Go ❌", value=str(declined_count), inline = True)
                embed.add_field(name="Maybe ❔", value=str(tentative_count), inline = True)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.set_footer(text=f"Created by {creator} on {datecreated}")
                await interaction.response.edit_message(embed=embed)
            elif self.call =='delete': 
                self.db.query("DELETE FROM events_db WHERE event_id = ?", self.values[0])
                self.db.query("DELETE FROM responses_db WHERE event_id = ?", self.values[0])
                embed = Embed(title="", description=f"Event `{event_name}` has been deleted!", color = discord.Color.green())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = Embed(title="", description=f"Oops! Something went wrong. Try again or contact support.", color = discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class EventsView(ui.View):
     def __init__(self, server_id, call, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(EventsMenu(server_id, call))