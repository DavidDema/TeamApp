import datetime
import os
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

dateList = []
numweeks = 13

@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    for d in dateList:
        channel_id = 'C1U1T1L31'
        if (d.weekday() == 0):
            wd = "Montag"
            ls = "\n*Laufschuhe mitnehmen!*"
        else:
            wd = "Donnerstag"
            ls = ""
        say(text=
            "Training am *" + wd + ", " + datetime.datetime.strftime(d, '%d') + "-" + datetime.datetime.strftime(d,
                                                                                                                 '%m') + "* um " + str(
                datetime.datetime.strftime(d, '%H')) + " Uhr!\n" +
            ":muscle: = SGS07,:punch: = SGS16, :thumbsdown: = Absage!" +
            ls,
            channel=channel_id
            )

if __name__ == "__main__":

    startdate = datetime.datetime(year=2021, month=9, day=6, hour=20)

    t1 = startdate
    t2 = t1 + datetime.timedelta(days=3)


    for x in range(0, numweeks):
        dateList.append(t1 + datetime.timedelta(days=x*7))
        dateList.append(t2 + datetime.timedelta(days=x*7))
    print(dateList)

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()