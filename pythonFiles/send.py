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
    g = c07.games[3]
    say(
        text=
        "*<" + g.url2 + "|" + g.homeTeam + ":" + g.awayTeam + ">*"
        ""
    )

class Cal:
    def __init__(self, url, id):
        self.url    = url
        self.id     = id

        self.c = Calendar(requests.get(self.url).text)
        self.events = list(self.c.timeline)
        self.name = "SGS" + str(self.id)

        self.games = self.addGames(self.events)

        #print(c16.events[2].extra[2].value)
        #to get extra values from list

    def addGames(self, eventList):
        g = []
        for e in eventList:
            homeTeam, awayTeam = self.convertTitle(e.name)
            if (homeTeam or awayTeam) == "":
                print("Event \"" + e.name + "\" is not a game")
                continue
            league, round_nr = self.convertDescription(e.description)
            g_tmp = Game(homeTeam, awayTeam, e.begin, e.duration,e.location, self.id, e.url, league, round_nr)
            g.append(g_tmp)

        print("Calendar \""+self.name+"\": "+ str(len(g)) +" games added\n")
        return g

    def convertDescription(self,d):
        if "(" not in d:
            return d,""
        tmp = d.split("(")
        league = tmp[0]
        round_nr = tmp[1].replace(")", "")
        return league, round_nr

    def convertTitle(self,text):
        if ":" not in text:
            print("Event title is not normal for a game:"+text)
            return "",""
        tmp = text.split(" : ")
        homeTeam = tmp[0]
        awayTeam = tmp[1]

        return homeTeam, awayTeam

class Event:
    def __init__(self, title, date, location, duration, slack_channel, url):
        self.title = title
        self.date= date
        self.location = location
        self.duration = duration

        self.slack_channel = slack_channel
        self.posted = 0
        self.updated = 0
        self.url = url

class Game(Event):

    def __init__(self,homeTeam, awayTeam, date, location, duration, slack_channel, url, league, round_nr):
    #def __init__(self, homeTeam, awayTeam, date,duration,location, slack_channel, league, round_nr):
        super().__init__(homeTeam+":"+awayTeam, date, location, duration, slack_channel, url)
        self.homeTeam   = homeTeam
        self.awayTeam   = awayTeam
        self.league     = league
        self.round_nr   = round_nr

    def __str__(self):
        title = self.homeTeam + " vs " + self.awayTeam + "\n" + self.url
        subtitle = str(self.date) + "\n"
        return title + subtitle

class Training(Event):

    def __init__(self,title, date, location, duration, slack_channel, teams):
    #def __init__(self, homeTeam, awayTeam, date,duration,location, slack_channel, league, round_nr):
        super().__init__(title, date, location, duration, slack_channel, url= "")
        self.teams = teams
        self.running = 0

    def __str__(self):
        title = self.title + "\n"
        subtitle = str(self.date) + "\n"
        return title + subtitle

class TeamApp:
    def __init__(self):
        #SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
        print("init ok")

    def postEvents(self, events):
        print("Posting "+str(len(events))+"events")
        for e in events:
            if isinstance(e, Game):
                self.postGame(e)
            else:
                self.postEvent(e)

    def postEvent(self, event):
        print("Post event \""+ event.title +"\"on Slack Channel \"" + event.slack_channel + "\"")

    def postGame(self, event):
        print("Post game \""+ event.title +"\"on Slack Channel \"" + event.slack_channel + "\"")

if __name__ == "__main__":

    c16 = Cal(url_16, "16")
    c07 = Cal(url_07, "07")


    #for g in c16.games:
    #    print(g)

    myApp = TeamApp()
    myApp.postEvents(c16.games)

