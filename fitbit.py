#!/usr/bin/env python

'''

https://wiki.fitbit.com/display/API/Fitbit+API

Probably don't need the hashbang here. Leaving it anyway.

This is a module that creates a FitBit access class. This is the most
in-depth Python coding I've ever written.

This is based on sample code I found in a forum online, so I pass on this
code with as much restriction as I received it with: none at all.

usage:
    fitbit = p_class.make_class()
    print fitbit.devices_json()
    print fitbit.profile_json()
    print fitbit.dated_activities_json()

Questions or comments? jacoby.david <at> gmail <dot> com,
or leave a comment on the gist

'''

import datetime
import os, httplib
import re
import simplejson as json
import urllib
import yaml
from oauth import oauth

class FitBit:
    SERVER = 'api.fitbit.com'
    REQUEST_TOKEN_URL = 'https://%s/oauth/request_token' % SERVER
    ACCESS_TOKEN_URL  = 'https://%s/oauth/access_token' % SERVER
    AUTHORIZATION_URL = 'https://%s/oauth/authorize' % SERVER
    def __init__(self,consumer_key,consumer_secret,default,tokens):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.default = default
        self.tokens = tokens
    def get_key(self):
        return self.consumer_key
    def get_secret(self):
        return self.consumer_secret
    def get_tokens(self):
        return self.tokens.keys()
    def get_token_info(self,key=''):
        if (key==''):
            key = self.default
        return self.tokens[key]
    def get_token(self,key=''):
        if (key==''):
            key = self.default
        return self.tokens[key]['access_token']
    def get_token_secret(self,key=''):
        if (key==''):
            key = self.default
        return self.tokens[key]['access_token_secret']
    def get_token_string(self,key=''):
        if (key==''):
            key = self.default
        return "oauth_token_secret=" + self.tokens[key]['access_token_secret'] + "&oauth_token=" + self.tokens[key]['access_token']

    def do_oauth( self ):
        apiCall = '/oauth/request_token'
        return self.__make_api_call_json( apiCall )

    def devices_json(self):
        apiCall = '/1/user/-/devices.json'
        return self.__make_api_call_json( apiCall )
    def profile_json(self):
        apiCall = '/1/user/-/profile.json'
        return self.__make_api_call_json( apiCall )
    def recent_activities_json(self):
        apiCall = '/1/user/-/activities/recent.json'
        return self.__make_api_call_json( apiCall )
    def activities_date_json(self,date='NONE'):
        if date=='NONE':
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")
        apiCall = '/1/user/-/activities/date/' + date + '.json'
        return self.__make_api_call_json( apiCall )
    def log_body_weight( self, weight='0'):
        apiCall = '/1/user/-/body/log/weight.json'
        weight = str(weight)
        if re.match( '\D' , weight ):
            return 0
        else:
            if int(weight) < 160 :
                return 0
            metric = int( weight ) * 0.453592
            now = datetime.datetime.now()
            data = {}
            data['weight'] = metric
            data['date'] = now.strftime( '%Y-%m-%d')
            return self.__make_api_call_json_with_post( apiCall , data )
        return 0
    def __make_api_call_json_with_post(self , apiCall , data ):
        params = urllib.urlencode(data)
        json_data = json.dumps( data )
        connection = httplib.HTTPSConnection(self.SERVER)
        consumer = oauth.OAuthConsumer(self.consumer_key, self.consumer_secret)
        signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
        token  = self.get_token_string()
        access_token = oauth.OAuthToken.from_string(token)
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(
            consumer,
            token=access_token ,
            http_url=apiCall
            )
        oauth_request.sign_request(signature_method, consumer, access_token)
        headers = oauth_request.to_header(realm='api.fitbit.com')
        for d in data:
            headers[d] = data[d]
        api = apiCall + '?' + params
        # query string, jsondata AND header injection?
        # ah, it works. Figure it out later
        connection.request( 'POST', api , json_data , headers )
        resp = connection.getresponse()
        j_data= resp.read()
        return json.loads( j_data )
    def __make_api_call_json(self , apiCall ):
        connection = httplib.HTTPSConnection(self.SERVER)
        consumer = oauth.OAuthConsumer(self.consumer_key, self.consumer_secret)
        signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
        token  = self.get_token_string()
        access_token = oauth.OAuthToken.from_string(token)
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(
            consumer,
            token=access_token ,
            http_url=apiCall
            )
        oauth_request.sign_request(signature_method, consumer, access_token)
        headers = oauth_request.to_header(realm='api.fitbit.com')
        connection.request('GET', apiCall, headers=headers)
        resp = connection.getresponse()
        j_data= resp.read()
        return json.loads( j_data )

def make_class( conf = '/home/jacoby/.fitbit.cnf' ):
    config = os.path.abspath( conf )
    c = open( conf , 'r' )
    c_yaml = c.read()
    c_obj = yaml.load(c_yaml)
    fitbit = FitBit(
        c_obj['consumer_key'] ,
        c_obj['consumer_secret'] ,
        c_obj[ 'default' ] ,
        c_obj[ 'tokens' ]
        ) 
    return fitbit
