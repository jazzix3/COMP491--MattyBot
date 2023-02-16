# :wave: Hi there! MattyBot is currently under development
  
## About Us

### :sparkles: Vision Statement
For new student members on the CSUN Esports club Discord server who need help navigating the server and answering common questions, our “MattyBot” is a Discord bot that will aid incoming student members in answering their specific questions related to campus life and CSUN Esports, unlike a general help bot our bot is fully customizable to fit the needs of the CSUN Esports server and CSUN gaming community.

### :crystal_ball: Planned Features
- Basic commands for MattyBot to answer commonly asked questions such as:
  - !help to give user a menu of commands
  - !gamehours to tell user when the gamesroom is open
  - !location to tell user where the gameroom is located
  
- Google Calendar Implementations
  - Admins will update calendar for events, streams, etc.
  - Users have options to accept, decline, or respond tentatively to invitations
  
- Commands for Mattybot to check statistics from a certain game such as:
  - !rank to show user's current rank
  - !playtime to show user's total hours played

## Requirements
- Set up a virtual environment:
```
python3 -m venv venv
```
- Activate the virtual environment:
```
source venv/bin/activate
```

- Install libraries:
```
pip install discord
pip install dotenv
pip install sqlite
```

- Create a new file named `.env`, and include your bot token in the contents. It should be formatted like this:
```
DISCORD_BOT_TOKEN=yourbottokengoeshere
```

## Available Commands
### FAQ Commands: 
`/addfaq` – Will open a modal (form) to prompt the user for a question and answer, which will be added to the FAQ. When the user submits the form, an embed message is sent to the channel confirming that the FAQ has been added, and the question and answer are saved in the database.

`/clearallfaq` - Clears all FAQ from the database and sends a success message in an embed.

`/deletefaq` – Deletes a FAQ from the database based on user input. It first fetches all the FAQs from the database, creates an embed displaying each FAQ along with its number, and prompts the user to enter the number of the FAQ they want to delete. Then, it waits for the user to input the number and deletes the corresponding FAQ from the database. Finally, it sends a confirmation message to the user that the FAQ has been successfully deleted.

`/listfaq` -  Retrieves a list of all FAQ questions from the database and sends them in an embedded message. If there are no FAQ in the database, it sends a message stating that there are none.

`/listanswers` – Retrieves a list of all the answers from the database and returns them in an embed. If there are no FAQ in the database, it sends a message stating that there are none.

`/viewfaq` – Displays a dropdown menu of questions stored in the database. When a user selects a question from the menu, the corresponding answer and additional information (such as the creator and date created) are displayed in an embed.
 

### Event Commands:

`/addevent` - Will open a modal (form) to prompt the user to input details about the event.  When the user submits the form, it adds the new event to a database and sends a message confirming that the event has been added. The message includes information about the event, such as the event name, date, time, location, and description, as well as the name of the user who created the event and the date it was created.

`/clearallevents` - Clears all FAQ from the database and sends a success message in an embed.

`/deleteevent` - Deletes an event from the database based on user input. It first fetches all the events from the database, creates an embed displaying each event along with its number, and prompts the user to enter the number of the event they want to delete. Then, it waits for the user to input the number and deletes the corresponding even from the database. Finally, it sends a confirmation message to the user that the event has been successfully deleted.

`/listevents` - Retrieves a list of all events from the database and creates an embed that displays the names, dates, and times of all events. If there are no events in the database, it sends a message stating that there are none.

`/viewevents` - Displays a dropdown menu of events stored in the database. When a user selects an event from the menu, the event details from the database is populated in an embed. The message includes the event name, date, time, location, description, and creator, and has additional fields for users to indicate if they are attending, not attending, or unsure about the event.


