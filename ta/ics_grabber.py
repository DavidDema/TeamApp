from ics import Calendar
import requests
import datetime

from event import Event
from event import Game
import par

test_url = "https://fussballoesterreich.at/netzwerk/icalendar/670725461856634215_485215725~1165862735024510172-T-x.ics"
url_07 = "https://fussballoesterreich.at/netzwerk/icalendar/670725461856634215_485215725~665233077005870945-T-x.ics"

class Cal:
    def __init__(self, url, test=False):
        self.url    = url

        self.c = Calendar(requests.get(self.url).text)
        self.events = list(self.c.timeline)

        if not test:
            self.games = self.addGames(self.events)
        else:
            for e in self.events:
                print(e)


    def addGames(self, eventsDates):
        games = []
        for e in eventsDates:
            homeTeam, awayTeam = self.convertTitle(e.name)
            league, round_nr = self.convertDescription(e.description)
            #date = e.begin.arrowObj = arrow.get('2014-10-09T10:56:09.347444-07:00')

            date=datetime.datetime.strptime(str(e.begin),par.TIME_FORMAT)
            date = date.replace(tzinfo=None)

            game = Game(
                title= homeTeam + " : " + awayTeam,date=date,location=e.location,
                url=e.url,homeTeam=homeTeam, awayTeam=awayTeam,league=league, round=round_nr)

            game.channel_id = par.get_channel_id("test")
            games.append(game)
        return games

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


def get_games(ics_url):
    games=[]
    c = Cal(ics_url)
    return c.games

if __name__ == "__main__":

    test = 2
    print("ICS grabber test " + str(test) + "")

    if test == 0:
        Cal(url=test_url, test=True)
    if test == 1:
        cal_t1 = Cal(test_url)
        for g1 in cal_t1.games:
            print(g1)
    elif test == 2:
        games = get_games(test_url)
        for g2 in games:
            print(g2)
    print("ics grabber test finished!")