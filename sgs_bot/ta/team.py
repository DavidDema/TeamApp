import par
from event import Event
from event import Game
from event import Training
from event import g

class Club:

    def __init__(self, name):
        self.name = name

        self.events = []
        self.games = []
        self.trainings = []

    def get_event_ID(self):
        return len(self.events)+1

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

        #add to list and set ID for event
        event.id = self.get_event_ID()
        list.append(event)
        self.events.append(event)

        if not reboot:
            event.updated = True

    def add_events(self, events,reboot=False):
        add = True
        for e in events:
            add = self.check_equal_event(e)
            if add:
                print("add new event")
                self.add_event(event=e, reboot=reboot)
        return

    def check_equal_event(self, event:Event):
        add = True
        for ev in self.events:
            if event.title == ev.title:
                add = False

                if (event.date != ev.date):
                    ev.update_data(event)
                    add = False
                    break
        return add