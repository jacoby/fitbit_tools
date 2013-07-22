#!/usr/bin/env python

# I don't have an Aria scale, so I track my weight manually and use
# this script to upload the data to FitBit

import datetime
import httplib
import os
import simplejson as json
import time
from oauth import oauth

import fitbit
import mydb

def main():
    fb = fitbit.make_class()
    db = mydb.Database( 'csoc' )
    sql = "select weight from weight where CURRENT_DATE = DATE(date)"
    out = db.db_array( sql , )
    if len(out) > 0 :
        weight = out[-1][-1] 
        response = fb.log_body_weight( weight )
        if response['weightLog'] :
            a = 1
        else:
            print response

if __name__ == '__main__':
    main()
