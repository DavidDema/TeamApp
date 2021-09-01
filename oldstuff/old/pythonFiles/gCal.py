from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from ics import Calendar
import requests
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
g_cal_id = 'c_uoa76mpbtomraj3brmbbb5giuk@group.calendar.google.com'

url_16 = "https://fussballoesterreich.at/netzwerk/icalendar/670725461856634215_485215725~1165862735024510172-T-x.ics"
url_07 = "https://fussballoesterreich.at/netzwerk/icalendar/670725461856634215_485215725~665233077005870945-T-x.ics"

sl_16_id = ''
sl_07_id = ''
sl_tr_id = ''

class googleApp:

    def __init__(self):
        self.__initCalendar()


    def __initCalendar(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)

    def clearAll(self):

        self.service.calendars().clear(calendarId=g_cal_id).execute()
        #self.service.calendars().delete(calendarId='c_moc7l1gksd1kittvgc8b7lu7l4@group.calendar.google.com').execute()
    def __str__(self):

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId=g_cal_id, timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        self.events = events_result.get('items', [])

        if not self.events:
            return 'No upcoming events found.'
        for event in self.events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            return start + event['summary']

    def createEvent(self, events):
        for e in events:
            print("Create event")
            print(str(e.location))
            event = self._getBody(e)

            event = self.service.events().insert(calendarId=g_cal_id,
                                            body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
    def _getBody(self, e):
        if isinstance(e, Game):
            body = {
                'summary': e.title,
                'location': str(e.location),

                'start': {
                    'dateTime': str(e.date),
                    'timeZone': 'Europe/Vienna',
                },
                'end': {
                    'dateTime': str(e.date + e.duration),
                    'timeZone': 'Europe/Vienna',
                },
                "source": {
                    "url": e.url,
                    "title": "Link zum Spiel"
                },
                'Home Team': e.homeTeam,
                'Away Team': e.awayTeam,
                'League': e.league,
                'Round': e.round_nr,
                'Link': e.url,
                'recurrence': [
                    'RRULE:FREQ=DAILY;COUNT=1'
                ],
                'reminders': {
                    'useDefault': True,
                },
            }
            return body

class Cal:
    def __init__(self, url, id):
        self.url    = url
        self.id     = id

        self.c = Calendar(requests.get(self.url).text)
        self.events = list(self.c.timeline)
        self.games = self.addGames(self.events)

    def addGames(self, eventList):
        g = []
        for e in eventList:
            homeTeam, awayTeam = self.convertTitle(e.name)
            league, round_nr = self.convertDescription(e.description)
            g_tmp = Game(homeTeam=homeTeam, awayTeam=awayTeam, date=e.begin, duration=e.duration,location=e.location, slack_channel=self.id, url=e.url, league=league, round_nr=round_nr)
            g.append(g_tmp)
        return g

    def convertDescription(self,d):
        tmp = d.split("(")
        league = tmp[0]
        round_nr = tmp[1].replace(")", "")
        return league, round_nr

    def convertTitle(self,text):
        tmp = text.split(" : ")
        homeTeam = tmp[0]
        awayTeam = tmp[1]
        # TODO: remove ()
        return homeTeam, awayTeam


class Event:
    def __init__(self, title, date, location, duration, slack_channel, url):
        self.title = title
        self.description = title
        self.date  = date
        self.location = location
        self.duration = duration

        self.slack_channel = slack_channel
        self.posted = 0
        self.updated = 0
        self.url = url

    def postEvent(self):
        print("Post event on "+self.slack_channel+"!")
        #slack class
        self.posted = 1

class Game(Event):

    def __init__(self,homeTeam, awayTeam, date, location, duration, slack_channel, url, league, round_nr):
    #def __init__(self, homeTeam, awayTeam, date,duration,location, slack_channel, league, round_nr):
        super().__init__(title="Spiel " + slack_channel, date=date, location=location, duration=duration, slack_channel=slack_channel, url=url)
        self.homeTeam   = homeTeam
        self.awayTeam   = awayTeam
        self.league     = league
        self.round_nr   = round_nr
        self.url2 = url

    def __str__(self):
        title = self.homeTeam + " vs " + self.awayTeam + "\n" + self.url2
        #subtitle = str(super.date) + "\n"
        return title# + subtitle

if __name__ == '__main__':
    gApp = googleApp()

    c16 = Cal(url_16,"16")

    gApp.createEvent(c16.games)

    #print(gApp)
    #gApp.clearAll()


