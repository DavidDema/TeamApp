import datetime
import os
from time import sleep

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

#Google import
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import par

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# welcome_channel_id = par.SPIELE07_ID
#
# user_id = event["user"]
# reaction = event["reaction"]
# ts = event["event_ts"]
#
# t.reaction_added(user_id=user_id, reaction=reaction, ts=ts)
# print(user_id + " answered with " + reaction + " to ts "+ ts)

@app.event("reaction_added")
def reaction_added(event, say):
    user_id = event["user"]
    reaction = event["reaction"]
    ts = event["item"]["ts"]

    t.reaction_event(reaction=reaction, user_id=user_id, ts=ts, added=True)


@app.event("reaction_removed")
def reaction_removed(event, say):
    user_id = event["user"]
    reaction = event["reaction"]
    ts = event["event_ts"]

    t.reaction_event(reaction=reaction, user_id=user_id, added=False)

@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        text=
        "hello"
    )

class Event:

    def __init__(self, posting_date, date, type, league, round, homeTeam, awayTeam,
                 team="", title="", description="", url="",participant_count=0, participant_list=[], status="", sheet_row=-1, range="", location="Red Star Penzing Platz", pitch="Kunstrasen", channel="", timestamp=""):
        # status	type	posting_date	date	channel_id	timestamp	league	round	team	homeTeam	awayTeam	pitchType	participant_count	participant_list	title	description

        self.title = title
        self.description = description
        self.status = status

        self.type = type

        self.channel = channel
        self.timestamp = timestamp
        self.participant_count = 0
        self.participant_list = []
        #self.participant_list = participant_list

        self.date = date
        self.posting_date = posting_date
        self.duration = datetime.timedelta(hours=2)

        self.location = location
        self.url = url
        if self.url == "":
            self.url = self.get_url()

        self.pitch = pitch
        self.league = league
        self.round = round

        self.team = team
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam

        self.sheet_row = sheet_row
        self.range = range

        self.posted = False
        if self.timestamp != '':
            self.posted = True

        self.time_state = "init"
        self.time_state_tmp = "0"
        self.time_state = self.get_state()
        self.update = True

    def update_event(self):

        #Check state
        if self.get_state() is True:
            print("State changed -> update")
            self.update = True

        if self.update is True:
            print("Update Event")
            self.posted = s.post_event(self)
            if self.posted == True:
                self.status = "POSTED"
            self.update = False

    def get_state(self):

        now = datetime.datetime.today()

        self.time_state_tmp = self.time_state
        if now < (self.date):
            self.time_state = "coming up"
            if self.posted is True:
                self.status = "POSTED"
        elif now > (self.date+self.duration):
            self.time_state = "finished"
            if self.posted is True:
                self.status = "OVER"
        else:
            self.time_state = "started"
            if self.posted is True:
                self.status = "LIVE"

        if self.time_state != self.time_state_tmp:
            print("Event "+str(self.sheet_row) + " is " + self.time_state)
            return True
        else:
            return False

    def reaction_added(self, reaction, user_id):
        if reaction == "+1":
            self.participant_count += 1
            self.participant_list.append(user_id)
        if reaction == "-1":
            self.participant_count += 0

        print("New pariticant @" + str(user_id) + "| New count="+ str(self.participant_count))

    def reaction_removed(self, reaction, user_id):
        if reaction == "+1":
            self.participant_count -= 1
            self.participant_list.remove(user_id)
        if reaction == "-1":
            self.participant_count += 0

        print("Remove pariticant @" + str(user_id) + "| New count=" + str(self.participant_count))
        #g.update_event_sheet(self)

    def get_data(self):
        data = []
        name = []
        # status	type	posting_date	date	channel_id	timestamp	location	league	round	team	homeTeam	awayTeam	pitchType	participant_count	participant_list	title	description

        data.append(str(self.status))
        name.append("status")
        data.append(self.type)
        name.append("type")
        data.append(self.title)
        name.append("title")
        data.append(self.description)
        name.append("description")

        data.append(self.location)
        name.append("location")

        data.append(self.participant_list)
        name.append("participant_list")
        data.append(self.participant_count)
        name.append("participant_count")

        data.append(self.channel)
        name.append("channel_id")
        data.append(self.timestamp)
        name.append("timestamp")



        data.append(g.convert_date(self.date, True))
        name.append("date")
        data.append(g.convert_date(self.posting_date, True))
        name.append("posting_date")

        data.append(self.team)
        name.append("team")
        data.append(self.homeTeam)
        name.append("homeTeam")
        data.append(self.awayTeam)
        name.append("awayTeam")
        data.append(self.pitch)
        name.append("pitchType")
        data.append(str(self.league))
        name.append("league")
        data.append(self.round)
        name.append("round")

        data.append(self.url)
        name.append("url")

        return data, name

    def get_url(self):
        location = self.location.replace(" ", "+")
        return par.g_maps_url + location + "+Wien"

    def __str__(self):

        # message =  + "| " + str(self.title) + " @ " + str(self.location) + "\n\t"\
        #           +datetime.datetime.strftime(self.date, "%D") + " at " + datetime.datetime.strftime(self.date, "%H") + " o'clock" + "\n\t"\
        #           +"State:" + str(self.event_state) +" | Posted:" + str(self.posted) +"\n\t"\
        #           +"Slack:\n\t\t"\
        #           +"ch_id: "+ str(self.channel_id) + "\n\t\t"\
        #           +" m_id:" + str(self.message_id)
        message = (
                str(self.date) +"|" +self.status + " -> " + self.homeTeam + " vs " + self.awayTeam +
                "\nURL:" + self.url
        )
        return message

