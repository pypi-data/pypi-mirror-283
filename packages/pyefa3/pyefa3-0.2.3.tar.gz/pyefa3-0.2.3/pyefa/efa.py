import os
from .triprequest import TripRequest
import urllib.request
import urllib.parse


class EFA(TripRequest):

    def __init__(self):
        super().__init__()
        self.debug = False

    def submit(self, url: str, post_data: dict, outputtype: str):
        post_data.update({'outputFormat': outputtype, 'coordOutputFormat': 'WGS84'})
        if self.debug and os.path.isfile(f'cache.{outputtype}'):
            return open(f'cache.{outputtype}', 'r').read()

        post_data["name_destination"] = urllib.parse.quote(post_data["name_destination"])
        data = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req).read().decode('utf-8')

        if self.debug:
            open(f'cache.{outputtype}', 'w').write(response)
        return response
