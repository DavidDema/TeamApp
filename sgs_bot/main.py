from __future__ import print_function
from time import sleep
import asyncio
import time

import par
from team import Club

#Event import
from event import Event
from event import g
from event import s


# async def Sheet():
#     while (1):
#         for e in events16:
#             e.update()
#         await asyncio.sleep(5)
#
#
# async def Slack():
#     while (1):
#         s.start_app()
#         await asyncio.sleep(5)
#
# async def main():
#     print(f"started at {time.strftime('%X')}")
#
#     await Slack()
#     await Sheet()
#
#     print(f"finished at {time.strftime('%X')}")


if __name__ == "__main__":
    print("Bot is waking up...")

    events16 = g.read_sheet(par.SPIELE16_RANGE)
    events07 = g.read_sheet(par.SPIELE07_RANGE)
    trainings = g.read_sheet(par.TRAININGS_RANGE)

    # for e in events16:
    #     print(e)
    #     s.post_event(e)

    #asyncio.run(main())

    while (1):
        for e in events16:
            e.update()
        for e in events07:
            e.update()
        for e in trainings:
            e.update()
        sleep(5)

    #TODO:
    #create Tasks: Slack Listener, App manager, Sheet manager
    #listen to Reactions and count participants for event

    #create ICS to Sheet converter, with "ü"
    #

    #install on Google Cloud


    # for e in events07:
    #     print(e)
    #     s.post_event(e)
    # for e in trainings:
    #     print(e)
    #     s.post_event(e)


