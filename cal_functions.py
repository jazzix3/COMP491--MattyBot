
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = Credentials.from_authorized_user_file('cal_token.json', SCOPES)
service = build('calendar', 'v3', credentials=creds)


class GoogleCalendarEvents():

    def AddToCalendar(event_name, location, description):
        event_name = event_name
        location = location
        description = description
        
        event = {
            'summary': f'{event_name}',
            'location': f'{location}',
            'description': f'{description}',
            'start': {
                'dateTime': '2023-06-1T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2023-06-01T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()

        event_link = event.get('htmlLink')
        print('Event created: %s' % (event_link))


