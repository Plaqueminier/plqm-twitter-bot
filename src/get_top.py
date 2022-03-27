import string
import requests
from dotenv import load_dotenv
import os
import json
import logging
from operator import attrgetter, itemgetter
from typing import List

from .utils import retrieve_id, create_tweet_url
from .tweets_data import ListingData
import dateutil.parser


def create_url(id, limit, next_token):
    url = (
        f"https://api.twitter.com/2/users/{id}/tweets"
        f"?max_results={limit}"
        f"&tweet.fields=public_metrics,created_at"
        f"&exclude=retweets"
        f"&expansions=attachments.media_keys,author_id"
        f"&media.fields=url,type,preview_image_url"
        f"&user.fields=name"
    )
    if next_token:
        url += f"&pagination_token={next_token}"
    return url


def create_top_answer(data: ListingData, username: string):
    answer = (
        "@"
        + username
        + " "
        + str(data.meta.count)
        + " tweets from "
        + str(dateutil.parser.isoparse(data.meta.oldest).strftime("%Y-%m-%d %H:%M"))
        + " to "
        + str(dateutil.parser.isoparse(data.meta.newest).strftime("%Y-%m-%d %H:%M"))
        + "\n"
    )
    for i in range(5):
        answer += (
            str(data.tweets[i].public_metrics["like_count"])
            + "\U00002665"
            + " : "
            + create_tweet_url(data.tweets[i].id)
            + "\n"
        )
    return answer


def retrieve_top_tweets(name: str, nb: int, filters):
    id = retrieve_id(name)
    if not id:
        return None
    limit = 100 if nb > 100 else max(nb, 5)
    next_token = None
    logging.info("Now retrieving tweets of " + name)
    medias = []
    users = []
    data = ListingData()
    while nb > 0:
        url = create_url(id, limit, next_token)
        headers = {
            "Authorization": "Bearer " + os.environ.get("BEARER"),
        }
        r = requests.get(url, headers=headers)
        result = r.json()
        try:
            data.set_tweets_from_listing(result)
            medias += result["includes"]["media"]
            users += result["includes"]["users"]
            if not "next_token" in result["meta"]:
                break
            next_token = result["meta"]["next_token"]
        except KeyError:
            logging.error(result)
            break
        nb -= limit
        limit = 100 if nb > 100 else max(nb, 5)
    data.set_metadata(users, medias)
    data.sort_by_likes()
    return data
