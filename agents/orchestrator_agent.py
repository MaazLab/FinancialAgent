from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, LANGSMITH_API_KEY
import os 
from langchain.callbacks.tracers import LangChainTracer

os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"

tracer = LangChainTracer()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, callbacks=[tracer])

# Create the main orchestrator agent
orchestrator_agent = create_react_agent(
    llm,
    [],  # No tools - it just orchestrates other agents
    prompt="""You are the Financial Analysis Orchestrator Agent. Your role is to:

1. Receive a stock ticker symbol from the user
2. Call four specialized sub-agents in parallel:
   - StockPriceAgent: for real-time stock data
   - CompanyNewsAgent: for recent company news
   - FinancialAgent: for technical indicators
   - CompanyFundamentalAgent: for company fundamentals
3. Collect all their outputs
4. Provide a comprehensive, actionable financial analysis summary

When you receive the ticker, you will automatically call all four sub-agents and then provide a detailed summary including:
- Current stock performance analysis
- Key news highlights and their impact
- Technical analysis insights
- Company fundamentals insights
- Overall market sentiment
- Investment considerations and recommendations

Be thorough, professional, and provide actionable insights."""
)
