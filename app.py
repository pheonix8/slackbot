import time
import logging
from flask import Flask
import slackbot_settings
from slack import WebClient
from unleashedBot import Unleashed
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(slackbot_settings.SLACK_SIGNING_SECRET, "/slack/events", app)
slack_web_client = WebClient(slackbot_settings.SLACK_BOT_TOKEN)


def show_unleashed(channel):
    unleashedbot = Unleashed(channel)

    message = unleashedbot.get_message_payload()

    while True:
        slack_web_client.chat_postMessage(**message)
        time.sleep(100)


def talk(channel):
    unleashedbot = Unleashed(channel)

    directmessage = unleashedbot.get_message_payload()

    slack_web_client.chat_postMessage(**directmessage)


@slack_events_adapter.on("message")
def directtalk(payload):
    event = payload.get("event", {})

    text = event.get("text")

    if "hi" in text.lower():
        channel_id = event.get("channel")
        return talk(channel_id)


@slack_events_adapter.on("member_joined_channel")
def startUnleashed(payload):
    event = payload.get("event", {})

    test = event.get("user")

    if test == "U01CNLCRAJV":
        channel_id = event.get("channel")
        return show_unleashed(channel_id)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0', port=3000)
