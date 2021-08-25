import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Install the Slack app and get xoxb- token in advance
# SET SLACK_BOT_TOKEN=xoxb-2078205375157-2081356491730-n5cw6wKuK1I1UqI7WQ5VxKMz
# SET SLACK_APP_TOKEN=xapp-1-A0226FG1886-2081523690947-edea07a85b487d80d9ea4db1cac39e38cfd7a09d4bb41ccd06f089f7f8a6d3fb

app = App(token=os.environ["SLACK_BOT_TOKEN"])

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()