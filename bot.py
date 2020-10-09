import requests

URL_SLACK = 'webhook'
data = {'text': 'Hello'}
requests.post(URL_SLACK, json=data)
