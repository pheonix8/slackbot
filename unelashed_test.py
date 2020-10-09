import time
import slackbot_settings
from slack import WebClient
from unleashedBot import Unleashed

slack_web_client = WebClient(slackbot_settings.SLACK_BOT_TOKEN)

unleashedBot = Unleashed("#test")

message = unleashedBot.get_message_payload()

while True:
    slack_web_client.chat_postMessage(**message)
    time.sleep(3600)
