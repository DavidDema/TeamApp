from __future__ import print_function
import datetime
import os
import os.path
from time import sleep

import par

#Slack import
#from slack_bolt import App
#from slack_bolt.adapter.socket_mode import SocketModeHandler

#Team import
import ics_grabber
from team import Team
from team import Club

#Event import
from event import Event
from event import Game
from event import g
from event import s
#from event import Training

#User import
from user import User
from user import Player


if __name__ == "__main__":
    print("Starting...")
    c = Club("SGS")

    #read_ics = False
    read_ics = False
    read_sheet = True
    post_slack = True
    clear_sheet = True

    update = True
    #write = True

    c.add_events(g.read_sheet(par.EVENTS_RANGE),reboot=True)

    while(1):
        if g.get_sheet_values(par.ADMIN_RANGE)[0][1] == "TRUE":
            print("Programm running")

            if read_ics:
                games = ics_grabber.get_games(par.URL_16)
                read_ics = False
                c.add_events(games)
            if read_sheet:
                events = g.read_sheet(par.ADD_RANGE)
                c.add_events(events)
            if clear_sheet:
                g.clear_sheet()

            if update:
                c.update()
        else:
            print("Program in standby")

        sleep(5)
        #break