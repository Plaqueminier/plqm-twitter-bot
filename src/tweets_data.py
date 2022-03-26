from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class MetaData:
    count: int
    oldest: datetime
    newest: datetime

    def __init__(self):
        self.count = 0


@dataclass
class Tweet:
    id: str
    author_id: str
    text: str
    created_at: str
    public_metrics: Dict[str, int]
    name: str = ""
    username: str = ""
    media_keys: Optional[str] = None
    media_type: Optional[str] = None
    media_url: Optional[str] = None

    def __init__(
        self,
        id: str,
        author_id: str,
        text: str,
        created_at: str,
        public_metrics: Dict[str, int],
        media_keys: Optional[List[str]],
    ):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.created_at = created_at
        self.public_metrics = public_metrics
        if media_keys:
            self.media_keys = media_keys

    def __repr__(self):
        return (
            self.text
            + " created "
            + self.created_at
            + " rt/like "
            + str(self.public_metrics["retweet_count"])
            + "/"
            + str(self.public_metrics["like_count"])
        )


@dataclass
class ListingData:
    tweets: List[Tweet]
    meta: MetaData

    def __init__(self):
        self.tweets = []
        self.meta = MetaData()

    def sort_by_likes(self):
        self.tweets = sorted(
            self.tweets, key=(lambda x: x.public_metrics["like_count"]), reverse=True
        )

    def set_metadata(self, users: List, medias: List = []):
        self.meta.count = len(self.tweets)
        if self.meta.count > 0:
            self.meta.oldest = self.tweets[-1].created_at
            self.meta.newest = self.tweets[0].created_at
            self.associate_medias(medias)
            self.associate_users(users)

    def set_tweets_from_listing(self, result):
        self.tweets += [
            Tweet(
                x["id"],
                x["author_id"],
                x["text"],
                x["created_at"],
                x["public_metrics"],
                x["attachments"]["media_keys"] if "attachments" in x else None,
            )
            for x in result["data"]
        ]

    def associate_medias(self, medias: List):
        for tweet in self.tweets:
            if tweet.media_keys != None:
                tweet.media_url = []
                for key in tweet.media_keys:
                    media = next(X for X in medias if X["media_key"] == key)
                    tweet.media_type = media["type"]
                    tweet.media_url.append(
                        media["url"] if "url" in media else media["preview_image_url"]
                    )

    def associate_users(self, users: List):
        for tweet in self.tweets:
            user = next(X for X in users if X["id"] == tweet.author_id)
            tweet.name = user["name"]
            tweet.username = user["username"]
