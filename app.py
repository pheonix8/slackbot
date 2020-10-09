import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from unleashedBot import Unleashed
import slackbot_settings

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(slackbot_settings.SLACK_SIGNING_SECRET, "/slack/events", app)

slack_web_client = WebClient(slackbot_settings.SLACK_BOT_TOKEN)

unleashed_sent = {}


def show_unleashed(user_id: str, channel: str):
    unleashedbot = Unleashed(channel)

    message = unleashedbot.get_message_payload()

    response = slack_web_client.chat_postMessage(**message)

    if channel not in unleashed_sent:
        unleashed_sent[channel] = {}
    unleashed_sent[channel][user_id] = unleashedbot


@slack_events_adapter.on("message")
def onboarding_message(payload):
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")

    show_unleashed(user_id, channel_id)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
