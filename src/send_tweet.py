from lib2to3.pgen2 import token
from venv import create
import requests
import os
import logging

import time
import urllib.parse
import hmac
import hashlib
from base64 import b64encode
import binascii
import requests
import uuid
from requests_oauthlib import OAuth1


def create_oauth():
    consumer_key = os.environ.get("KEY_ID")
    access_token = os.environ.get("ACCESS_TOKEN")
    consumer_secret = urllib.parse.quote(os.environ.get("KEY_SECRET"))
    access_token_secret = urllib.parse.quote(os.environ.get("TOKEN_SECRET"))
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    headers = {
        "Content-Type": "application/json",
    }
    return headers, auth


def send_tweet(text, reply_id=None):
    url = f"https://api.twitter.com/2/tweets"
    data = {"text": text}
    headers, auth = create_oauth()
    print(headers)
    if reply_id:
        data["reply"] = {"in_reply_to_tweet_id": reply_id}
    r = requests.post(url, headers=headers, auth=auth, json=data)
    result = r.json()
    logging.info("Just tweeted " + str(r.content))
    return result