class gApp:

    def __init__(self):
        self.startup = True

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time
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

    def update_event_sheet(self, event:Event):
        #print("Update Sheet")
        header = self.get_sheet_values(par.get_header(event.range))[0]
        print(header)
        val, nam = event.get_data()
        message = []

        for h in header:
            try:
                message.append(str(val[nam.index(h)]))
            except:
                print("Value not in list: " + h)
                message.append("")

        value_range_body = {
            "values": [
                message
            ]
        }

        row = event.sheet_row
        if row == -1:
            value_input_option = 'USER_ENTERED'
            insert_data_option = 'OVERWRITE'
            request = self.service.spreadsheets().values().append(spreadsheetId=par.SAMPLE_SPREADSHEET_ID,
                                                                  range=event.range,
                                                                  valueInputOption=value_input_option,
                                                                  insertDataOption=insert_data_option,
                                                                  body=value_range_body)
        else:
            value_range_body2 = {

            }
            request = self.service.spreadsheets().values().clear(spreadsheetId=par.SAMPLE_SPREADSHEET_ID,
                                                                 range=event.range.split("!")[0]+"!A"+ str(row) + ":U" + str(row),
                                                                 body=value_range_body2)

            try:
                response = request.execute()
            except:
                print("Not updated")
                response=""

            value_input_option = 'USER_ENTERED'
            request = self.service.spreadsheets().values().update(spreadsheetId=par.SAMPLE_SPREADSHEET_ID,
                                                                  range=event.range.split("!")[0]+"!A"+ str(row) + ":U" + str(row),
                                                                  valueInputOption=value_input_option,
                                                                  body=value_range_body)
        try:
            response = request.execute()
        except:
            print("Not updated")
            response = ""

    def convert_date(self, date_str, toString=False):
        if toString is True:
            #print("Converting " + str(date_str) + " to String...")
            date = date_str.strftime(par.TIME_FORMAT)
        else:
            #print("Converting "+ str(date_str) + " to Datetime...")
            date = datetime.datetime.strptime(date_str, par.TIME_FORMAT)
        return date

    def read_sheet(self, ranges):
        events = []
        for range in ranges:

            values = self.get_sheet_values(range)
            row = 1

            if values is None:
                # print("sheet empty")
                return events

            header = self.get_sheet_values(par.get_header(range))[0]
            for col in values:
                #status	type	posting_date	date	channel_id	timestamp	league	round	team	homeTeam	awayTeam	pitchType	participant_count	participant_list	title	description
                row += 1

                status = self.get_value(col=col, header=header, search_val='status')
                type = self.get_value(col=col, header=header, search_val='type')

                posting_date = self.convert_date(self.get_value(col=col, header=header, search_val='posting_date'))
                date = self.convert_date(self.get_value(col=col, header=header, search_val='date'))

                channel_id = self.get_value(col=col, header=header, search_val='channel_id')
                timestamp = self.get_value(col=col, header=header, search_val='timestamp')

                title = self.get_value(col=col, header=header, search_val='title')
                description = self.get_value(col=col, header=header, search_val='description')
                location =  self.get_value(col=col, header=header, search_val='location')
                url = self.get_value(col=col, header=header, search_val='url')

                team = self.get_value(col=col, header=header, search_val='team')
                homeTeam =  self.get_value(col=col, header=header, search_val='homeTeam')
                awayTeam =  self.get_value(col=col, header=header, search_val='awayTeam')
                league =    self.get_value(col=col, header=header, search_val='league')
                round =     self.get_value(col=col, header=header, search_val='round')
                pitch =     self.get_value(col=col, header=header, search_val='pitchType')

                participant_count = self.get_value(col=col, header=header, search_val='participant_count')
                participant_list = self.get_value(col=col, header=header, search_val='participant_list')

                if status == "EDIT":
                    continue
                elif status == "READY":
                    status = "PROCESSING"
                    event = Event(  status=status, date=date, posting_date=posting_date, location=location, type=type,
                                    channel=channel_id, timestamp=timestamp, title=title, description=description,
                                    participant_list=participant_list, participant_count=participant_count,
                                    sheet_row=row,range=range,url=url,
                                    homeTeam=homeTeam, awayTeam=awayTeam, pitch=pitch, league=league, round=round, team=team
                                 )
                    events.append(event)

                else:
                    continue
            sleep(0.1)
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

    def get_value(self, col, header, search_val):

        try:
            val = col[header.index(str(search_val))]
        except:
            #print("Value "+ str(search_val)+ " not found")
            return ""
        return val

    def set_state(self, text):
        for range in par.RANGE_LIST:
            # print("Update Sheet")
            message = []
            val = self.get_sheet_values(range)

            for col in val:
                message.append([text])

            value_range_body = {
                "values": [
                    message
                ]
            }

            value_range_body2 = {

            }
            request = self.service.spreadsheets().values().clear(spreadsheetId=par.SAMPLE_SPREADSHEET_ID,
                                                                 range=range.split("!")[0] + "!A2:A",
                                                                 body=value_range_body2)
            response = request.execute()

            value_input_option = 'USER_ENTERED'
            request = self.service.spreadsheets().values().update(spreadsheetId=par.SAMPLE_SPREADSHEET_ID,
                                                                  range=range.split("!")[0] + "!A2:A",
                                                                  valueInputOption=value_input_option,
                                                                  body=value_range_body)
            response = request.execute()

