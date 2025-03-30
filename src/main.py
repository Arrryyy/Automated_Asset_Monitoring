import tweepy
import pandas as pd
import datetime
import requests
import re
import traceback
import json
from typing import Dict, List, Any

# Hugging Face Open API details
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"

# Twitter API credentials (replace these!)
consumer_key = "nk4WRAnq8pqXonhUaheZO70ac"    
consumer_secret = "jec29ljDq6n6VHoeD8yMmCwiqOCIy5oxIH06rzq1xpGDKEz7YF"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAJgN0QEAAAAA2uMlcKJrVC07WYNBjfMuSdBI3fo%3DehtyJLpBup75s8YojnH2km25MOnJprNhP9Vy1c68Y0MVgMZvjn"

client = tweepy.Client(bearer_token=bearer_token)

def scrape_tweets(query: str, max_tweets=100):
    tweets_data = []
    today = datetime.datetime.now(datetime.UTC)
    seven_days_ago = today - datetime.timedelta(days=7)

    for tweet in tweepy.Paginator(client.search_recent_tweets, 
                                  query=query,
                                  tweet_fields=['created_at', 'author_id', 'public_metrics'],
                                  max_results=100).flatten(limit=max_tweets):
        tweets_data.append({
            "id": tweet.id,
            "date": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "content": tweet.text,
            "likes": tweet.public_metrics['like_count'],
            "retweets": tweet.public_metrics['retweet_count']
        })

    return tweets_data

def evaluate_tweet_hf(content: str) -> Dict[str, Any]:
    try:
        response = requests.post(HUGGINGFACE_API_URL, json={"inputs": content})
        response_json = response.json()

        sentiment_label = max(response_json[0], key=lambda x: x['score'])['label']

        risk_keywords = ["scam", "hack", "fraud", "vulnerability", "attack"]
        risk_score = sum(content.lower().count(term) for term in risk_keywords)

        relevance = any(term in content.lower() for term in ["solana", "$sol", "#sol", "#solana"])

        categories = []
        if re.search(r"\b(price|market|bull|bear|invest)\b", content, re.I):
            categories.append("investment")
        if re.search(r"\b(code|develop|program|build|deploy)\b", content, re.I):
            categories.append("development")
        if re.search(r"\b(nft|art|collect)\b", content, re.I):
            categories.append("NFT")
        if re.search(r"\b(defi|yield|swap|lend)\b", content, re.I):
            categories.append("DeFi")

        return {
            "sentiment": sentiment_label,
            "risk_score": risk_score,
            "relevance": relevance,
            "categories": categories
        }
    except Exception as e:
        print(f"Error in LLM evaluation: {e}")
        traceback.print_exc()
        return {"sentiment": "unknown", "risk_score": 0, "relevance": False, "categories": []}

def main():
    tweets = scrape_tweets("(Solana OR #Solana) lang:en -is:retweet", max_tweets=5)

    if not tweets:
        print("No tweets were scraped. Exiting.")
        return

    for tweet in tweets:
        tweet.update(evaluate_tweet_hf(tweet["content"]))

    df = pd.DataFrame(tweets)

    csv_filename = "data/solana_tweets_analysis.csv"
    df.to_csv(csv_filename, index=False)
    print(f"CSV exported to {csv_filename}")

    json_filename = "data/solana_tweets_analysis.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=4)

    print(f"JSON exported to {json_filename}")

if __name__ == "__main__":
    main()
