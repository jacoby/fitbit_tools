#!/usr/bin/env python

# pull all fitbit data from Fitbit API to MySQL server

# June 20th is my first day with a FitBit. fill in yours

import datetime 
import httplib
import os
import simplejson as json
import time
from oauth import oauth

import fitbit
import mydb

def main():
    date = datetime.datetime( 2012,6,20,1,0,0 )
    now = datetime.datetime.now()
    c = 1
    
    while date < now:
        a = []
        a.append('')
        a.append(str(c))
        a.append(date.strftime("%Y-%m-%d"))
        check = check_day( date )
        if check != 1 :
            insert_day_data( get_day_data( date ) )
        date = date + datetime.timedelta(1)

def check_day( date='' ):
    if date == '' :
        date = datetime.date( 2012,06,20 )
    datestr = date.strftime("%Y-%m-%d")
    db = mydb.Database()
    sql = "SELECT * FROM fitbit_daily WHERE datestamp = %s "
    out = db.db_array( sql , ( datestr ) )
    return len(out)

def insert_day_data( obj ):
    db = mydb.Database()
    sql = "INSERT INTO fitbit_daily ( floors , steps , miles , kilometers , datestamp ) VALUES ( %s , %s , %s , %s , %s )"
    out = db.db_array(sql, ( obj['floors'], obj['steps'], obj['distance_m'], obj['distance_k'], obj['date'] ) )

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
