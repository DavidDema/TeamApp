import datetime
import os
from time import sleep

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

dateList = []
numweeks = 5

eventList = []





def initDates():
    #startdate = datetime.datetime(year=2021, month=8, day=31, hour=21, minute=30)
    startdate = datetime.datetime.today()+datetime.timedelta(minutes=5)
    print("Starttime:"+ str(startdate))
    t1 = startdate

    for x in range(0, numweeks):
        dateList.append(t1 + datetime.timedelta(minutes=x * 3))
        print("Time" + str(dateList[x]))

    for d in dateList:
        eventList.append(Event(title="Training", date=d, location="Red Star Auto (1160 Wien)", duration=datetime.timedelta(minutes=2)))
    print(str(len(dateList)) + " Training Events added !\n")


def find_closest_event(events):

    dates = []
    for e in events:
        dates.append(e.date)
    date1 = min(dates, key=lambda d: abs(d - datetime.datetime.today()))
    for e in events:
        if e.date == date1:
            return e
    return None

if __name__ == "__main__":
    app.client.chat_postMessage(
        channel='C022A67PNQ5',
        text="---------------------"
    )

    initDates()
    for e in eventList:
        e.post('C022A67PNQ5')
        print(e)

    ts = ""
    while(1):
        for e in eventList:
            e.update()

        sleep(5)
        closest_event = find_closest_event(eventList)

        ts = closest_event.post_preview(message_id=ts)


    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


# class Game(Event):
#
#     def __init__(self,homeTeam, awayTeam, date, location, duration, league, round_nr):
#         super().__init__(homeTeam+":"+awayTeam, date, location, duration)
#         self.homeTeam   = homeTeam
#         self.awayTeam   = awayTeam
#         self.league     = league
#         self.round_nr   = round_nr
#
#     def __str__(self):
#         title = self.homeTeam + " vs " + self.awayTeam + "\n" + self.url
#         #subtitle = str(super.date) + "\n"
#         return title# + subtitle