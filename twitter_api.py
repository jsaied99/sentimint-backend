import requests
import os
from dotenv import load_dotenv
load_dotenv()

bearer_token = os.getenv("TWITTER_API_KEY")

def get_tweets(topic: str, limit=10) -> list:
    base_url = "https://api.twitter.com/2/tweets/search/recent?query={}&max_results={}&tweet.fields=lang".format(
        topic, limit)
    
    response = requests.get(base_url, headers={"Authorization": bearer_token})    
    data = response.json()
    text_array = []

    for tweet in data["data"]:
        tmp = (tweet["text"], tweet["lang"])
        text_array.append(tmp)

    return text_array
