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
      





           
