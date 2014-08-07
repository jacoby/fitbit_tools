#!/usr/bin/env python

# One of the first things I wrote against the fitbit API, showing
# the battery status.

import datetime 
import httplib
import os
import simplejson as json
import time
from oauth import oauth

import fitbit
import pushover as p 

def main():
    fb = fitbit.make_class()
    devices = fb.devices_json()
    device = devices[0]
    battery = device['battery']
    pu = p.pushover()
    pu.send_message( 'Current Battery Status: ' + battery )
if __name__ == '__main__':
    main()
