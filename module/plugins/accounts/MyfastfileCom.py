# -*- coding: utf-8 -*-

import time

from module.common.json_layer import json_loads
from module.plugins.internal.Account import Account


class MyfastfileCom(Account):
    __name__    = "MyfastfileCom"
    __type__    = "account"
    __version__ = "0.08"
    __status__  = "testing"

    __description__ = """Myfastfile.com account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("stickell", "l.stickell@yahoo.it")]


    def grab_hosters(self, user, password, data):
        json_data = self.load("http://myfastfile.com/api.php", get={'hosts': ""})
        self.log_debug("JSON data", json_data)
        json_data = json_loads(json_data)

        return json_data['hosts']

    def grab_info(self, user, password, data):
        if 'days_left' in self.json_data:
            validuntil = time.time() + self.json_data['days_left'] * 24 * 60 * 60
            return {'premium': True, 'validuntil': validuntil, 'trafficleft': -1}
        else:
            self.log_error(_("Unable to get account information"))


    def signin(self, user, password, data):
        #: Password to use is the API-Password written in http://myfastfile.com/myaccount
        html = self.load("https://myfastfile.com/api.php",
                         get={'user': user,
                              'pass': password})

        self.log_debug("JSON data: " + html)

        self.json_data = json_loads(html)
        if self.json_data['status'] != 'ok':
            self.log_error(_('Invalid login. The password to use is the API-Password you find in your "My Account" page'))
            self.fail_login()
