from __future__ import print_function
import datetime
import os
import os.path
from time import sleep

#Google import

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

#Slack import
#from slack_bolt import App
#from slack_bolt.adapter.socket_mode import SocketModeHandler

#Team import
from team import Team
from team import Club

#Event import
from event import Event
from event import Game
#from event import Training

#User import
from user import User
from user import Player

SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/calendar']

        # The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BsbelcuvmYAZsBWTr1-BfuxXHK_zPws6QIpdNmk_7hE'
ADMIN_RANGE = "admin!A1:B"
EVENTS_RANGE = "events!A2:D"

class gApp:


    def __init__(self):

        SAMPLE_RANGE_NAME = 'events!A2:C'

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

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        self.sheet = service.spreadsheets()
        self.ranges = []

    def get_sheet_value(self, range, col, row):
        result = self.sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                         range=range).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return None
        else:
            #print("Found value:" + str(values[col][row]))
            return values[col][row]

    def update_sheet_value(self, range, row, col, text):
        print("Change value")
        self.sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=range,
            value=None
        )

if __name__ == "__main__":
    print("Starting...")

    g = gApp()
    while(1):
        if g.get_sheet_value(ADMIN_RANGE, 0, 1) == "TRUE":
            print("Programm running")

        else:
            print("Program in standby")

        sleep(2)
