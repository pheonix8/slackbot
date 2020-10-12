import time
import logging
import slackbot_settings
from slack import WebClient
from unleashedBot import Unleashed
from flask import abort, Flask, request
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)


slack_events_adapter = SlackEventAdapter(slackbot_settings.SLACK_SIGNING_SECRET, "/slack/events", app)
slack_web_client = WebClient(slackbot_settings.SLACK_BOT_TOKEN)


def show_unleashed(channel):
    unleashedbot = Unleashed(channel)
    message = unleashedbot.get_message_payload()

    while True:
        slack_web_client.chat_postMessage(**message)
        time.sleep(15)


def is_request_valid(request):
    is_token_valid = request.form['token'] == slackbot_settings.SLACK_VERIFICATION_TOKEN
    is_team_id_valid = request.form['team_id'] == slackbot_settings.SLACK_TEAM_ID

    return is_token_valid and is_team_id_valid


@app.route('/show', methods=['POST'])
def show():
    channel = request.form['channel_id']
    unleashed = Unleashed(channel)
    post = unleashed.get_message_payload()
    if not is_request_valid(request):
        abort(400)

    return slack_web_client.chat_postMessage(**post)


@app.route('/start', methods=['POST'])
def start():
    channel = request.form['channel_id']
    if not is_request_valid(request):
        abort(400)

    return show_unleashed(channel)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0', port=3000)
