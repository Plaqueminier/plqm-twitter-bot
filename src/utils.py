import requests
from dotenv import load_dotenv
import os
import json
import logging
from operator import attrgetter, itemgetter

def retrieve_id(name):
    logging.info("Retrieving id of " + name)
    url = f"https://api.twitter.com/2/users/by/username/{name}"
    headers = {
        "Authorization": "Bearer " + os.environ.get("BEARER"),
    }
    r = requests.get(url, headers=headers)
    id = r.json()["data"]["id"]
    logging.info("ID is " + id)
    return id

def associate_medias(tweets, medias):
    for tweet in tweets:
        if "attachments" in tweet:
            tweet["media_url"] = []
            for key in tweet["attachments"]["media_keys"]:
                media = next(X for X in medias if X["media_key"] == key)
                tweet["media_type"] = media["type"]
                if "url" in media:
                    tweet["media_url"].append(media["url"])
                elif "preview_image_url" in media:
                    tweet["media_url"].append(media["preview_image_url"])
    return tweets

def associate_users(tweets, users):
    for tweet in tweets:
        user = next(X for X in users if X["id"] == tweet["author_id"])
        tweet["name"] = user["name"]
        tweet["username"] = user["username"]
    return tweets
