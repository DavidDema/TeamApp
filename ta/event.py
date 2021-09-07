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
    event_id = 0

    def __init__(self, title, date:datetime, location="Wien", duration=datetime.timedelta(hours=1), url="", message_id='', channel_id=''):

        self.id = Event.get_id()
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
        if self.get_state() == self.event_state_tmp:
            return
        elif self.event_state == "started":
            print("Event Nr."+ str(self.id) +" started!")
            self.updated = True
        elif self.event_state == "finished":
            print("Event Nr." + str(self.id) + " is finished!")
            self.updated = True


        if self.updated is True:
            print("Update Event")
            g.update_sheet_value(self)
            print("type: " + self.post_type)
            s.post_event(self)

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
        data.append(self.message_id)
        name.append("message_id")
        data.append(self.url)
        name.append("url")

        if      isinstance(self, Game):
            data.append("GAME")
        elif    isinstance(self, Training):
            data.append("Training")
        elif    isinstance(self, Event):
            data.append("EVENT")
        name.append("type")

        return data, name

    def __str__(self):

        message = str(self.event_id) + "| " + str(self.title) + " @ " + str(self.location) + "\n\t"\
                  +datetime.datetime.strftime(self.date, "%D") + " at " + datetime.datetime.strftime(self.date, "%H") + " o'clock" + "\n\t"\
                  +"State:" + str(self.event_state) +" | Posted:" + str(self.posted) +"\n\t"\
                  +"Slack:\n\t\t"\
                  +"ch_id: "+ str(self.channel_id) + "\n\t\t"\
                  +" m_id:" + str(self.message_id)
        return message

    @staticmethod
    def get_id():
        Event.event_id += 1
        return Event.event_id

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

    def __init__(self, title,date,location,duration=datetime.timedelta(hours=2), channel_id="", message_id="", pitch="NORMAL"):
        super().__init__(title=title,date=date, location=location, duration=duration, channel_id=channel_id, message_id=message_id)

        self.pitch = pitch

    def get_data(self):
        data = []
        data, name = super().get_data()
        data.append(self.pitch)
        name.append("pitch")
        return data, name

class sApp:

    def __init__(self):
        print("Slack init")
        app.client.chat_postMessage(
            channel=par.TEST_ID,
            text=(
                "--------------------"+
                "\n New Test @ "+str(datetime.datetime.today())+
                "\n-------------------"
            )
        )

    def get_event_message(self, event):
        message = "no message"

        if isinstance(event, Game):
            if event.post_type == "primary":
                message = (
                        "Spiel am *"
                        + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date,'%m')
                        + "* um " + str(datetime.datetime.strftime(event.date, '%H:%M')) + " Uhr!\n"
                        + "Treffpunkt um " + str(datetime.datetime.strftime(event.date-datetime.timedelta(hours=1), '%H:%M')) + " Uhr\n"
                        + ":thumbsup: = Zusage, :thumbsdown: = Absage!"
                )
            if event.post_type == "finished":
                message = (
                        "~Spiel am *"
                        + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date,
                                                                                                          '%m')
                        + "* um " + str(datetime.datetime.strftime(event.date, '%H:%M')) + " Uhr!~\n"
                        + "~Treffpunkt um " + str(
                    datetime.datetime.strftime(event.date - datetime.timedelta(hours=1), '%H:%M')) + " Uhr~\n"
                )
            if event.post_type == "preview":
                message = (
                        "---------------------------------------------\n" +
                        "---------------------------------------------\n" +
                        "N\"achstes Training am *"  # + event.weekday + ", "
                        + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date,
                                                                                                          '%m')
                        + "* um " + str(datetime.datetime.strftime(event.date, '%M')) + " Uhr!"
                )
        elif isinstance(event,Training):
            if event.post_type == "primary":
                message = (
                        "Training am *"  # + event.weekday + ", "
                        + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date,
                                                                                                          '%m')
                        + "* um " + str(datetime.datetime.strftime(event.date, '%M')) + " Uhr!\n"
                        + ":muscle: = SGS07,:punch: = SGS16, :thumbsdown: = Absage!"
                )
            if event.post_type == "finished":
                message = (
                        "~Training am *"  # + event.weekday + ", "
                        + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date,
                                                                                                          '%m')
                        + "* um " + str(datetime.datetime.strftime(event.date, '%M')) + " Uhr!~\n"
                )
            if event.post_type == "preview":
                message = (
                        "---------------------------------------------\n" +
                        "---------------------------------------------\n" +
                        "N\"achstes Training am *"  # + event.weekday + ", "
                        + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date,
                                                                                                          '%m')
                        + "* um " + str(datetime.datetime.strftime(event.date, '%M')) + " Uhr!"
                )
        elif isinstance(event,Event):
            if event.post_type == "primary":
                message = (
                        event.title + " am *"
                        + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date,'%m')
                        + "* um " + str(datetime.datetime.strftime(event.date, '%H:%M')) + " Uhr!\n"
                        + ":thumbsup: = Zusage, :thumbsdown: = Absage!"
                )
            if event.post_type == "finished":
                message = (
                        "~" + event.title + " am *"
                        + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date,'%m')
                        + "* um " + str(datetime.datetime.strftime(event.date, '%H:%M')) + " Uhr!~\n"
                )
            if event.post_type == "preview":
                message = (
                        "---------------------------------------------\n" +
                        "---------------------------------------------\n" +
                        "N\"achstes Training am *"  # + event.weekday + ", "
                        + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date,
                                                                                                          '%m')
                        + "* um " + str(datetime.datetime.strftime(event.date, '%M')) + " Uhr!"
                )
        else:
            message = ""

        return message

    def post_event(self,event):
        print("post event on slack:" + event.post_type)

        if (event.posted is False) and (event.post_type == "finished"):
            event.post_type = "primary"
            print("First create post")

        message = self.get_event_message(event=event)
        print(message)

        if event.channel_id == "":
            print("Missing channel id!")
            return False

        if event.post_type=="finished":
            response = app.client.chat_update(
                channel=event.channel_id,
                ts= event.message_id,
                text=message
            )
        elif event.post_type=="primary":
            if event.message_id == "":
                response = app.client.chat_postMessage(
                    channel=event.channel_id,
                    text=message
                )
            else:
                response = app.client.chat_update(
                    channel=event.channel_id,
                    ts=event.message_id,
                    text=message
                )
        elif event.post_type=="preview":
            response = app.client.chat_postMessage(
                channel=event.channel_id,
                text=message
            )
        else:
            response = []

        try:
            event.message_id = response["ts"]
        except:
            print("No message id found!")

        print("ok: "+ str(response["ok"]))
        return response["ok"]

    def get_weekday(self):
        if self.date.today().weekday() == 0:
            return "Montag", "Mo"
        if self.date.today().weekday() == 1:
            return "Dienstag", "Di"
        if self.date.today().weekday() == 2:
            return "Mittwoch", "Mi"
        if self.date.today().weekday() == 3:
            return "Donnerstag", "Do"
        if self.date.today().weekday() == 4:
            return "Freitag", "Fr"
        if self.date.today().weekday() == 5:
            return "Samstag", "Sa"
        if self.date.today().weekday() == 6:
            return "Sonntag", "So"


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

        #
        row = self.get_row("id", event.id)
        if row == -1:
        #if True:
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
                event = Event(title=title,date=date,location=location,duration=duration, channel_id=channel_id, message_id=message_id,
                                  url=url)
            else:
                print("TYPE INCORRECT")

            events.append(event)
            print(event)

        return events

g = gApp()
s = sApp()

