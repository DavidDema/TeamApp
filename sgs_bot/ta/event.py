import datetime
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

#Google import
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import par

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


class Event:

    def __init__(self, title, date:datetime, location="Wien", duration=datetime.timedelta(hours=1), url="", message_id='', channel_id=''):

        self.id = -1

        self.title = title
        self.date  = date
        self.location = location
        self.duration = duration

        #Slack API
        self.channel_id = channel_id
        self.message_id = message_id
        self.url = url

        self.event_state_tmp = 'none'
        self.event_state = 'none'
        #upcoming, started, finished
        self.posted = False
        self.post_type = 'primary'

        self.updated = False

        if self.message_id != '':
            print("Event already posted")
            self.posted = True
        #if channel_id != '':
            #Ready to post
         #   s.post_event(self)

    def post(self):

        if self.posted == False:
            print("post")
            self.posted = s.post_event(self)
        #slack class

    def update(self):

        #Check state
        if self.get_state() != self.event_state_tmp:
            if self.event_state == "started":
                print("Event Nr."+ str(self.id) +" started!")
                self.updated = True
            elif self.event_state == "finished":
                print("Event Nr." + str(self.id) + " is finished!")
                self.post_type = "finished"
                self.updated = True

        if self.updated is True:
            print("Update Event")
            self.posted = s.post_event(self)
            g.update_sheet_value(self)
            self.updated = False

    def update_data(self, event):
        print("Update data")
        self.updated = True
        self.date = event.date
        self.location = event.location
        self.duration = event.duration

    def get_state(self):
        now = datetime.datetime.today()
        self.event_state_tmp = self.event_state
        if now < (self.date):
            self.event_state = "upcoming"
            self.post_type == "primary"
        elif now > (self.date+self.duration):
            self.event_state = "finished"
            self.post_type == "finished"
        else:
            self.event_state = "started"
            self.post_type == "primary"

        #print("state: "+ self.event_state)
        return self.event_state

    def get_data(self):
        data = []
        name = []
        data.append(str(self.id))
        name.append("id")
        data.append(self.title)
        name.append("title")
        data.append(self.event_state)
        name.append("status")
        data.append(str(self.date))
        name.append("date")
        data.append(self.location)
        name.append("location")
        data.append(str(self.duration))
        name.append("duration")
        data.append(self.channel_id)
        name.append("channel_id")

        msg_id = ''
        try:
            msg_id = self.message_id.split('.')[0] + '.' + self.message_id.split('.')[1]
        except:
            print("msg id not found or incorrect")

        data.append(msg_id)
        name.append("message_id")
        data.append(self.url)
        name.append("url")

        if      isinstance(self, Game):
            data.append("GAME")
        elif    isinstance(self, Training):
            data.append("TRAINING")
        elif    isinstance(self, Event):
            data.append("EVENT")
        name.append("type")

        return data, name

    def __str__(self):

        message = str(self.id) + "| " + str(self.title) + " @ " + str(self.location) + "\n\t"\
                  +datetime.datetime.strftime(self.date, "%D") + " at " + datetime.datetime.strftime(self.date, "%H") + " o'clock" + "\n\t"\
                  +"State:" + str(self.event_state) +" | Posted:" + str(self.posted) +"\n\t"\
                  +"Slack:\n\t\t"\
                  +"ch_id: "+ str(self.channel_id) + "\n\t\t"\
                  +" m_id:" + str(self.message_id)
        return message

class Game(Event):

    def __init__(self, title,date,location="Wien",duration=datetime.timedelta(hours=1), channel_id="", message_id="",homeTeam="ht", awayTeam="at", url="", league="", round="", pitch="NORMAL"):

        super().__init__(title=title,date=date, location=location, duration=duration, channel_id=channel_id, message_id=message_id, url=url)

        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.url = url
        self.league = league
        self.round = round
        self.pitch = pitch

    def get_data(self):
        data, name = (super().get_data())

        data.append(self.homeTeam)
        name.append("homeTeam")
        data.append(self.awayTeam)
        name.append("awayTeam")
        data.append(self.league)
        name.append("league")
        data.append(str(self.round))
        name.append("round")
        data.append(self.pitch)
        name.append("pitch")

        return data, name

class Training(Event):

    def __init__(self, title,date,location,duration=datetime.timedelta(hours=2), channel_id="", message_id="", pitch="NORMAL", url=""):
        super().__init__(title=title,date=date, location=location, duration=duration, channel_id=channel_id, message_id=message_id, url=url)

        self.pitch = pitch

    def get_data(self):
        data = []
        data, name = super().get_data()
        data.append(self.pitch)
        name.append("pitch")
        return data, name



