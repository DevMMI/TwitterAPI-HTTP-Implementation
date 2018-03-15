#!/usr/bin/env python3


#add the following
import os
import stat
import sys
#import http.client
import requests
import logging
import http.client
import hmac
import hashlib
import urllib
import urllib.parse
import time
import socket
import random
import secrets
import string
import base64
import json
from requests_oauthlib import OAuth1

def _generate_signature(data, key):
    """ Create the signed message from api_key and string_to_sign """
    #return hmac.new(key, data, hashlib.sha1).hexdigest()
    return base64.b64encode(hmac.new(key, data, digestmod=hashlib.sha1).digest())

def query(queryurl, client_key, client_secret, resource_owner_key, resource_owner_secret):
        headeroauth = OAuth1(client_key, client_secret, resource_owner_key,
        resource_owner_secret, signature_type = 'auth_header')

        return requests.get(queryurl, auth = headeroauth)

def _generate_nonce():
    secret = secrets.token_hex(16)
    return str(secret)



def sendTweet():
    debug = False
    #debug = True
    base_url = "https://api.twitter.com/1.1/statuses/update.json?"
    if debug:
        base_url = "localhost:9001"

    # included entities
    entities = "true"
    encoded_incl_entities_key = urllib.parse.quote("include_entities", safe='')
    encoded_incl_entities = urllib.parse.quote(entities, safe='')

    # oauth_consumer_key
    consumerKey = "pGPSO52SDNFh9mw9bjs3UlyTt"
    encoded_cons_key_key = urllib.parse.quote("oauth_consumer_key", safe='')
    encoded_cons_key = urllib.parse.quote(consumerKey, safe='')

    # oath_nonce
    nonce = _generate_nonce()
    encoded_nonce_key = urllib.parse.quote("oauth_nonce", safe='')
    encoded_nonce = urllib.parse.quote(nonce, safe='')

    # oauth_signature_method
    signatureMethod = "HMAC-SHA1"
    encoded_sign_meth_key = urllib.parse.quote("oauth_signature_method", safe='')
    encoded_sign_meth = urllib.parse.quote(signatureMethod, safe='')

    # oauth_timestamp
    timestamp = time.time()
    timestamp_str = str(int(timestamp))
    print("time : "+timestamp_str)
    encoded_timestamp_key = urllib.parse.quote("oauth_timestamp", safe='')
    encoded_timestamp= urllib.parse.quote(timestamp_str, safe='')

    # oauth_token
    myToken = "718628746278879232-rPx8JLxwQuvllwz5JT6mnBZRTTOKLf9"
    encoded_token_key = urllib.parse.quote("oauth_token", safe='')
    encoded_token = urllib.parse.quote(myToken, safe='')

    # oauth_version
    version = "1.0"
    encoded_version_key = urllib.parse.quote("oauth_version", safe='')
    encoded_version = urllib.parse.quote(version, safe='')

    # status
    status = "hello world"
    encoded_status_key = urllib.parse.quote("status", safe='')
    encoded_status = urllib.parse.quote(status, safe='')

    # Build 'DST' Header String
    DST = ""
    keys = [encoded_incl_entities_key, encoded_cons_key_key, encoded_nonce_key, encoded_sign_meth_key, encoded_timestamp_key, encoded_token_key, encoded_version_key, encoded_status_key]

    elements = [encoded_incl_entities, encoded_cons_key, encoded_nonce,encoded_sign_meth, encoded_timestamp, encoded_token, encoded_version, encoded_status]

    # Build header
    for i in range(0, len(elements)):
        if i == (len(elements) - 1):
            DST = DST + keys[i] + "=" + elements[i]
        else:
            DST = DST + keys[i] + "=" + elements[i] + "&"

    # Build full signature base string
    header = "POST"
    encoded_url = urllib.parse.quote(base_url, safe='')
    encoded_parameter_string = urllib.parse.quote(DST, safe='')
    data = header + "&" + encoded_url + "&" + encoded_parameter_string


    # percent encode consumer secret
    cons_secret = "8trRaoFQN6uanT514CWHyEf161We5b1wY66fTYeFYXPiHU9Cim"
    encoded_cons_secret = urllib.parse.quote(cons_secret, safe='')

    # percent encode token secret
    tok_secret = "Tf8DKGNKk4QmDuiVFPXgHFUJilFOGHsCH0U6ahBFonTD2"
    encoded_tok_secret = urllib.parse.quote(tok_secret, safe='')

    # signing key
    sign_key = encoded_cons_secret + "&" + encoded_tok_secret
    #print("data : "+ data + "\n")
    print("key : "+ str(sign_key) + "\n")
    # generate signature
    #key = bytearray(sign_key.encode("utf8").strip())
    #data = bytearray(data.encode("utf8").strip())
    key = bytes(sign_key.encode("utf8"))
    data = bytes(data.encode("utf8"))
    #encoded_signature = _generate_signature(data, key)
    encoded_signature = str(OAuth1(consumerKey, cons_secret, myToken, tok_secret))
    encoded_signature = urllib.parse.quote(encoded_signature, safe='')
    encoded_signature_key = urllib.parse.quote("oauth_signature", safe='')


    # encoded_signature_base_two = urllib.parse.quote(signature, safe='')
    # encoded_signature_base_64 = str(base64.b64encode(encoded_signature_base_two.encode()))
    # encoded_signature_one = encoded_signature_base_64[2:]
    #encoded_signature = urllib.parse.quote(signature, safe='')
    #print("output : "+ signature.decode("utf-8") )
    #print("signature : " + encoded_signature)

    # make auth header
    headerKeys = [encoded_cons_key_key, encoded_nonce_key, encoded_signature_key, encoded_sign_meth_key, encoded_timestamp_key, encoded_token_key,encoded_version_key]
    headerValues = [encoded_cons_key, encoded_nonce, encoded_signature, encoded_sign_meth, encoded_timestamp, encoded_token, encoded_version]

    auth_head = "OAuth "
    # Build header
    for i in range(0, len(headerKeys)):
        if i == (len(headerKeys) - 1):
            auth_head = auth_head + headerKeys[i] + "=" + "\"" + headerValues[i] + "\" "
        else:
            auth_head = auth_head + headerKeys[i] + "=" + "\"" + headerValues[i] + "\"" + ", "

    print("Header : " +auth_head)
    # begin connection
    conn = http.client.HTTPSConnection("api.twitter.com")
    if debug:
        conn = http.client.HTTPConnection("localhost:9001")

    headers = {"Accept": "*/*", "Connection": "close", "User-Agent": "OAuth gem v0.4.4",\
     "Content-Type": "application/x-www-form-urlencoded","Authorization": auth_head, "status": status, "media_ids": "471592142565957632"}

    if debug:
         #conn = http.client.HTTPConnection("localhost:9001")
         #conn.request("POST", "/", "status="+encoded_status, headers)
         r = requests.post("http://localhost:9001", data=headers)
         print(r.status_code, r.reason)
    else:
        rauth = OAuth1(consumerKey, cons_secret, myToken, tok_secret)
        r = requests.post("https://api.twitter.com/1.1/statuses/update.json?", data=headers, auth = rauth)
        print(r.status_code, r.reason)
        #conn.request("POST", "/1.1/statuses/update.json?", "status="+encoded_status, headers)
        #resp, content = client.request("'https://api.twitter.com/1.1/statuses/update.json?", method="POST", body=status, headers=headers )

    response = conn.getresponse()
    data = response.read()
    print("Response : "+ str(data))
    conn.close()


if __name__ == '__main__':
  sendTweet()
