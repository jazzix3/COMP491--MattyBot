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
  
- ~~Commands for Mattybot to check statistics from a certain game such as:
  - ~~!rank to show user's current rank
  - ~~!playtime to show user's total hours played

- Polling system

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
pip install python-dotenv
pip install colorama
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```


- Create a new file named `.env`, and include your bot token in the contents. It should be formatted like this:
```
DISCORD_BOT_TOKEN=yourbottokengoeshere
```

- Assign "MattyBotAdmin" role to users to allow admin permissions

## Available Commands
### FAQ Commands: 

`/faqs` – Displays a dropdown menu of questions stored in the database. When a user selects a question from the menu, the corresponding answer and additional information (such as the creator and date created) are displayed in an embed.

`/faqs- list` -  Retrieves a list of all FAQ questions from the database and sends them in an embedded message. If there are no FAQ in the database, it sends a message stating that there are none.

`/faqs-- add` – (Admins only) Opens a modal (form) to prompt the user for a question and answer, which will be added to the FAQ. When the user submits the form, an embed message is sent to the channel confirming that the FAQ has been added, and the question and answer are saved in the database. 

`/faqs-- clearall` - (Admins only) Clears all FAQ from the database and sends a success message in an embed.

`/faqs-- delete` – (Admins only) Displays a dropdown menu of questions store in the database. When a user selects a question from the menu, the corresponding faq is deleted from the database.


### Event Commands:
`/events` - Displays a dropdown menu of events stored in the events database. When a user selects an event from the menu, the event details from the database is populated in an embed. The message includes the event name, description, location, start date & time, end date& time, creator, and date created. In addition, it displays the number of users who are attending, not attending, or are unsure.

`/events- calendar` - Generates an embed with a link to a public Google Calendar with all events.

`/events- list` - Retrieves a list of all events from the database and creates an embed that displays the names, dates, and times of all events. If there are no events in the database, it sends a message stating that there are none.

`/events- rsvp` - Displays a dropdown menu of eventsstored in the database. When a user selects an event from the menu, an invitation for a selected event is created and an embed is sent to the channel. Buttons are displayed so members can indicate whether they are "attending", "can't go", or "maybe". When a button is clicked, it updates the responses database with the member's RSVP and updates the original embed to display the number of attendees. This message is ephemeral, so only the member who called it can RSVP.

`/events-- add` - (Admins only) Opens a modal (form) to prompt the user to input details about the event.  When the user submits the form, it adds the new event to a database and sends a message confirming that the event has been added. The message includes information about the event, such as the event name, date, time, location, and description, as well as the name of the user who created the event and the date it was created.

`/events-- archive` - (Admins only) Displays a dropdown menu of eventsstored in the database. When a user selects an event from the menu, the corresponding event is moved from the events database to the archive database.

`/events-- clearall` - (Admins only) Clears all FAQ from the database and sends a success message in an embed.

`/events-- delete` - (Admins only) Displays a dropdown menu of events stored in the database. When a user selects an event from the menu, the corresponding event is deleted from the events database as well as the responses from the responses database.

`/events-- modify` - (Admins only) Displays a dropdown menu of events stored in the database. When a user selects an event from the menu, the event details from the database is populated in an embed. Then, a second dropdown is displayed for the user to select a field to modify. The user may select event name, description, location, start date & time, or end date & time. The selection opens a modal (form) to prompt the user to enter new input for the selected field. 

`/events-- invite` - (Admins only)  Displays a dropdown menu of events stored in the events database. When a user selects an event from the menu, an invitation for a selected event is created and an embed is sent to the channel. Buttons are displayed so members can indicate whether they are "attending", "can't go", or "maybe". When a button is clicked, it updates the responses database with the member's RSVP and updates the original embed to display the number of attendees. This message can be seen by all members so any member can RSVP.

### Archive Commands:
`/archive` - Displays a dropdown menu of events stored in the archive database. When a user selects an event from the menu, the event details from the database is populated in an embed.

`/restore` - (Admins only) Displays a dropdown menu of events stored in the archive database. When a user selects an event from the menu, the corresponding event is moved from the archive database to the events database.
