# AI-Powered Financial Analysis System

A sophisticated multi-agent financial analysis platform that provides institutional-grade stock analysis using LangGraph, LangChain, and multiple financial data APIs.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI WEB SERVER                       │
│                     (Port 8000)                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                LANGGRAPH WORKFLOW ENGINE                    │
│              (Parallel Agent Orchestration)                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR AGENT (MASTER)                    │
│              (Senior Financial Analyst)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              PARALLEL EXECUTION OF 4 AGENTS                 │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐  │
│  │Stock Price  │Company News │Financial    │Company      │  │
│  │Agent        │Agent        │Agent        │Fundamental  │  │
│  │             │             │             │Agent        │  │
│  └─────────────┴─────────────┴─────────────┴─────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              FINAL SUMMARY SYNTHESIS                        │
│              (Institutional-Grade Report)                   │
└─────────────────────────────────────────────────────────────┘
```

## Workflow Process

### Step 1: API Request Reception
- User sends POST request to `/analyze` endpoint with stock ticker
- FastAPI validates request format using Pydantic models
- System initializes LangGraph workflow state

### Step 2: Workflow Initialization
- Creates initial state with empty data containers
- Sets up LangSmith tracing for observability
- Prepares parallel execution environment

### Step 3: Orchestrator Node Execution
- Orchestrator Agent receives the ticker symbol
- Creates 4 parallel tasks for specialized agents
- Uses `asyncio.gather()` for concurrent execution
- Monitors all agent executions simultaneously

### Step 4: Parallel Agent Execution
All 4 agents run simultaneously:

1. **Stock Price Agent**: Fetches real-time market data
2. **Company News Agent**: Gathers recent news and sentiment
3. **Financial Agent**: Collects technical indicators
4. **Company Fundamental Agent**: Retrieves financial ratios

### Step 5: Data Collection & State Update
- Each agent returns structured data to the orchestrator
- Results are stored in the workflow state
- Error handling ensures partial data recovery

### Step 6: Final Summary Generation
- Orchestrator Agent synthesizes all collected data
- Uses professional prompt template for comprehensive analysis
- Generates institutional-grade final summary

### Step 7: Response Processing
- FastAPI extracts data from tool messages
- Structures response according to Pydantic models
- Returns comprehensive analysis to user

## Features

- **Multi-Agent Architecture**: 5 specialized AI agents working in parallel
- **Parallel Processing**: All data sources fetched simultaneously
- **Fault Tolerance**: Multiple fallback APIs for each data type
- **Comprehensive Analysis**: Price, news, technical, and fundamental data
- **Institutional Grade**: Professional analysis suitable for portfolio managers
- **Full Observability**: LangSmith tracing for debugging and monitoring
- **Real-time Data**: Live market data from multiple sources

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit `config.py` and add your API keys:
```python
OPENAI_API_KEY = 'your-openai-key'
FINNHUB_API_KEY = 'your-finnhub-key'
ALPHA_VANTAGE_API_KEY = 'your-alpha-vantage-key'
TWELVEDATA_API_KEY = 'your-twelvedata-key'
FMP_API_KEY = 'your-fmp-key'
LANGSMITH_API_KEY = 'your-langsmith-key'
```

### 3. Start the Server
```bash
python app.py
```

### 4. Test the API
```bash
# Health check
curl http://localhost:8002/health

# Analyze a stock
curl -X POST "http://localhost:8002/analyze" \
     -H "Content-Type: application/json" \
     -d '{"ticker": "AAPL"}'
