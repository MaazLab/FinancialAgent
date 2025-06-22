from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, LANGSMITH_API_KEY
import os 
from langchain.callbacks.tracers import LangChainTracer
from tools.company_news_tool import get_company_news_finnhub, get_company_news_rss

os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"


tracer = LangChainTracer()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, callbacks=[tracer])

company_news_agent = create_react_agent(
    llm,
    [get_company_news_finnhub, get_company_news_rss], 
    prompt="You are CompanyNewsAgent: retrieve recent news for a ticker. Return the most relevant news articles in a structured format. You have two tools available: one for fetching news from Finnhub and another for fetching news from Google News RSS feeds. Fetch news from Finnhub first and if you cannot fetch any news, then use the Google News RSS feed as a fallback. "
    )
