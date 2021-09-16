from __future__ import print_function
from time import sleep
import time
import threading

import par

#Event import
from event import t



if __name__ == "__main__":

    if True:
        x = threading.Thread(target=t.Sheet_Task, args=())
        y = threading.Thread(target=t.Event_Task, args=())
        z = threading.Thread(target=t.Slack_Task, args=())

        #y.start()
        x.start()
        y.start()
        z.start()

        x.join()
        y.join()
        z.join()


#TODO:
# -> Fix problem with Google Api
# -> Reaction removed doesnt work
# -> Implement error handling
# -> Implement preview of upcoming event
# -> Implement classes for Game and Training
# -> Classes Game,Training,Team,Club,User,Player
