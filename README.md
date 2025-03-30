# Solana Tweets Analysis

This project scrapes recent tweets about Solana, evaluates each tweet's sentiment, risk score, relevance, and category using a Hugging Face sentiment model, and then exports the results to both CSV and JSON formats.

## Overview

- **Tweet Scraping:** Uses Tweepy to fetch recent tweets containing terms like "Solana", "#Solana", or "$sol".  
- **Tweet Evaluation:** Analyzes each tweet’s text for:
  - **Sentiment:** Uses a Hugging Face model to determine the tweet’s sentiment.
  - **Risk Score:** Counts risk-related keywords (e.g., scam, hack, fraud).
  - **Relevance:** Checks if the tweet contains specific Solana-related terms.
  - **Categories:** Assigns categories (investment, development, NFT, DeFi) based on keyword matching.
- **Output:** Saves the combined results as a CSV and a JSON file.

## Requirements

- Python 3.8 or higher
- Packages:
  - `tweepy`
  - `pandas`
  - `requests`
  - `datetime`
  - `re`
  - `traceback`
  - `json`

## Setup

1. **Clone the repository** (or copy the script into your working directory).

2. **Install the required packages:**

   ```bash
   pip install tweepy pandas requests# Solana Tweets Analysis

This project fetches recent tweets about Solana, analyzes each tweet for sentiment, risk, relevance, and category, and then exports the results to both CSV and JSON files.

## Overview

- **Tweet Scraping:** Uses Tweepy to collect recent tweets containing terms like "Solana", "#Solana", or "$sol".
- **Tweet Evaluation:** 
  - Uses a Hugging Face sentiment model to assess tweet sentiment.
  - Counts risk-related keywords (e.g., scam, hack, fraud) to compute a risk score.
  - Checks for Solana-related terms to determine relevance.
  - Assigns categories (investment, development, NFT, DeFi) based on keyword matching.
- **Output:** Saves the combined data to `solana_tweets_analysis.csv` and `solana_tweets_analysis.json`.

## Requirements

- Python 3.7+
- Required Python packages:
  - `tweepy`
  - `pandas`
  - `requests`

Install the required packages using pip:

```bash
pip install tweepy pandas
```
## Setup

1. **Clone or Download the Project:**
   - Place the `main.py` script in your working directory.

2. **Configure API Credentials:**
   - Open `main.py` and replace the placeholder values for the Twitter API credentials:
     - `consumer_key`
     - `consumer_secret`
     - `bearer_token`
   - The Hugging Face API URL is preset to:
     ```
     https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest
     ```
   - **Important:** Ensure that sensitive files (such as `config.yaml` if used) are not pushed to GitHub by adding them to your `.gitignore`.

## How to Run the Code

1. **Activate your Python Environment:**
   - Make sure you have activated the correct Python environment (e.g., via conda or virtualenv).

2. **Run the Script:**

   ```bash
   python main.py

## Output Files:
	
  The script will generate:
	-	solana_tweets_analysis.csv — a CSV file with the tweet data and analysis.
	-	solana_tweets_analysis.json — a JSON file with the same information.
