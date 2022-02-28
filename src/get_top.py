import requests
from dotenv import load_dotenv
import os
import json
import logging
from operator import attrgetter, itemgetter
from .utils import retrieve_id, associate_medias

def create_url(id, limit, next_token):
    url = f"https://api.twitter.com/2/users/{id}/tweets" \
        f"?max_results={limit}" \
        f"&tweet.fields=public_metrics,created_at" \
        f"&exclude=retweets" \
        f"&expansions=attachments.media_keys" \
        f"&media.fields=url,type,preview_image_url"
    if next_token:
        url += f"&pagination_token={next_token}"
    return url


def filter_and_sort(
    tweets,
    filters
):
    filtered = []
    if filters["text"]:
        filtered += list(filter(lambda x: not "media_type" in x, tweets))
    if filters["photo"]:
        filtered += list(filter(lambda x: "media_type" in x and x["media_type"] == "photo", tweets))
    if filters["video"]:
        filtered += list(filter(lambda x: "media_type" in x and x["media_type"] == "video", tweets))
    filtered = sorted(filtered, reverse=True, key=lambda x: x["public_metrics"]["like_count"])
    return filtered

def retrieve_top_tweets(
    name,
    nb,
    filters
):
    id = retrieve_id(name)
    limit = 100 if nb > 100 else max(nb, 5)
    next_token = None
    logging.info("Now retrieving tweets of", name)
    medias = []
    data = {
        "tweets": [],
        "meta": {
            "count": 0,
            "oldest": None,
            "newest": None
        },
    }
    while nb > 0:
        url = create_url(id, limit, next_token)
        headers = {
            "Authorization": "Bearer " + os.environ.get("BEARER"),
        }
        r = requests.get(url, headers=headers)
        result = r.json()
        try:
            data["tweets"] += result["data"]
            medias += result["includes"]["media"]
            associate_medias(data["tweets"], medias)
            if not "next_token" in result["meta"]:
                break
            next_token = result["meta"]["next_token"]
        except KeyError:
            logging.error(result)
            break
        nb -= limit
        limit = 100 if nb > 100 else max(nb, 5)
    data["tweets"] = filter_and_sort(data["tweets"], filters)
    data["meta"]["count"] = len(data["tweets"])
    data["meta"]["oldest"] = data["tweets"][-1]["created_at"]
    data["meta"]["newest"] = data["tweets"][0]["created_at"]
    print(json.dumps(data))
