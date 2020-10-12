from bot import UnleashedAPI


class Unleashed:
    """Constructs the message"""

    START_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "*Stock on Hand:*"
            ),
        },
    }

    def __init__(self, channel):
        self.channel = channel
        self.username = "unleashedbot"

    def build_block(self):
        unleashed = UnleashedAPI()
        products = unleashed.convert()
        alert = unleashed.get_ProductAlert()
        out = self.evaluate_alert(products, alert)
        print(out)
        test = str(out)
        text = (
                test + "\n"
                       "*Login:* https://au.unleashedsoftware.com/v2/Account/LogOn"
        )
        return self._get_block(text)

    def get_message_payload(self):
        return {
            "channel": self.channel,
            "username": self.username,
            "blocks": [
                self.START_BLOCK,
                *self.build_block()
            ],
        }

    @staticmethod
    def evaluate_alert(product, alert):
        alertandstock = ""
        length = list(range(len(alert[0])))
        for i in length:
            name = str(alert[0][i])
            stock = str(product[1][i])
            if alert[1][i] > product[1][i]:
                alertandstock = alertandstock + name + ":  " + stock + ",  :exclamation: \n"
            else:
                alertandstock = alertandstock + name + ":  " + stock + ",  :heavy_check_mark: \n"
        return alertandstock

    @staticmethod
    def _get_block(text):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        ]
