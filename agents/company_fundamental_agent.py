import os
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.callbacks.tracers import LangChainTracer
from config import OPENAI_API_KEY, LANGSMITH_API_KEY
from tools.company_fundamentals_tool import get_fundamentals_finnhub

os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"

tracer = LangChainTracer()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, callbacks=[tracer])

company_fundamental_agent = create_react_agent(
    llm,
    [get_fundamentals_finnhub], 
    prompt="You are FinancialAgent: gather Company fundamentals from multiple sources. Return the company fundamental data in a structured format."
)