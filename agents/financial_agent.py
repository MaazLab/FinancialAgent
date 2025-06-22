from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, LANGSMITH_API_KEY
import os 
from langchain.callbacks.tracers import LangChainTracer
from tools.technical_indicator_tool import (
    get_technical_indicators_alpha_vantage_tool,
    get_technical_indicators_twelvedata_tool
)

os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"

tracer = LangChainTracer()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, callbacks=[tracer])

financial_data_agent = create_react_agent(
    llm,
    [get_technical_indicators_alpha_vantage_tool, get_technical_indicators_twelvedata_tool],
    prompt="You are FinancialAgent: gather technical indicators from multiple sources. Return the technical idicators data in a structured format. You have two tools available: one for fetching technical indicators from Alpha Vantage and another fetching technical indicators from Twelvedata. Fetch technical indicators from Twelvedata first and if you cannot fetch any technical indicators, then use the AlphaVantage as a fallback."
)
