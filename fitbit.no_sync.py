#!/usr/bin/env python

# check last three days' worth of data from the fitbit site.
# if steps == 0 for all three days, send pushover message.


import datetime 
import httplib
import os
import simplejson as json
import time
from oauth import oauth

import fitbit
import mydb
import pushover as p

def main():
    now = datetime.datetime.now()
    total = 0 
    for i in range(0,3):
        date = now.strftime("%Y-%m-%d")
        data = get_day_data( now )
        total = total + data['steps']
        now = now - datetime.timedelta(1)
    if total == 0:
        message = "You have not reported data over the last 3 days. Check your FitBit."
        pu = p.pushover()
        pu.send_message( message )

def get_day_data( date='' ):
    if date == '' :
        date = datetime.date( 2012,06,20 )
    # start is june 20 2012
    weekdays = ( 'Mon' , 'Tue' , 'Wed' , 'Thu' , 'Fri' , 'Sat' , 'Sun' ) 
    data = {}
    datestr = date.strftime("%Y-%m-%d")
    fb = fitbit.make_class()
    fbr = fb.activities_date_json( datestr )
    summary         = fbr['summary']
    distances       = summary['distances']
    data['date']    = datestr
    data['floors']  = summary['floors']
    data['steps']   = summary['steps']
    data['distance_k'] = 0
    
    for d in distances:
        activity = d['activity']
        if activity == 'total':
            data['distance_k'] = d['distance']
    data['distance_m'] = "%.02f" % ( data['distance_k'] * 0.621371 )
    data['distance_k'] = "%.02f" % data['distance_k'] 
    return data

if __name__ == '__main__':
    main()
