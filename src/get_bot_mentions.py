from venv import create
import requests
import os
import json
import logging
from .utils import retrieve_id, associate_users

def create_url(id):
    url = f"https://api.twitter.com/2/users/{id}/mentions" \
        f"?tweet.fields=public_metrics,created_at,author_id" \
        f"&expansions=author_id" \
        f"&user.fields=name"
    return url


def retrieve_tweets_to_bot():
    id = retrieve_id("plqmbot")
    url = create_url(id)
    headers = {
        "Authorization": "Bearer " + os.environ.get("BEARER"),
    }
    data = {
        "tweets": [],
        "meta": {
            "count": 0,
            "oldest": None,
            "newest": None
        },
    }
    users = []
    r = requests.get(url, headers=headers)
    result = r.json()
    users = []
    users = result["includes"]["users"]
    data["tweets"] = result["data"]
    data["meta"]["count"] = len(data["tweets"])
    data["meta"]["oldest"] = data["tweets"][-1]["created_at"]
    data["meta"]["newest"] = data["tweets"][0]["created_at"]
    associate_users(data["tweets"], users)
    return data