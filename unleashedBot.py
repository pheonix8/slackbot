class Unleashed:
    """Constructs the message"""

    TEST_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "hello"
            ),
        },
    }

    def __init__(self, channel):
        self.channel = channel
        self.username = "unleashedbot"
        self.icon_emoji = ":robot_face:"

    def get_message_payload(self):
        return {
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.TEST_BLOCK,
            ],
        }
