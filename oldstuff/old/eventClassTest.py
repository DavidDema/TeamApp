import datetime

default_channel = "default"
training_channel = "training"

dateList = []
numweeks = 13
eventList = []

class Event:
    eventCount = 0

    def __init__(self,title,date,duration=1,location="",channel_id=default_channel):
        self.id = Event.getID()
        self.title = title
        self.date  = date
        self.location = location

        self.channel_id = channel_id

        self.posted = False
        self.event_past = self.is_past()

        #self.type

    def is_past(self):
        if datetime.datetime.today()>self.date:
            return True
        else:
            return False

    def is_posted(self):
        return self.posted

    def equal(self):


    def __str__(self):
        tmp1 = str(self.id) + "|Event \"" + self.title+ "\" at " + str(self.date) + \
                "\n\tpost on channel \"" + self.channel_id + "\"" + \
                "\n\tpassed: " + str(self.is_past()) + "\n\tposted: " + str(self.posted)

        return tmp1


    @staticmethod
    def getID():
        Event.eventCount += 1
        return Event.eventCount

if __name__ == "__main__":

    startdate = datetime.datetime(year=2021, month=9, day=6, hour=20)

    t1 = startdate
    t2 = t1 + datetime.timedelta(days=3)

    for x in range(0, numweeks):
        e1 = Event(title="Training",date=t1 + datetime.timedelta(days=x*7), location="Red Star Auto", channel_id=training_channel)
        e2 = Event(title="Training",date=t2 + datetime.timedelta(days=x*7), location="Red Star Auto", channel_id=training_channel)
        eventList.append(e1)
        eventList.append(e2)
    print(eventList[3])