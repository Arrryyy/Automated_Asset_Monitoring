import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import requests
import re
import os
import json
from typing import Dict, List, Any

# Hugging Face Open API details
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"

def scrape_tweets(query: str, max_tweets=100):
    tweets_data = []
    today = datetime.datetime.utcnow()
    seven_days_ago = today - datetime.timedelta(days=7)

    search_query = f"{query} since:{seven_days_ago.date()} until:{today.date()}"

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
        if i >= max_tweets:
            break
        tweets_data.append({
            "id": tweet.id,
            "date": tweet.date.strftime("%Y-%m-%d %H:%M:%S"),
            "content": tweet.content,
            "likes": tweet.likeCount,
            "retweets": tweet.retweetCount
        })

    return tweets_data

def evaluate_tweet_hf(content: str) -> Dict[str, Any]:
    try:
        response = requests.post(HUGGINGFACE_API_URL, json={"inputs": content})
        response.raise_for_status()
        response_json = response.json()

        if not response_json or not isinstance(response_json, list) or not response_json[0]:
            raise ValueError("Unexpected response format from Hugging Face API")

        sentiment_label = max(response_json[0], key=lambda x: x['score'])['label']
    except Exception as e:
        print(f"Error in LLM evaluation: {e}")
        return {"sentiment": "unknown", "risk_score": 0, "relevance": False, "categories": []}

    # Risk Analysis
    risk_keywords = ["scam", "hack", "fraud", "vulnerability", "attack"]
    risk_score = sum(content.lower().count(term) for term in risk_keywords)

    # Relevance
    relevance = any(term in content.lower() for term in ["solana", "$sol", "#sol", "#solana"])

    # Categorization
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

def main():

    tweets = scrape_tweets("(Solana OR #Solana) lang:en", max_tweets=5)
    
    if not tweets:
        print("No tweets were scraped. Exiting.")
        return
    


    for tweet in tweets:
        tweet.update(evaluate_tweet_hf(tweet["content"]))



    df = pd.DataFrame(tweets)



    os.makedirs("data", exist_ok=True)



    csv_filename = "data/test_tweets_analysis.csv"



    df.to_csv(csv_filename, index=False)
    print(f"CSV exported to {csv_filename}")

    json_filename = "data/test_tweets_analysis.json"



    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=4)


    print(f"JSON exported to {json_filename}")

if __name__ == "__main__":

    main()