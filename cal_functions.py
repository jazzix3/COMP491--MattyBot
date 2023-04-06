from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = Credentials.from_authorized_user_file('cal_token.json', SCOPES)
service = build('calendar', 'v3', credentials=creds)


class GoogleCalendarEvents():

    async def AddToCalendar(event_name, location, description, start_date, start_time, end_date, end_time):
        event_name = event_name
        location = location
        description = description
        start_date =start_date
        start_time = start_time
        end_date = end_date
        end_time = end_time
        
        event = {
            'summary': f'{event_name}',
            'location': f'{location}',
            'description': f'{description}',
            'start': {
                'dateTime': f'{start_date}T{start_time}:00-07:00', #YYYY-MM-DDTHH:mm:ss.000Z
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': f'{end_date}T{end_time}:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()

        event_link = (event.get('htmlLink'))
        event_id = event['id']
        
        print('Event created: %s' % (event.get('htmlLink')))
        print('Event ID: %s' % (event_id))

        return (event_link, event_id)
    
    
    async def ClearCalendar():
        service.calendars().clear(calendarId='primary').execute()

    
    async def DeleteFromCalendar(event_id):
        eventId = event_id
        service.events().delete(calendarId='primary', eventId=f'{eventId}').execute()

    
    async def LinkCalendar():
        calendar_list = service.calendarList().list().execute()
        for calendar in calendar_list['items']:
            if calendar.get('primary'):
                primary_calendar_id = calendar['id']
                break
        calendar_link = f'https://calendar.google.com/calendar/u/0/embed?src={primary_calendar_id}&ctz=America/Los_Angeles'
        return calendar_link



    async def ModifyEventCalendar(event_id, new_value, field):
        eventId = event_id
        event = service.events().get(calendarId='primary', eventId=f'{eventId}').execute()
        
        event[field] = new_value
        service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

    
    async def ModifyDateTimeCalendar(event_id, new_start_date, new_start_time, new_end_date, new_end_time):
        eventId = event_id
        event = service.events().get(calendarId='primary', eventId=f'{eventId}').execute()
        
        
        event['start'] = {'dateTime': f'{new_start_date}T{new_start_time}:00-07:00', 'timeZone': 'America/Los_Angeles',}
        event['end'] = {'dateTime': f'{new_end_date}T{new_end_time}:00-07:00','timeZone': 'America/Los_Angeles',}
        service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()




        


