from datetime import datetime
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ..dao import RoomDao


SCOPES = ['https://www.googleapis.com/auth/calendar']
TIMEZONE = 'America/Los_Angeles'
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

SCOPES = ['https://www.googleapis.com/auth/calendar']


class AvailableRoom():
    name: str
    capacity: str

    def __init__(self, name=None, capacity=None):
        self.name = name
        self.capacity = capacity


def initialize_rooms():
    rooms = RoomDao().initRooms()
    return rooms


def get_events_from_google_calendar(reservation, calendar_id):
    user_info = {
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'refresh_token': reservation.google_auth_token,
    }
    creds = Credentials.from_authorized_user_info(info=user_info, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    events_result = service.events().list(calendarId=calendar_id, timeMin=reservation.start_time, maxResults=1,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result['items']


def get_datetime_from_time_string(time_string):
    return datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S%z')


def get_time_in_google_api_compatible_format(timestamp_str):
    timestamp_dt = datetime.strptime(timestamp_str, '%a %b %d %Y %H:%M:%S %Z %z')
    converted = timestamp_dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    return converted


def is_room_available(room, requested, event):
    start_dt = get_datetime_from_time_string(requested.start_time)
    end_dt = get_datetime_from_time_string(requested.end_time)
    event_start_dt = get_datetime_from_time_string(event['start']['dateTime'])
    room_availability_timediff = event_start_dt - start_dt
    room_requested_timediff = end_dt - start_dt
    if room_availability_timediff > room_requested_timediff and room.size >= int(requested.num_guests):
        return True
    return False


def get_rooms(roomsQuery, meeting_rooms):
    roomsQuery.start_time = get_time_in_google_api_compatible_format(roomsQuery.start_time)
    roomsQuery.end_time = get_time_in_google_api_compatible_format(roomsQuery.end_time)
    available_rooms = []
    for room in meeting_rooms:
        calendar_id = room.url.split('=')[1]
        events_list = get_events_from_google_calendar(roomsQuery, calendar_id)
        for event in events_list:
            if is_room_available(room, roomsQuery, event):
                available_room = AvailableRoom(room.name, room.size)
                available_rooms.append(available_room)
    return available_rooms


# Function to create a new event
def create_event(reservation, room_name):
    # Authenticate with Google Calendar API
    creds = Credentials.from_authorized_user_info(info=reservation.google_auth_token, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    # Calculate event start and end times
    start_time = get_time_in_google_api_compatible_format(reservation.start_time)
    end_time = get_time_in_google_api_compatible_format(reservation.end_time)

    # Create event object
    event = {
        'summary': reservation.title,
        'location': room_name,
        'description': reservation.event_description,
        'start': {
            'dateTime': start_time,
            'timeZone': TIMEZONE,
        },
        'end': {
            'dateTime': end_time,
            'timeZone': TIMEZONE,
        },
        'attendees': [
            {'email': reservation.email},
            {'email': [{'email': email.strip()} for email in reservation.guest_email.split(',')]},
        ],
        'reminders': {
            'useDefault': True,
        },
    }

    # Call the Calendar API to create the event
    event = service.events().insert(calendarId='primary', body=event).execute()
    # TODO: insert event in google calendar of the room as well
    print(f'Event created: {event.get("htmlLink")}')
    return True;