```

## Agent System Overview

### Orchestrator Agent (Master)
**Role**: Senior Financial Analyst & Project Manager

**Responsibilities**:
- Strategic Coordination: Lead and coordinate a team of specialized financial analysis agents
- Data Synthesis: Integrate comprehensive financial data from multiple sources
- Professional Analysis: Deliver institutional-grade financial analysis and insights
- Risk Assessment: Provide thorough risk evaluation and investment considerations
- Quality Control: Ensure all analysis meets institutional standards
- Final Report Generation: Create comprehensive, actionable investment intelligence

**Workflow Role**:
- Initialization: Receives stock ticker and initiates parallel analysis
- Parallel Execution: Coordinates execution of 4 specialized sub-agents simultaneously
- Data Collection: Collects and validates all agent outputs with error handling
- Data Integration: Combines disparate data sources into unified analysis
- Professional Synthesis: Uses advanced AI to create institutional-grade final summary
- Quality Assurance: Ensures professional standards and balanced perspectives
- Final Delivery: Provides comprehensive report with actionable insights

**Status**: Working

### Stock Price Agent
**Role**: Market Data Analyst

**Responsibilities**:
- Real-time Market Data Analysis: Live price feeds, volume patterns, and market dynamics
- Technical Price Analysis: Support/resistance levels, price momentum, and volatility assessment
- Market Microstructure: Order flow analysis, liquidity assessment, and market depth evaluation
- Comparative Analysis: Peer comparison and sector relative performance
- Market Sentiment Assessment: Institutional flow analysis and investor sentiment evaluation

**Tools**:
- **`get_stock_data_tool`**: Yahoo Finance API (Primary)
  - Fetches comprehensive real-time market data including price, volume, market cap
  - Provides day high/low, previous close, open price, and year-to-date performance
  - High reliability with extensive coverage of global markets
- **`get_stock_info_fmp`**: Financial Modeling Prep API (Fallback)
  - Secondary validation source for stock data
  - Additional market metrics and validation capabilities
  - Ensures data accuracy and completeness when primary source fails

**Status**: Working

### Company News Agent
**Role**: Market Intelligence Analyst

**Responsibilities**:
- Financial News Analysis: Critical evaluation of market-moving news and events
- Sentiment Analysis: Market reaction assessment and investor sentiment evaluation
- Event Impact Assessment: Analysis of news impact on stock performance and market dynamics
- Regulatory and Corporate Event Monitoring: Earnings, M&A, regulatory changes, and corporate actions
- Strategic Intelligence: Investment implications and timing considerations

**Tools**:
- **`get_company_news_tool`**: Finnhub News API (Primary)
  - Fetches recent financial news articles for the specified ticker
  - Provides headlines, summaries, sources, and publication dates
  - Configurable date range for news retrieval (default: 7 days)
  - Professional financial news sources with high relevance

**Status**: Working

### Financial Agent
**Role**: Technical Analysis Specialist

**Responsibilities**:
- Advanced Technical Analysis: Multi-timeframe analysis and indicator synthesis
- Quantitative Modeling: Statistical analysis and probability assessment
- Market Trend Analysis: Trend identification, strength measurement, and reversal detection
- Risk Management: Volatility analysis and position sizing recommendations
- Trading Signal Generation: Clear entry/exit signals and risk-reward assessment

**Tools**:
- **`get_technical_indicators_twelvedata_tool`**: Twelve Data API (Primary)
  - Fetches comprehensive technical indicators including RSI, SMA, MACD, Bollinger Bands
  - Provides EMA, VWAP, and Stochastic oscillator data
  - Real-time data with 100-day historical analysis
  - Professional-grade technical analysis capabilities
- **`get_technical_indicators_alpha_vantage_tool`**: Alpha Vantage API (Fallback)
  - Alternative source for technical indicators
  - Provides RSI, SMA, EMA, and Stochastic data
  - Monthly interval analysis with error handling
  - Ensures reliability when primary source is unavailable

**Status**: Working

### Company Fundamental Agent
**Role**: Fundamental Analysis Specialist

**Responsibilities**:
- Financial Statement Analysis: Comprehensive evaluation of income statements, balance sheets, and cash flow statements
- Valuation Modeling: DCF analysis, comparable company analysis, and intrinsic value assessment
- Financial Ratio Analysis: Profitability, efficiency, liquidity, and solvency metrics
- Industry and Peer Analysis: Competitive positioning and sector benchmarking
- Long-term Investment Assessment: Growth potential and sustainability analysis

**Tools**:
- **`get_fundamental_analysis_tool`**: Finnhub Fundamentals API
  - Fetches comprehensive fundamental analysis data
  - Provides valuation metrics (P/E, P/B, P/S ratios, enterprise value)
  - Includes profitability metrics (margins, ROE, ROA)
  - Offers growth metrics (revenue growth, EPS growth)
  - Contains dividend metrics (yield, payout ratio)

**Status**: Working

## Tools Overview

### Data Fetching Tools

#### Stock Data Tools (`tools/stock_data_tool.py`)
- **`get_stock_data_tool`**: Primary tool using Yahoo Finance API for real-time market data
  - Fetches current price, volume, market cap, day high/low, previous close
  - Provides year-to-date performance and technical levels
  - Automatic fallback to FMP API if Yahoo Finance fails
- **`get_stock_info_fmp`**: Fallback tool using Financial Modeling Prep API
  - Secondary validation source for stock data
  - Additional market metrics and validation capabilities
  - Ensures data accuracy and completeness

#### News Tools (`tools/company_news_tool.py`)
- **`get_company_news_tool`**: Finnhub News API for professional financial news
  - Fetches recent news articles with configurable date range
  - Provides headlines, summaries, sources, and publication dates
  - High-quality, curated financial news sources

#### Technical Analysis Tools (`tools/technical_indicator_tool.py`)
- **`get_technical_indicators_twelvedata_tool`**: Primary tool using Twelve Data API
  - Comprehensive technical indicators suite (RSI, SMA, MACD, Bollinger Bands)
  - Real-time data with 100-day historical analysis
  - Professional-grade technical analysis capabilities
- **`get_technical_indicators_alpha_vantage_tool`**: Fallback tool using Alpha Vantage API
  - Alternative source for technical indicators
  - Monthly interval analysis with error handling
  - Ensures reliability when primary source is unavailable

#### Fundamental Analysis Tools (`tools/company_fundamentals_tool.py`)
- **`get_fundamental_analysis_tool`**: Finnhub Fundamentals API for financial ratios
  - Comprehensive fundamental analysis including valuation, profitability, and growth metrics
  - Company profile and basic financials
  - Professional-grade financial data with extensive coverage

## API Endpoints

### POST `/analyze`
Main analysis endpoint that triggers the complete workflow.

**Request:**
```json
{
    "ticker": "AAPL"
}
```

**Response:**
```json
{
    "stock_data": {
        "data": {
            "lastPrice": 150.25,
            "volume": 50000000,
            "marketCap": 2500000000000,
            "dayHigh": 152.00,
            "dayLow": 148.50,
            "previousClose": 149.80
        },
        "source": "yfinance"
    },
    "news_data": [
        {
            "datetime": "2024-01-15T10:30:00",
            "headline": "Apple Reports Strong Q4 Earnings",
            "summary": "Apple Inc. reported better-than-expected quarterly results...",
            "url": "https://example.com/news/article"
        }
    ],
    "technical_data": {
        "data": {
            "RSI": [...],
            "SMA": [...],
            "MACD": [...],
            "Bollinger_Bands": [...]
        },
        "source": "twelvedata"
    },
    "company_data": {
        "profile": {...},
        "financials": {
            "Valuation Metrics": {...},
            "Profitability Metrics": {...},
            "Growth Metrics": {...}
        }
    },
    "final_summary": "Comprehensive AI-generated analysis of the stock including market performance, news impact, technical indicators, and fundamental valuation..."
}
```

### GET `/health`
Health check endpoint.
```json
{
    "status": "ok"
}
```

## Configuration

### Required API Keys
- **OpenAI**: GPT-4o-mini for AI analysis
- **Finnhub**: News and fundamentals data
- **Alpha Vantage**: Technical indicators (fallback)
- **Twelve Data**: Technical indicators (primary)
- **Financial Modeling Prep**: Stock data (fallback)
- **LangSmith**: AI observability and tracing

### Environment Variables
```bash
LANGSMITH_API_KEY=your-langsmith-key
LANGCHAIN_TRACING_V2=true
```

## Project Structure

```
financial_analysis/
├── app.py                           # FastAPI web server
├── config.py                        # API keys and configuration
├── workflow.py                      # LangGraph workflow orchestration
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── agents/                          # AI agent implementations
│   ├── orchestrator_agent.py        # Master coordinator agent
│   ├── stock_price_agent.py         # Market data analysis
│   ├── company_news_agent.py        # News and sentiment analysis
│   ├── financial_agent.py           # Technical analysis
│   └── company_fundamental_agent.py # Fundamental analysis
└── tools/                           # Data fetching tools
    ├── stock_data_tool.py           # Stock price data (yfinance + FMP)
    ├── company_news_tool.py         # News data (Finnhub + RSS)
    ├── technical_indicator_tool.py  # Technical analysis (TwelveData + Alpha Vantage)
    └── company_fundamentals_tool.py # Fundamentals (Finnhub)
