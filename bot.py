from src.send_tweet import send_tweet
from src.get_bot_mentions import retrieve_tweets_to_bot
from src.get_top import create_top_answer, retrieve_top_tweets
from src.tweets_data import ListingData, Tweet
from dotenv import load_dotenv
import json
import logging
import time
from unidecode import unidecode
import dateutil.parser
from typing import List


def call_top(command: List[str], tweet: Tweet) -> None:
    if len(command) <= 1:
        logging.error("I need a username to do that !")
        return
    data = retrieve_top_tweets(
        command[1], 100, {"text": True, "photo": True, "video": True}
    )
    if data == None:
        logging.error(
            "You gave me a wrong username (maybe this person is in private mode)"
        )
        return
    if data.meta.count > 0:
        send_tweet(create_top_answer(data, tweet.username), tweet.id)


commands = {"/top": call_top}


def parse_command(tweet: Tweet) -> None:
    command = [X.lower() for X in tweet.text.split(" ")]
    command.remove("@plqmbot")
    for index, word in enumerate(command):
        if word in commands.keys():
            commands[word](command[index:], tweet)
            return
    logging.info("Cannot process this one")


if __name__ == "__main__":
    load_dotenv()
    logging.getLogger().setLevel(logging.INFO)
    while True:
        last_data: ListingData = retrieve_tweets_to_bot()
        logging.info(str(last_data.meta.count) + " tweets to process")
        for tweet in last_data.tweets:
            logging.info("Processing " + tweet.text)
            parse_command(tweet)
            logging.info("Waiting...")
            time.sleep(1)
        logging.info("Waiting 60s...")
        time.sleep(60)