class gApp:


    def __init__(self):
        self.startup = True

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', par.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', par.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        self.sheet = self.service.spreadsheets()
        self.ranges = []



    def update_sheet_value(self, event:Event):
        print("Update Sheet")
        header = self.get_sheet_values(par.EVENTS_HEADER)[0]
        val, nam = event.get_data()
        message = []

        for h in header:
            try:
                message.append(str(val[nam.index(h)]))
            except:
                print("Value not in list: " + h)

        value_range_body = {
            "values": [
                message
            ]
        }


        row = self.get_row("id", event.id)
        if row == -1:
            value_input_option = 'USER_ENTERED'
            insert_data_option = 'OVERWRITE'
            request = self.service.spreadsheets().values().append(spreadsheetId=par.SAMPLE_SPREADSHEET_ID,
                                                                  range=par.EVENTS_RANGE,
                                                                  valueInputOption=value_input_option,
                                                                  insertDataOption=insert_data_option,
                                                                  body=value_range_body)
        else:
            value_range_body2 = {

            }
            request = self.service.spreadsheets().values().clear(spreadsheetId=par.SAMPLE_SPREADSHEET_ID,
                                                                 range=par.EVENTS_RANGE.split("!")[0]+"!A"+ str(row) + ":U" + str(row),
                                                                 body=value_range_body2)
            response = request.execute()

            value_input_option = 'USER_ENTERED'
            request = self.service.spreadsheets().values().update(spreadsheetId=par.SAMPLE_SPREADSHEET_ID,
                                                                  range=par.EVENTS_RANGE.split("!")[0]+"!A"+ str(row) + ":U" + str(row),
                                                                  valueInputOption=value_input_option,
                                                                  body=value_range_body)
        response = request.execute()

    def read_sheet(self, range):

        values = self.get_sheet_values(range)
        events = []
        if values is None:
            # print("sheet empty")
            return events

        if range == par.ADD_RANGE:
            header = self.get_sheet_values(par.ADD_HEADER)[0]
        elif range == par.EVENTS_RANGE:
            header = self.get_sheet_values(par.EVENTS_HEADER)[0]
        else:
            print("read_sheet not possible. Range not compatible!")

        for col in values:
            if range == par.ADD_RANGE:

                channel_id = par.get_channel_id(self.get_value(col=col, header=header, search_val='slack_channel'))
                message_id = ''

            elif range == par.EVENTS_RANGE:

                status = self.get_value(col=col, header=header, search_val='status')
                channel_id = self.get_value(col=col, header=header, search_val='channel_id')
                message_id = self.get_value(col=col, header=header, search_val='message_id')
            else:
                channel_id = ""
                message_id = ""


            type =      self.get_value(col=col, header=header, search_val='type')
            title =     self.get_value(col=col, header=header, search_val='title')
            location =  self.get_value(col=col, header=header, search_val='location')
            url =       self.get_value(col=col, header=header, search_val='url')

            homeTeam =  self.get_value(col=col, header=header, search_val='homeTeam')
            awayTeam =  self.get_value(col=col, header=header, search_val='awayTeam')
            league =    self.get_value(col=col, header=header, search_val='league')
            round =     self.get_value(col=col, header=header, search_val='round')
            pitch =     self.get_value(col=col, header=header, search_val='pitch')

            #2021-09-02 17:13:00.223183
            date = datetime.datetime.strptime(
                self.get_value(col=col, header=header, search_val='date'),
                "%Y-%m-%d %H:%M:%S.%f")

            d_h, d_min, d_sec = self.get_value(col=col, header=header, search_val='duration').split(":")
            duration = datetime.timedelta(hours=int(d_h), minutes=int(d_min), seconds=int(d_sec))

            event = None
            if type == "GAME":
                event=  Game(title=title,date=date,location=location,duration=duration, channel_id=channel_id, message_id=message_id,
                                  homeTeam=homeTeam, awayTeam=awayTeam, url=url, pitch=pitch, league=league, round=round
                                  )
            elif type == "EVENT":
                event=  Event(title=title,date=date,location=location,duration=duration, channel_id=channel_id, message_id=message_id,
                                  url=url)
            elif type == "TRAINING":
                event = Training(title=title,date=date,location=location,duration=duration, channel_id=channel_id, message_id=message_id,
                                  url=url, pitch=pitch)
            else:
                print("TYPE INCORRECT")

            events.append(event)

        return events

    def get_sheet_values(self, range):
        result = self.sheet.values().get(spreadsheetId=par.SAMPLE_SPREADSHEET_ID,
                                         range=range).execute()
        values = result.get('values', [])

        if not values:
            #print('No data found.')
            return None
        else:
            #print('Values found.')
            return values

    def get_row(self, col_name, val):
        row = 2
        values =    self.get_sheet_values(par.EVENTS_RANGE)
        header =    self.get_sheet_values(par.EVENTS_HEADER)[0]

        if values is None:
            return -1
        for col in values:
            if self.get_value(col=col, header=header, search_val=col_name) == str(val):
                return row
            row +=1
        return -1

    def clear_sheet(self):
        #print("Clear sheet")
        value_range_body = {

        }
        request = self.service.spreadsheets().values().clear(spreadsheetId=par.SAMPLE_SPREADSHEET_ID, range=par.ADD_RANGE,
                                                        body=value_range_body)
        response = request.execute()

    def get_value(self, col, header, search_val):

        try:
            val = col[header.index(str(search_val))]
        except:
            print("Value not found")
            return ""
        return val

g = gApp()
s = sApp()

