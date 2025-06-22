from langgraph.graph import StateGraph, Graph
from typing import TypedDict, Dict, Any
from langchain_core.messages import HumanMessage
import asyncio

from agents.stock_price_agent import stock_price_agent
from agents.company_news_agent import company_news_agent
from agents.financial_agent import financial_data_agent
from agents.company_fundamental_agent import company_fundamental_agent 
from agents.orchestrator_agent import orchestrator_agent

class FinancialAnalysisState(TypedDict):
    ticker: str
    stock_data: Dict[str, Any]
    news_data: Dict[str, Any]
    technical_data: Dict[str, Any]
    company_data: Dict[str, Any]
    final_summary: str

# Define workflow nodes
async def orchestrator_node(state: FinancialAnalysisState) -> FinancialAnalysisState:
    """Main orchestrator node that calls all sub-agents in parallel"""
    ticker = state['ticker']
    
    try:
        print(f"🎯 Orchestrator Agent: Starting parallel analysis for {ticker}")
        
        # Create tasks for parallel execution of all 4 sub-agents

        stock_task = stock_price_agent.ainvoke({
            "messages": [HumanMessage(content=f"Get stock data for {ticker}")]
        })
        
        news_task = company_news_agent.ainvoke({
            "messages": [HumanMessage(content=f"Get news for {ticker}")]
        })
        

        technical_task = financial_data_agent.ainvoke({
            "messages": [HumanMessage(content=f"Get technical indicators for {ticker}")]
        })

        company_task = company_fundamental_agent.ainvoke({
            "messages": [HumanMessage(content=f"Get company fundamentals for {ticker}")]
        })
        
        # Execute all sub-agents in parallel
        print(f"🔄 Orchestrator Agent: Running 4 sub-agents in parallel...")
        stock_result, news_result, technical_result, company_result = await asyncio.gather(
            stock_task, news_task, technical_task, company_task, return_exceptions=True
        )
        
        # Handle results and store in state
        state["stock_data"] = stock_result if not isinstance(stock_result, Exception) else {"error": str(stock_result)}
        state["news_data"] = news_result if not isinstance(news_result, Exception) else {"error": str(news_result)}
        state["technical_data"] = technical_result if not isinstance(technical_result, Exception) else {"error": str(technical_result)}
        state["company_data"] = company_result if not isinstance(company_result, Exception) else {"error": str(company_result)}
        
        print(f"✅ Orchestrator Agent: All sub-agents completed")
        
        print("----"*10)
        print('state["stock_data"]')
        print("----"*10)
        print(state["stock_data"])
        print("\n"*5)


        print("----"*10)
        print('state["news_data"]')
        print("----"*10)
        print(state["news_data"])
        print("\n"*5)

        print("----"*10)
        print('state["technical_data"]')
        print("----"*10)
        print(state["technical_data"])
        print("\n"*5)

        print("----"*10)
        print('state["company_data"]')
        print("----"*10)
        print(state["company_data"])
        print("\n"*5)

        return state
        
    except Exception as e:
        print(f"❌ Orchestrator Agent: Error in parallel execution - {str(e)}")
        state["stock_data"] = {"error": f"Failed to fetch stock data: {str(e)}"}
        state["news_data"] = {"error": f"Failed to fetch news: {str(e)}"}
        state["technical_data"] = {"error": f"Failed to fetch technical data: {str(e)}"}
        state["company_data"] = {"error": f"Failed to fetch company fundamentals: {str(e)}"}
        return state

async def final_summary_node(state: FinancialAnalysisState) -> FinancialAnalysisState:
    """Node where orchestrator agent provides final comprehensive summary"""
    try:
        print(f"📊 Orchestrator Agent: Creating comprehensive summary...")
        
        # Create a comprehensive summary prompt with all collected data
        summary_prompt = f"""
        As the Financial Analysis Orchestrator Agent, create a comprehensive financial analysis summary for {state['ticker']} based on the following data collected from your sub-agents:

        STOCK DATA (from StockPriceAgent):
        {state.get('stock_data', {})}

        NEWS DATA (from CompanyNewsAgent):
        {state.get('news_data', {})}

        TECHNICAL DATA (from FinancialAgent):
        {state.get('technical_data', {})}

        Provide a professional, comprehensive analysis that includes:

        1. **Current Stock Performance**: Analyze current price, volume, market cap, and key metrics
        2. **Key News Highlights**: Summarize important news and their potential impact
        3. **Technical Analysis**: Interpret technical indicators and trends
        4. **Market Sentiment**: Overall market perception and sentiment
        5. **Investment Considerations**: Clear recommendations and risk factors
        6. **Action Items**: Specific actionable insights for investors

        Be thorough, data-driven, and provide clear, actionable insights.
        """
        
        # Use the orchestrator agent to create the final summary
        result = await orchestrator_agent.ainvoke({
            "messages": [HumanMessage(content=summary_prompt)]
        })
        
        # Fix: Access content directly from AIMessage
        if hasattr(result, 'content'):
            state["final_summary"] = result.content
        elif isinstance(result, dict) and 'messages' in result:
            state["final_summary"] = result['messages'][-1].content if result['messages'] else "Summary generation failed"
        else:
            state["final_summary"] = "Summary generation failed"
        
        print(f"✅ Orchestrator Agent: Final summary completed")
        
        return state
        
    except Exception as e:
        print(f"❌ Orchestrator Agent: Error in summary generation - {str(e)}")
        state["final_summary"] = f"Failed to create summary: {str(e)}"
        return state

# Create the workflow graph
def create_financial_analysis_graph() -> Graph:
    """Create the LangGraph workflow with proper orchestrator agent"""
    
    # Create state graph
    workflow = StateGraph(FinancialAnalysisState)
    
    # Add nodes
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("summary_generation", final_summary_node)
    
    # Set entry point
    workflow.set_entry_point("orchestrator")
    
    # Connect orchestrator to final summary
    workflow.add_edge("orchestrator", "summary_generation")
    
    # Set finish point
    workflow.set_finish_point("summary_generation")
    
    return workflow.compile()
