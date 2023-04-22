import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ..dao import RoomDao
from ..utils.datetime import get_datetime_from_time_string, get_time_in_google_api_compatible_format
from database.schemas.roomSchema import Privilege

SCOPES = ['https://www.googleapis.com/auth/calendar']
TIMEZONE = 'America/Los_Angeles'
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')


class GetRoomsInterface:
    def get_rooms(self):
        pass


class GetRoomsHandler:

    def __init__(self, request):
        self.roomDao = RoomDao()
        self.available_rooms = []
        self.request = request

    def get_events_from_google_calendar(self, calendar_id):
        user_info = {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'refresh_token': self.request.google_auth_token,
        }
        creds = Credentials.from_authorized_user_info(info=user_info, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        events_result = service.events().list(calendarId=calendar_id, timeMin=self.request.start_time, maxResults=1,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        return events_result['items']

    def is_room_available(self, room, event):
        start_dt = get_datetime_from_time_string(self.request.start_time)
        end_dt = get_datetime_from_time_string(self.request.end_time)
        event_start_dt = get_datetime_from_time_string(event['start']['dateTime'])
        room_availability_timediff = event_start_dt - start_dt
        room_requested_timediff = end_dt - start_dt
        if room_availability_timediff > room_requested_timediff and room.capacity >= int(self.request.num_guests):
            return True
        return False

    def get_rooms(self):
        self.request.start_time = get_time_in_google_api_compatible_format(self.request.start_time)
        self.request.end_time = get_time_in_google_api_compatible_format(self.request.end_time)
        for room in self.roomDao.getRoomsByPrivilege(privilege=Privilege.STUDENT):
            calendar_id = room.url.split('=')[1]
            events_list = self.get_events_from_google_calendar(calendar_id)
            for event in events_list:
                if self.is_room_available(room, event):
                    self.available_rooms.append({
                        'name': room.name,
                        'capacity': room.capacity,
                    })
        return self.available_rooms
    
class GetRoomsDecorator(GetRoomsInterface):
    _interface : GetRoomsInterface = None

    def __init__(self, interface):
        self._interface = interface
    
    def __getattr__(self, name):
        """
        Delegate all unimplemented methods to the wrapped component.
        """
        return getattr(self._interface, name)

    def get_rooms(self):
        return self._interface.getRooms()


class GetRoomsDecoratorAdmin(GetRoomsDecorator):
    def __init__(self, interface, request):
        super().__init__(interface)
        self.request = request
        self.roomDao = RoomDao()

    def get_rooms(self):
        rooms = self._interface.get_rooms()
        for room in self.roomDao.getRoomsByPrivilege(privilege=Privilege.STAFF_AND_FACULTY):
            calendar_id = room.url.split('=')[1]
            events_list = self.get_events_from_google_calendar(calendar_id)
            for event in events_list:
                if self.is_room_available(room, event):
                    rooms.append({
                        'name': room.name,
                        'capacity': room.capacity,
                    })
        return rooms



class ReserveRoomHandler:
    def __init__(self, reservation):
        self.reservation = reservation

    # Function to create a new event
    def create_event(self):
        # Authenticate with Google Calendar API
        user_info = {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'refresh_token': self.reservation.google_auth_token,
        }
        creds = Credentials.from_authorized_user_info(info=user_info, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        # Create event object
        event = {
            'summary': self.reservation.event.summary,
            'description': self.reservation.event.description,
            'start': {
                'dateTime': self.reservation.event.start['dateTime'],
                'timeZone': TIMEZONE,
            },
            'end': {
                'dateTime': self.reservation.event.end['dateTime'],
                'timeZone': TIMEZONE,
            },
            'attendees': self.reservation.event.guests,
            'reminders': {
                'useDefault': True,
            },
        }

        # TODO: Why does Google Calendar consider self.reservation.event.json() and event obj different?
        # print(self.reservation.event.json())
        # print(event)
        # inserted = service.events().insert(calendarId='primary', body=event).execute() # TODO: uncomment before demo
        # print(f'Event created: {inserted.get("htmlLink")}')
        return True;
