from ics import Calendar
import requests
import datetime
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

url_16 = "https://fussballoesterreich.at/netzwerk/icalendar/670725461856634215_485215725~1165862735024510172-T-x.ics"
url_07 = "https://fussballoesterreich.at/netzwerk/icalendar/670725461856634215_485215725~665233077005870945-T-x.ics"

@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "See Games"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    #say(f"<@{body['user']['id']}> clicked the button")
    #say(c16.game[3])
    say("Hello")


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
            g_tmp = Game(homeTeam, awayTeam, e.begin, e.duration,e.location, self.id, e.url, league, round_nr)
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
        Event(homeTeam+":"+awayTeam, date, location, duration, slack_channel, url)
        self.homeTeam   = homeTeam
        self.awayTeam   = awayTeam
        self.league     = league
        self.round_nr   = round_nr
        self.url2 = url

    def __str__(self):
        title = self.homeTeam + " vs " + self.awayTeam + "\n" + self.url2
        #subtitle = str(super.date) + "\n"
        return title# + subtitle

if __name__ == "__main__":
    c16 = Cal(url_16, "16")
    #c07 = Cal(url_07, "07")
    #for g in c16.games:
    #    print(g)
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()