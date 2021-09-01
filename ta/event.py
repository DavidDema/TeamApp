import datetime

class Event:
    event_id = 0

    def __init__(self, title, date:datetime, location, duration):

        self.id = Event.get_id()
        self.title = title
        self.date  = date
        self.weekday = self.get_weekday()[0]
        self.weekday_short = self.get_weekday()[1]
        self.location = location
        self.duration = duration

        #Slack API
        self.channel_id = ''
        self.message_id = ''
        self.message_id2 = ''
        self.url = ''

        self.event_state = 'none'
        #upcoming, started, finished
        self.posted = False
        self.preview = False

    def post(self, channel_id):
        self.channel_id = channel_id
        print("Post event on "+channel_id+"!")
        #slack class
        request=app.client.chat_postMessage(
            text=self.getMessage(),
            channel=channel_id
        )
        if request["ok"] is False:
            print("Message not posted: FAIL")
            self.posted = False
            return False
        self.message_id = request['ts']
        self.posted = True
        return True

    def post_preview(self, message_id=""):

        if  self.posted:
            if not self.preview:
                print("Show preview")
                if message_id == "":
                    request = app.client.chat_postMessage(
                        text=self.getMessage("preview"),
                        channel=self.channel_id
                    )
                    message_id = request["ts"]
                else:
                    app.client.chat_update(
                        ts=message_id,
                        channel=self.channel_id,
                        text=self.getMessage("preview")
                    )
                self.preview = True
        return  message_id

    def update(self):
        state_tmp = self.event_state
        # print(
        #     "EvNr:" + datetime.datetime.strftime(self.date,"%M") + "\n" +
        #     "State tmp: " + state_tmp + "\n"
        #     +"State:" + self.get_state()
        # )
        if self.get_state() == state_tmp:
            return
        print("Event updated!")
        if self.event_state == "finished":
            if self.posted:
                app.client.chat_update(
                    ts=self.message_id,
                    channel=self.channel_id,
                    text=self.getMessage("primary over")
                )
                #self.post_preview(delete=True)
        if self.event_state == "upcoming":
            if False:
                print("up")
        if self.event_state == "started":
            if False:
                print("st")

    def get_state(self):
        now = datetime.datetime.today()

        if now < (self.date):
            self.event_state = "upcoming"
        elif now > (self.date+self.duration):
            self.event_state = "finished"
        else:
            self.event_state = "started"

        print(
            "now:\t" + str(now) + "\n" +
            "date:\t" + str(self.date)+ "\n" +
            "state:\t" + self.event_state
        )
        return self.event_state

    def get_weekday(self):
        if self.date.today().weekday() == 0:
            return "Montag","Mo"
        if self.date.today().weekday() == 1:
            return "Dienstag","Di"
        if self.date.today().weekday() == 2:
            return "Mittwoch","Mi"
        if self.date.today().weekday() == 3:
            return "Donnerstag","Do"
        if self.date.today().weekday() == 4:
            return "Freitag","Fr"
        if self.date.today().weekday() == 5:
            return "Samstag","Sa"
        if self.date.today().weekday() == 6:
            return "Sonntag","So"

    def getMessage(self, type="primary"):
        message = "no message"
        if type == "primary":
            message = (
                "Training am *" + self.weekday + ", "
                +datetime.datetime.strftime(self.date, '%d') + "-" + datetime.datetime.strftime(self.date, '%m')
                + "* um " + str(datetime.datetime.strftime(self.date, '%M')) + " Uhr!\n"
                + ":muscle: = SGS07,:punch: = SGS16, :thumbsdown: = Absage!"
            )
        if type == "primary over":
            message = (
                "~Training am *" + self.weekday + ", "
                + datetime.datetime.strftime(self.date, '%d') + "-" + datetime.datetime.strftime(self.date, '%m')
                + "* um " + str(datetime.datetime.strftime(self.date, '%M')) + " Uhr!~\n"
                + "~:muscle: = SGS07,:punch: = SGS16, :thumbsdown: = Absage!~"
            )
        if type == "preview":
            message = (
                "---------------------------------------------\n"+
                "---------------------------------------------\n"+
                "N\"achstes Training am *" + self.weekday + ", "
                + datetime.datetime.strftime(self.date, '%d') + "-" + datetime.datetime.strftime(self.date, '%m')
                + "* um " + str(datetime.datetime.strftime(self.date, '%M')) + " Uhr!"
            )
        return message
    def __str__(self):

        message = str(self.event_id) + "| " + str(self.title) + " @ " + str(self.location) + "\n\t"\
                  +datetime.datetime.strftime(self.date, "%D") + " at " + datetime.datetime.strftime(self.date, "%m") + " o'clock" + "\n\t"\
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


    def __init__(self, title,date,location,duration):
        super().__init__(title="",date="", location="", duration=datetime.timedelta(hours=1, minutes=45))