class sApp:

    def __init__(self):
        print("Slack init")
        if False:
            app.client.chat_postMessage(
                channel=par.TEST_ID,
                text=(
                    "--------------------"+
                    "\n New Test @ "+str(datetime.datetime.today())+
                    "\n-------------------"
                )
            )

    def start_app(self):
        SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

    def get_event_message(self, event):
        message = "no message"
        if event.type == "GAME":
            #if (event.pitch == "Kunstrasen")or(event.pitch == ""):
            if (event.pitch == ""):
                pitch = ""
            else:
                pitch = " auf " + event.pitch

            message = (
                    "*" + event.homeTeam + " : " + event.awayTeam + "* am *"
                    + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date, '%m')
                    + " " + str(datetime.datetime.strftime(event.date, '%H:%M')) + " Uhr*" + pitch + "!\n"
                    + "Treffpunkt um " + str(
                datetime.datetime.strftime(event.date - datetime.timedelta(hours=1), '%H:%M')) + " Uhr - <" + event.url +"|" + event.location+ ">\n"
                    + event.description
            )
        else:
            try:
                title = event.title.split(";")[0]
                extra =  "\n" + event.title.split(";")[1] + "\n"
            except:
                extra = "\n"

            message = (
                    "*" + title + "* am *" + datetime.datetime.strftime(event.date, '%d') + "-" + datetime.datetime.strftime(event.date, '%m')
                    + " um " + str(datetime.datetime.strftime(event.date, '%H:%M')) + " Uhr*" +
                    extra +
                    event.description
            )

        if (event.time_state == "coming up") or (event.time_state == "started"):
            message = message
        elif event.time_state == "finished":
            message = message.replace(event.description,"")
            message = self.strike_out_message(message)
        else:
            message = ""

        return message

    def post_event(self,event):
        print("post event on slack:" + event.time_state)

        message = self.get_event_message(event=event)
        print("Post this on Slack: "+ message)

        if event.channel == "":
            print("Missing channel id!")
            return False

        blocks =  [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }]


        if event.posted is True:
            if event.timestamp != "":
                response = app.client.chat_update(
                    channel=event.channel,
                    ts=event.timestamp,
                    blocks=blocks,
                    text="test",
                    unfurl_links=False
                )
        elif event.posted is False: #TODO: fix scheduling, not getting a timestamp
            try:
                response = app.client.chat_scheduleMessage(
                    channel=event.channel,
                    #post_at= event.posting_date.timestamp(),
                    post_at=datetime.datetime.today().timestamp(),
                    blocks=blocks,
                    text="test",
                    unfurl_links=False
                )
            except:
                #print("time maybe in past")
                response = app.client.chat_postMessage(
                    channel=event.channel,
                    blocks=blocks,
                    text="test",
                    unfurl_links=False
                )
        else:
            print("Cannot post message on Slack: No message id and postedFlag is 'true'")
            return False

        try:
            event.timestamp = response["ts"]
        except:
            print("No message id found!")
            return False

        #print("message_id: "+str(response["ts"]))
        #print("ok: "+ str(response["ok"]))
        success = response["ok"]
        if success is True:
            print("update Sheet")
            #g.update_event_sheet(event)
        return success

    def strike_out_message(self, message):
        try:
            list = message.split("\n")
        except:
            list = []

        msg = ""
        for str in list:
            if str == "":
                break
            msg += "\n~" + str + "~"
        return msg

