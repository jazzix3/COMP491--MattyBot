import discord
from discord import app_commands, ui,  Interaction, Embed, SelectOption, Color
from discord.ext import commands
from matty_db import Database


class ExampleDB(commands.GroupCog, name="test"):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = Database()  

    @app_commands.command(name="insertdb", description="Fills the database with FAQ and event examples")
    async def insertdb(self, interaction: Interaction):
        server_id = interaction.guild_id
        self.db.query("DELETE FROM faqs_db")
        self.db.query("DELETE FROM events_db")
        self.db.query("DELETE FROM responses_db")
        
        
        try:
            faqsql = "INSERT INTO faqs_db(server_id, question, answer, creator, datecreated) VALUES (?, ?, ?, ?, ?)"
            val = (server_id, 
                "What are the game room hours?", 
                "The game room hours are from 10am Monday  through Friday \nBUT sometimes our teams will be practicing on cerain Mondays,Tuesdays, Fridays and if they are, the Game Room would start wrapping up around 5:30 to prep for our teams from 6-8pm", 
                "Jazzi", 
                "2/14/2023")
            self.db.query_input(faqsql,val)

            val = (server_id, 
                "Where is the games room located?", 
                "The USU Games Room is located in the lower level of the East Conference Center, across from the Student Recreation Center. \n\nFor more information visit the website \nhttps://www.csun.edu/src/games-room%27%27", 
                "Jazzi", 
                "2/14/2023")
            self.db.query_input(faqsql,val)

            val = (server_id, 
                "How do I register to become a member?", 
                "To become a member, you must complete the following forms:\n\n 1. Waiver\n 2. Emergency Card\n 3. Code of Conduct and Academic Release\n 4. Participant Medical Release\n\n Then, you must submit copies of Student ID and Driver’s License to the Sport Clubs Office to Sportclubs@csunas.org ", 
                "Jazzi", 
                "3/1/2023")
            self.db.query_input(faqsql,val)

            val = (server_id, 
                "What games do teams compete in?", 
                "College League of Legends(CLOL) - League of Legends\n Collegiate StarLeague (CSL) - League of Legends\n Counter-Strike:Global Offensive\n Tespa’s Overwatch Collegiate: Championship Series - Overwatch\n College Carball Association (CCA) - RocketLeague", 
                "Jazzi", 
                "3/1/2023")
            self.db.query_input(faqsql,val)

            val = (server_id, 
                "Who are the club officers?", 
                "President: Ash\n Vice-President: Misty\n Secretary: May\n Treasurer: Brock\n Faculty Advisor: Professor Oak", 
                "Jazzi", 
                "3/1/2023")
            self.db.query_input(faqsql,val)

            eventsql = "INSERT INTO events_db(server_id, event_name, date, time, location, description, creator, datecreated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            val = (server_id, 
                "FIFA 23 Tournament", 
                "3/6/2023",
                "5:00 PM",
                "Games Room, University Student Union",
                "Kick it in the Games Room and compete against other Matadors in FIFA ‘23 tournaments this semester! These tournaments are a great way to have fun while also having the potential of scoring some awesome prizes!", 
                "Jazzi", 
                "2/14/2023")
            self.db.query_input(eventsql,val)


            val = (server_id, 
                "MataGame Night", 
                "3/17/2023",
                "7:00 PM",
                "Games Room, University Student Union",
                "This is MataGame Night! Come and join celebrate all things esports! Join us for a night of fun with free play and live exhibition matches across many games!", 
                "Jazzi", 
                "3/1/2023")
            self.db.query_input(eventsql,val)


            val = (server_id, 
                "Super Smash Bros. Ultimate Tournament", 
                "3/30/2023",
                "5:00 PM",
                "Games Room, University Student Union",
                "The Games Room of the University Student Union invites players to fight their way to the top during the Super Smash Bros. Ultimate Tournament! Whether you’re a beginner entering your first tourney, or a seasoned wavedasher, everyone is welcome to battle it out on Nintendo Switch. Our first-place champions will go home with a $50 Amazon gift card, second will snag $25 Amazon gift card and third will walk away with a $15 Amazon gift card.", 
                "Jazzi", 
                "3/1/2023")
            self.db.query_input(eventsql,val)

        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while inserting faqs and events examples into the database", ephemeral=True)
        else:
            await interaction.response.send_message("Success! FAQ and events examples have been inserted into the database", ephemeral=True)

            
            
    @app_commands.command(name="insertresp", description="Fills the database with responses")
    async def insertresp(self, interaction: Interaction):   
        self.db.query("DELETE FROM responses_db")
        responsessql = "INSERT INTO responses_db(event_id, username, response) VALUES (?, ?, ?)"
        
        try:
            rows = self.db.query_fetch("SELECT event_id FROM events_db WHERE event_name = ?", ("FIFA 23 Tournament",))
            event_id= rows[0][0]
            val = (event_id, "Eevee", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Vaporeon", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Joleton", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Flareon", "declined")
            self.db.query_input(responsessql,val)
            val = (event_id, "Sylveon", "declined")
            self.db.query_input(responsessql,val)
            val = (event_id, "Umbreon", "declined")
            self.db.query_input(responsessql,val)
            val = (event_id, "Espeon", "tentative")
            self.db.query_input(responsessql,val)
            val = (event_id, "Leafeon", "tentative")
            self.db.query_input(responsessql,val)
            val = (event_id, "Glaceon", "tentative")
            self.db.query_input(responsessql,val)



            rows = self.db.query_fetch("SELECT event_id FROM events_db WHERE event_name = ?", ("MataGame Night",))
            event_id= rows[0][0]
            val = (event_id, "Eevee", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Vaporeon", "declined")
            self.db.query_input(responsessql,val)
            val = (event_id, "Joleton", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Flareon", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Sylveon", "declined")
            self.db.query_input(responsessql,val)
            val = (event_id, "Umbreon", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Espeon", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Leafeon", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Glaceon", "tentative")
            self.db.query_input(responsessql,val)


            rows = self.db.query_fetch("SELECT event_id FROM events_db WHERE event_name = ?", ("Super Smash Bros. Ultimate Tournament",))
            event_id= rows[0][0]
            val = (event_id, "Eevee", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Vaporeon", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Joleton", "tentative")
            self.db.query_input(responsessql,val)
            val = (event_id, "Flareon", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Sylveon", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Umbreon", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Espeon", "accepted")
            self.db.query_input(responsessql,val)
            val = (event_id, "Leafeon", "tentative")
            self.db.query_input(responsessql,val)
            val = (event_id, "Glaceon", "accepted")
            self.db.query_input(responsessql,val)

        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            await interaction.response.send_message("Oops! Something went wrong while inserting responses into database", ephemeral=True)
        else:
            await interaction.response.send_message("Success! Responses have been inserted into the database", ephemeral=True)


    @app_commands.command(name="clearallresponses", description="Clear all responses from the database")
    async def clearallresponses(self, interaction: Interaction):
        self.db.query("DELETE FROM responses_db")
        embed = Embed(title="Clear all responses", description="Success! All responses have been cleared from the database", color=Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)

 
            



        

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ExampleDB(client))

        