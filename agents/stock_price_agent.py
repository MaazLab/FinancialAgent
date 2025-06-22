from config import OPENAI_API_KEY, LANGSMITH_API_KEY
import os 
from langchain.callbacks.tracers import LangChainTracer
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from tools.stock_data_tool import get_stock_info_yf, get_stock_info_fmp

os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"


tracer = LangChainTracer()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, callbacks=[tracer])

# Create the 3 sub-agents using create_react_agent
stock_price_agent = create_react_agent(
    llm, 
    [get_stock_info_yf, get_stock_info_fmp],
    prompt="You are StockPriceAgent: fetch real-time price data for a given ticker. Return the data in a clear, structured format. You have two tools available: one for fetching stock data from yfinance and another for fetching stock data from financialmodelingprep. Fetch data from financialmodelingprep first and if you cannot fetch any data, then use the yfinance as a fallback."
)