class teamApp:

    def __init__(self):
        self.events = []

        print("Bot is waking up...")
        # g.set_state("READY")
        self.Sheet_Task(startup=True)

    def updateEvents(self, eventList):
        added = False
        for ev in eventList:
            for e in self.events:
                if(e.range == ev.range) and (e.sheet_row == ev.sheet_row):
                    self.events.remove(e)
                    self.events.append(ev)
                    print("Event updated: \n" + str(ev))
                    ev.update = True
                    added = True
                    break
            if added is False:
                self.events.append(ev)
                print("New event added: \n" + str(ev))
            print("update Sheet")
            # g.update_event_sheet(ev)
        return True

    def Event_Task(self):
        while (1):
            for e in self.events:
                e.update_event()
            sleep(5)

    def Sheet_Task(self,startup=False):
        #startup read events
        if startup is True:
            events_tmp = (g.read_sheet(par.RANGE_LIST))
            self.updateEvents(events_tmp)
            return
        while (1):
            events_tmp = (g.read_sheet(par.RANGE_LIST))
            self.updateEvents(events_tmp)
            sleep(5)

    def Slack_Task(self):
        s.start_app()

    def get_event(self, ts):
        for e in self.events:
            print("Comparing -> " + ts + " | "+ e.timestamp)
            if e.timestamp == ts:
                return e
        return None

    def reaction_event(self, added, user_id, reaction, ts):
        event = self.get_event(ts=ts)
        print("Reaction event: " + reaction + " | " + str(added))
        if event is None:
            print("Event not found")
            return
        if added is True:
            event.reaction_added(user_id=user_id, reaction=reaction)
        else:
            event.reaction_removed(user_id=user_id, reaction=reaction)

s = sApp()
g = gApp()
t = teamApp()