#!/usr/bin/env python

# creates sparkline of the steps I've recorded over the last seven days.

import datetime 
import httplib
import os
import simplejson as json
import time
from oauth import oauth

import spark
import mydb

def main():
    itap = mydb.Database( 'itap' )
    select = """
SELECT
    steps steps ,
    datestamp date,
    DATE_FORMAT( datestamp , "%Y" ) year ,
    YEARWEEK(datestamp) month ,
    DATE_FORMAT( datestamp , "%a" ) day 
FROM fitbit_daily
ORDER BY datestamp
DESC LIMIT 7
"""
    data = itap.db_array(select)
    steps = []
    reverse = []
    for row in data:
        step = row[0]
        steps.append( step )
        reverse.insert( 0 , step )
    stepspark = spark.spark( reverse )
    print stepspark

if __name__ == '__main__':
    main()
