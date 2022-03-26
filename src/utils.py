import requests
from dotenv import load_dotenv
import os
import json
import logging
from operator import attrgetter, itemgetter


def create_tweet_url(id: str):
    return f"https://twitter.com/twitter/status/{id}"


def retrieve_id(name):
    logging.info("Retrieving id of " + name)
    url = f"https://api.twitter.com/2/users/by/username/{name}"
    headers = {
        "Authorization": "Bearer " + os.environ.get("BEARER"),
    }
    r = requests.get(url, headers=headers)
    try:
        id = r.json()["data"]["id"]
        logging.info("ID is " + id)
        return id
    except KeyError:
        return None
