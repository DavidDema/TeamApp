import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import par

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.event("reaction_added")
def ask_for_introduction(event, say):
    print("message_changed event")
    welcome_channel_id = par.SPIELE07_ID
    user_id = event["user"]
    text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel."
    say(text=text, channel=welcome_channel_id)

@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        text=
        "hello"
    )

SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()