

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
        print("update")

class Team:


    def __init__(self, name):
        self.name = name