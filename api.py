# app.py

import os
import json
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# 1) Enable LangSmith v2 tracing globally
# Make sure you have LANGSMITH_API_KEY set before any LangChain code runs
import config
os.environ["LANGSMITH_API_KEY"]    = config.LANGSMITH_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"

from langchain_core.tracers.context import tracing_v2_enabled
tracing_v2_enabled()

# 2) Your workflow & state type
from workflow import create_financial_analysis_graph, FinancialAnalysisState

app = FastAPI()

# 3) Pydantic models
class TickerRequest(BaseModel):
    ticker: str

class AnalysisResponse(BaseModel):
    stock_data:      Dict[str, Any]
    news_data:       List[Dict[str, Any]]
    technical_data:  List[Dict[str, Any]]
    final_summary:   str
    company_data:    Dict[str, Any]


# 4) Core graph invocation
async def run_financial_analysis(ticker: str) -> FinancialAnalysisState:
    graph = create_financial_analysis_graph()
    init_state: FinancialAnalysisState = {
        "ticker":          ticker,
        "stock_data":      {},
        "news_data":       {},
        "technical_data":  {},
        "final_summary":   "",
        "company_data":    {},
    }
    # no callbacks arg needed—v2 tracing picks up everything
    return await graph.ainvoke(init_state)


# 5) Helper to pull out the JSON payload from your tool messages
def extract_tool_json(
    messages: List[Any],
    tool_name: str
) -> Any:
    for msg in messages:
        msg_type    = getattr(msg, "type", None) or getattr(msg, "message_type", None)
        msg_name    = getattr(msg, "name", None) or getattr(msg, "tool", None)
        msg_content = getattr(msg, "content", None)
        if msg_type == "tool" and msg_name == tool_name and msg_content:
            return json.loads(msg_content)
        if isinstance(msg, dict) and msg.get("type") == "tool" and msg.get("name") == tool_name:
            return json.loads(msg["content"])
    return {}


# 6) Your FastAPI routes
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: TickerRequest):
    try:
        state = await run_financial_analysis(request.ticker)

        stock_data = extract_tool_json(
            state["stock_data"]["messages"],
            "get_stock_info_fmp"
        )

        news_raw = extract_tool_json(
            state["news_data"]["messages"],
            "get_company_news_finnhub"
        )
        news_data = news_raw.get("data", [])

        tech_raw = extract_tool_json(
            state["technical_data"]["messages"],
            "get_technical_indicators_twelvedata_tool"
        )
        technical_data = tech_raw.get("data", [])

        company_data = extract_tool_json(
            state["company_data"]["messages"],
            "get_fundamentals_finnhub"
        )

        print("----" * 10)
        print("RESPONSE DATA")
        print("----" * 10)

        print("company_data")
        print(company_data)
        print("\n" * 5)

        print("stock_data")
        print(stock_data)
        print("\n" * 5)

        print("news_data")
        print(news_data)
        print("\n" * 5)

        print("technical_data")
        print(technical_data)
        print("\n" * 5)

        return AnalysisResponse(
            stock_data=stock_data,
            news_data=news_data,
            technical_data=technical_data,
            final_summary=state["final_summary"],
            company_data=company_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
