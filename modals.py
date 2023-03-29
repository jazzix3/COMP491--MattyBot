from discord import ui, TextStyle, Interaction, Embed, Color
from matty_db import Database 
from datetime import datetime
from cal_functions import GoogleCalendarEvents



class AddFaqModal(ui.Modal, title="Add to FAQ"):
    db = Database()
    question = ui.TextInput(label="Question", style=TextStyle.short, required=True)
    answer = ui.TextInput(label="Answer:", style=TextStyle.long, required=True)

    async def on_submit(self, interaction: Interaction):
        server_id = interaction.guild_id
        creator = interaction.user.name
        timestamp = datetime.now()
        datecreated = timestamp.strftime(f"%m/%d/%Y")
        
        embed = Embed(title="Success! A new FAQ has been added.", description="To see all FAQs, type command **/viewFAQ**", color = Color.green())
        embed.add_field(name="Question", value=self.question, inline=False)
        embed.add_field(name="Answer", value=self.answer, inline=False)
        embed.add_field(name=" ", value=" ", inline=False)
        embed.add_field(name=" ", value=" ", inline=False)
        embed.set_footer(text=f"Created by {creator} on {datecreated}")

        try:
            sql = "INSERT INTO faqs_db(server_id, question, answer, creator, datecreated) VALUES (?, ?, ?, ?, ?)"
            val = (server_id, self.question.value, self.answer.value, creator, datecreated)
            self.db.query_input(sql,val)
        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while adding a new FAQ.", ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
      




class AddEventModal(ui.Modal, title="Add an Event"):
    db = Database()
    event_name = ui.TextInput(label="Name of event:", style=TextStyle.short, required=True)
    date = ui.TextInput(label="Start date:", style=TextStyle.short, required=True)
    time = ui.TextInput(label="Start time:", style=TextStyle.short, required=True)
    location = ui.TextInput(label="Location:", style=TextStyle.short, required=True)
    description = ui.TextInput(label="Description:", style=TextStyle.long, required=True)

    async def on_submit(self, interaction: Interaction):
        server_id = interaction.guild_id
        creator = interaction.user.name
        timestamp = datetime.now()
        datecreated = timestamp.strftime(f"%m/%d/%Y")
    
        

        try:
            sql = "INSERT INTO events_db(server_id, event_name, date, time, location, description, creator, datecreated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            val = (server_id, self.event_name.value, self.date.value, self.time.value, self.location.value, self.description.value, creator, datecreated)
            self.db.query_input(sql, val)

            event_name = self.event_name.value
            location = self.location.value
            description = self.description.value
            GoogleCalendarEvents.AddToCalendar(event_name, location, description)

            embed = Embed(title="Success! A new event has been added.", description="To send an invitation for this event, type command **/eventinvite**",color = Color.green())
            embed.add_field(name="Name of Event", value=self.event_name, inline=False)
            embed.add_field(name="Start date", value=self.date, inline=True)
            embed.add_field(name="Start time", value=self.time, inline=True)
            embed.add_field(name="Location", value=self.location, inline=False)
            embed.add_field(name="Description", value=self.description, inline=False)
            embed.add_field(name=" ", value=" ", inline=False)
            embed.add_field(name=" ", value=" ", inline=False)
            embed.set_footer(text=f"Created by {creator} on {datecreated}")

        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while adding a new event.", ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
           
