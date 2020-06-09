import json
from time import time
# -*- coding: utf-8 -*-

class MonLog:
    '''
    Monitoring Log object repserents the history of the app.
    It is used to publish periodic status messages to the broker.
    '''
    def __init__(self):
        self.n_success = 0
        self.n_delta_success = 0
        self.n_fail = 0
        self.n_delta_fail = 0
        self._n_success_prev = 0
        self._n_fail_prev = 0
        self._time_last_allow = 0

    def __str__(self):
        # delta = current - previous
        self.n_delta_success = self.n_success - self._n_success_prev
        self.n_delta_fail = self.n_fail - self._n_fail_prev
        return json.dumps({"n_success": self.n_success,
                           "n_delta_success": self.n_delta_success,
                           "n_fail": self.n_fail,
                           "n_delta_fail": self.n_delta_fail
                        })

    def allow(self):
        now = time()
        if self._time_last_allow == 0 or self._time_last_allow + 30 < now:
            self._time_last_allow = now
            return True
        return False
