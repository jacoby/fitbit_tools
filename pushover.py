#!/usr/bin/env python

'''

Module to send Pushover messages in Python

usage:
    pu = pushover.pushover()
    pu.send_message( message )

'''

import os, httplib , urllib
import yaml

class pushover:
    TOKEN = '' ,
    USER  = '' ,
    def __init__(self, myyaml = os.environ['HOME'] + '/.pushover.yml'):
        c = open( myyaml , 'r' )
        c_yaml = c.read()
        c_obj = yaml.load(c_yaml)
        self.TOKEN = c_obj['token']
        self.USER = c_obj['user']
    def send_message(self,message):
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urllib.urlencode({
                        "token": self.TOKEN ,
                        "user": self.USER,
                        "message": message ,
                        }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

