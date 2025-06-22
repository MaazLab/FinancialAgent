from langchain_core.tools import tool
import finnhub
from datetime import datetime, timedelta, timezone
import feedparser
from config import FINNHUB_API_KEY
from urllib.parse import quote_plus

@tool
async def get_company_news_finnhub(ticker: str, days: int = 7) -> dict:
    """
    Fetch recent news articles for a NASDAQ ticker using Finnhub.
    """
    print("----"*10)
    print("Tool called: get_company_news_finnhub")
    print("----"*10)

    if not FINNHUB_API_KEY:
        return {"error": "Finnhub API key not provided"}

    # Initialize client
    client = finnhub.Client(api_key=FINNHUB_API_KEY)

    # Compute date range
    to_date = datetime.now(timezone.utc).date()
    from_date = to_date - timedelta(days=days)
    frm = from_date.isoformat()
    to = to_date.isoformat()

    try:
        # Fetch company news
        news = client.company_news(symbol=ticker, _from=frm, to=to)

        if not isinstance(news, list):
            return {"error": f"Unexpected response format: {news}"}

        # Return only relevant fields
        filtered = []
        for item in news:
            filtered.append({
                "datetime": item.get("datetime"),
                "headline": item.get("headline"),
                "source": item.get("source"),
                "url": item.get("url"),
                "summary": item.get("summary"),
                "image": item.get("image")
            })

        return {"data": filtered}

    except finnhub.exceptions.FinnhubAPIException as e:
        return {"error": f"Finnhub API error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}
    

@tool
async def get_company_news_rss(ticker: str, days: int = 7) -> dict:
    """
    Fetch recent news articles for a NASDAQ ticker over the past `days` days
    by querying the Google News RSS feed.

    Args:
        ticker (str): Stock symbol, e.g. "AAPL"
        days   (int): Lookback window in days (default 7)

    Returns:
        dict:
          - on success: {"data": [
                {
                  "datetime": "2025-06-20T14:30:00",
                  "headline": "...",
                  "link": "...",
                  "summary": "..."
                },
                …
            ]}
          - on error:   {"error": "<message>"}
    """

    print("----"*10)
    print("Tool called: get_company_news_rss")
    print("----"*10)

    # URL-encode the query to avoid spaces and control characters
    query = quote_plus(f"{ticker} stock")
    feed_url = f"https://news.google.com/rss/search?q={query}"

    # Try parsing the feed
    try:
        feed = feedparser.parse(feed_url)
        if feed.bozo and hasattr(feed, "bozo_exception"):
            raise feed.bozo_exception
    except Exception as e:
        return {"error": f"Failed to fetch or parse RSS feed: {e}"}

    # Filter entries by publish date
    cutoff = datetime.utcnow() - timedelta(days=days)
    articles = []
    for entry in feed.entries:
        if not hasattr(entry, "published_parsed"):
            continue
        published_dt = datetime(*entry.published_parsed[:6])
        if published_dt < cutoff:
            continue

        articles.append({
            "datetime": published_dt.isoformat(),
            "headline": entry.get("title", ""),
            "link":      entry.get("link", ""),
            "summary":   entry.get("summary", "")
        })

    return {"data": articles}
