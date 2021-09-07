import par
from event import Event
from event import Game
from event import Training
from event import g

class Club:

    def __init__(self, name):
        self.name = name

        self.teams = []
        self.events = []
        self.games = []
        self.trainings = []

        # SHEETS
        self.sheet_id = ""
        self.e_sheet_range = ""
        self.g_sheet_range = ""
        self.t_sheet_range = ""

        # SLACK
        self.e_channel_id = ""
        self.g_channel_id = ""
        self.t_channel_id = ""

    def add_team(self, team):
        try:
            self.teams.append(team)
        except():
            print("Team not added!")

    def update(self):
        for e in self.events:
            e.update()

    def add_event(self, event, reboot=False):
        if isinstance(event,Game):
            list = self.games
        elif isinstance(event,Training):
            list = self.trainings
        elif isinstance(event,Event):
            list = []
        else:
            print("cannot add event: no event "+ str(type(event)))
            return
        list.append(event)
        self.events.append(event)
        if not reboot:
            g.update_sheet_value(event)

    def add_events(self, events,reboot=False):
        add = True
        for e in events:
            add = self.check_equal_event(e)
            #add = True
            if add:
                print("add new event")
                self.add_event(event=e, reboot=reboot)
        return

    def check_equal_event(self, event:Event):
        add = True
        for ev in self.games:
            if event.title == ev.title:
                add = False

                if (event.date != ev.date):
                    ev.update_data(event)
                    add = False
                    break
        return add

class Team:

    def __init__(self, name):
        self.name = name