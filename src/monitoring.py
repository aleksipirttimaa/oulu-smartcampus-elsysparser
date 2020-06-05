import json
# -*- coding: utf-8 -*-

class MonLog:
    '''
    Monitoring Log object repserents the history of the app.
    Currently it is used to publish periodic status messages to the broker.
    '''
    def __init__(self):
        self.n_success = 0
        self.n_fail = 0

    def __str__(self):
        return json.dumps(self.__dict__)