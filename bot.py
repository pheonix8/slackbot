import requests
import slackbot_settings
import requests.auth
import binascii
import hashlib
import hmac

api_key = slackbot_settings.API_KEY
api_id = slackbot_settings.API_ID


class UnleashedAPI(requests.auth.AuthBase):
    def __init__(self):
        self.api_key = api_key.encode('utf-8')
        self.api_id = api_id
        self.api_url = 'https://api.unleashedsoftware.com'

    def get_query(self, url):
        parts = url.split('?')
        if len(parts) > 1:
            return parts[1]
        else:
            return ""

    def __call__(self, r):
        query = self.get_query(r.url)

        hashed = hmac.new(self.api_key, query.encode('utf-8'), hashlib.sha256)
        signature = binascii.b2a_base64(hashed.digest())[:-1]
        r.headers['api-auth-signature'] = signature
        r.headers['api-auth-id'] = self.api_id
        return r

    def _get_request(self, method, params=None):
        params = params or {}
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
        }
        resp = requests.get(
            self.api_url + '/' + method,
            headers=headers,
            params=params,
            auth=self
        )
        return resp

    def get_StockOnHand(self):
        resp = self._get_request('StockOnHand')
        json_parsed = resp.json()
        array = []
        code = []
        hand = []
        items = json_parsed['Items']
        for i in items:
            pc = i['ProductCode']
            qoh = i['QtyOnHand']
            code.append(pc)
            hand.append(qoh)
        array.append(code)
        array.append(hand)
        return array

    def get_ProductAlert(self):
        resp = self._get_request('Products')
        json_parsed = resp.json()
        array = []
        code = []
        al = []
        items = json_parsed['Items']
        for i in items:
            pc = i['ProductCode']
            minal = i['MinStockAlertLevel']
            if minal == None:
                minal = 0.0
            code.append(pc)
            al.append(minal)
        array.append(code)
        array.append(al)
        return array

    def convert(self):
        array = self.get_StockOnHand()
        array2 = self.get_ProductAlert()
        lenght = list(range(len(array2[0])))
        for i in lenght:
            if array2[0][i] != array[0][i]:
                name = str(array2[0][i])
                array[0].insert(i, name)
                array[1].insert(i, 0.0)
        return array


if __name__ == '__main__':
    unleashedAPI = UnleashedAPI()
    products = unleashedAPI.get_StockOnHand()
    alert = unleashedAPI.get_ProductAlert()
    test = unleashedAPI.convert()
    print(alert)
    print(products)
    print(test)
