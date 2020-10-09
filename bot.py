import requests

URL_SLACK = 'https://hooks.slack.com/services/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'
data = {'text': 'Hello'}
requests.post(URL_SLACK, json=data)
