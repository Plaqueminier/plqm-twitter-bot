from ast import Str
from venv import create
import requests
import os
import datetime
import json
import logging

from .tweets_data import ListingData
from .utils import retrieve_id

last_tweet_id = None


def create_url(id) -> str:
    url = (
        f"https://api.twitter.com/2/users/{id}/mentions"
        f"?tweet.fields=public_metrics,created_at,author_id"
        f"&expansions=author_id"
        f"&user.fields=name"
    )
    if last_tweet_id:
        url += f"&since_id={last_tweet_id}"
    else:
        half_hour_before = (
            (datetime.datetime.utcnow() - datetime.timedelta(minutes=200))
            .replace(microsecond=0)
            .isoformat()
        )
        url += f"&start_time={half_hour_before}Z"
    return url


def retrieve_tweets_to_bot():
    global last_tweet_id
    id = retrieve_id("plqmbot")
    url = create_url(id)
    headers = {
        "Authorization": "Bearer " + os.environ.get("BEARER"),
    }
    data = ListingData()
    r = requests.get(url, headers=headers)
    result = r.json()
    try:
        users = result["includes"]["users"]
        print(result)
        data.set_tweets_from_listing(result)
        data.set_metadata(users)
        print(data)
        last_tweet_id = data.tweets[-1].id
    except KeyError or IndexError:
        logging.error(result)
    return data
