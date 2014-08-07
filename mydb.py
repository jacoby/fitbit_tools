#!/usr/bin/env python

# wrapper to MySQL library, hiding most of the complexity.

# needs a little work, especially to remove the hardcoded "myyaml"
# file location

import sys
import yaml
import MySQLdb as db

class Database:
    config = ''
    def __init__( self , client="default" ):
        myyaml = '/home/jacoby/.my.yaml'
        c = open( myyaml , 'r' )
        c_yaml = c.read()
        c_obj = yaml.load(c_yaml)
        clients = c_obj[ "clients" ]
        self.user = clients[client]["user"]
        self.database = clients[client]["database"]
        self.password = clients[client]["password"]
        self.host = clients[client]["host"]
        self.con = db.connect(self.host, self.user,
                              self.password, self.database)

    def db_do( self , query='' , values=[] ):
        if ( len(query) > 0 ):
            with self.con:
                cur = self.con.cursor()
                cur.execute( query , values )
                numrows = int(cur.rowcount)
                return numrows

    def db_array( self , query='' , values=[] ):
        if ( len(query) > 0 ):
            output = []
            with self.con:
                cur = self.con.cursor()
                if len( values ) > 0 :
                    cur.execute( query , values )
                else:
                    cur.execute( query )
                numrows = int(cur.rowcount)
                for i in range( numrows ):
                    row = cur.fetchone()
                    output.append(row)
            return output

