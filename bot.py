from src.get_bot_mentions import retrieve_tweets_to_bot
from src.get_top import retrieve_top_tweets
from dotenv import load_dotenv
import json
import logging
import time

def call_top(command):
    print(command)

commands = {
    "/top": call_top
}

def parse_command(tweet):
    command = [X.lower() for X in tweet.split(" ")]
    command.remove("@plqmbot")
    for index, word in enumerate(command):
        if word in commands.keys():
            commands[word](command[index:])
            return
    logging.info("Cannot process this one")

if __name__ == "__main__":
    load_dotenv()
    logging.getLogger().setLevel(logging.INFO)
    last_data = retrieve_tweets_to_bot()
    logging.info(str(last_data["meta"]["count"]) + " tweets to process")
    for tweet in last_data["tweets"]:
        logging.info("Processing " + tweet["text"])
        parse_command(tweet["text"])
        logging.info("Waiting...")
        time.sleep(1)