```

## Development

### Running in Development Mode
```bash
python app.py
```
The server runs with auto-reload enabled on `http://localhost:8002`

### Interactive API Documentation
Visit `http://localhost:8002/docs` for Swagger UI documentation.

### LangSmith Tracing
Monitor agent execution and debug issues at [LangSmith Dashboard](https://smith.langchain.com/)

## Use Cases

This system is designed for:
- **Institutional Investors**: Portfolio managers, hedge funds
- **Financial Advisors**: Client portfolio analysis
- **Research Institutions**: Financial data aggregation
- **Trading Platforms**: Real-time market intelligence
- **Investment Banks**: Equity research and analysis

## Troubleshooting

### Common Issues

1. **"Address already in use"**
   ```bash
   pkill -f "python app.py"
   python app.py
   ```

2. **API Key Errors**
   - Verify all API keys in `config.py`
   - Check API rate limits and quotas

3. **Data Source Failures**
   - System automatically uses fallback sources
   - Check logs for specific error messages

4. **LangSmith Tracing Issues**
   - Verify `LANGSMITH_API_KEY` is set
   - Check LangSmith dashboard for traces

### Debug Mode
Enable detailed logging by setting:
```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"
```

## Performance

- **Parallel Execution**: All 4 agents run simultaneously
- **Response Time**: ~10-30 seconds for complete analysis
- **Data Sources**: 5 financial APIs with fallback mechanisms
- **Scalability**: Modular architecture for easy expansion


## Assumptions
- *Requirement Interpretation*: The requirement mentioned a chat agent and an endpoint. To meet the core objective, we implemented a single /analyze endpoint rather than a separate chat interface.
- *Orchestration*: A dedicated orchestrator agent manages parallel execution of four specialized agents to ensure coordinated data collection and synthesis.
- *Agent Expansion*: Although three sub-agents were implied, we included four (Price, News, Technical, Fundamentals) to deliver a more comprehensive analysis.