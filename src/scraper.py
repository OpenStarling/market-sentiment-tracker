import feedparser
import pandas as pd
from bs4 import BeautifulSoup

def scrape_reddit_rss(subreddit="CryptoCurrency"):
    url = f"https://www.reddit.com/r/{subreddit}/new/.rss"
    
    # Prepending 'Mozilla/5.0' makes Reddit think you're a person browsing
    feed = feedparser.parse(url, agent='Mozilla/5.0 (X11; Linux x86_64)')
    
    posts = []
    for entry in feed.entries:
        # RSS descriptions are often messy HTML, BeautifulSoup cleans it up
        soup = BeautifulSoup(entry.summary, "html.parser")
        posts.append({
            "title": entry.title,
            "text": soup.get_text()[:500], # Grab first 500 chars
            "date": entry.updated,
            "link": entry.link
        })
    
    return pd.DataFrame(posts)

if __name__ == "__main__":
    print(f"Fetching latest 'vibe' from Reddit...")
    df = scrape_reddit_rss("CryptoCurrency")
    df.to_csv("data/raw_social.csv", index=False)
    print("Saved to data/raw_social.csv. Check the folder!")