from langchain_core.tools import tool
import finnhub
from config import FINNHUB_API_KEY

@tool
def get_fundamentals_finnhub(ticker: str) -> dict:
    """
    Fetch company fundamentals data for a NASDAQ ticker using Finnhub.
    """

    print("----"*10)
    print("Tool called: get_fundamentals_finnhub")
    print("----"*10)

    client = finnhub.Client(api_key=FINNHUB_API_KEY)

    company_funamentals_dict = {
                        "Valuation Metrics": {
                            "marketCapitalization": None,
                            "peAnnual": None,
                            "peTTM": None,
                            "peExclExtraAnnual": None,
                            "peExclExtraTTM": None,
                            "peInclExtraTTM": None,
                            "peNormalizedAnnual": None,
                            "peBasicExclExtraTTM": None,
                            "pb": None,
                            "pbAnnual": None,
                            "pbQuarterly": None,
                            "psAnnual": None,
                            "psTTM": None,
                            "ptbvAnnual": None,
                            "ptbvQuarterly": None,
                            "enterpriseValue": None,
                            "currentEv/freeCashFlowAnnual": None,
                            "currentEv/freeCashFlowTTM": None
                        },
                        "Profitability Metrics": {
                            "netProfitMarginAnnual": None,
                            "netProfitMarginTTM": None,
                            "netProfitMargin5Y": None,
                            "grossMarginAnnual": None,
                            "grossMarginTTM": None,
                            "grossMargin5Y": None,
                            "operatingMarginAnnual": None,
                            "operatingMarginTTM": None,
                            "operatingMargin5Y": None,
                            "pretaxMarginAnnual": None,
                            "pretaxMarginTTM": None,
                            "pretaxMargin5Y": None,
                            "ebitdPerShareAnnual": None,
                            "ebitdPerShareTTM": None,
                            "netInterestCoverageAnnual": None,
                            "netInterestCoverageTTM": None
                        },
                        "Growth Metrics": {
                            "revenueGrowth3Y": None,
                            "revenueGrowth5Y": None,
                            "revenueGrowthQuarterlyYoy": None,
                            "revenueGrowthTTMYoy": None,
                            "epsGrowth3Y": None,
                            "epsGrowth5Y": None,
                            "epsGrowthQuarterlyYoy": None,
                            "epsGrowthTTMYoy": None,
                            "dividendGrowthRate5Y": None,
                            "bookValueShareGrowth5Y": None,
                            "revenueShareGrowth5Y": None,
                            "tbvCagr5Y": None,
                            "focfCagr5Y": None,
                            "capexCagr5Y": None,
                            "ebitdaCagr5Y": None,
                            "ebitdaInterimCagr5Y": None,
                            "netMarginGrowth5Y": None
                        },
                        "Dividend and Cash Flow Metrics": {
                            "dividendPerShareAnnual": None,
                            "dividendPerShareTTM": None,
                            "dividendYieldIndicatedAnnual": None,
                            "currentDividendYieldTTM": None,
                            "payoutRatioAnnual": None,
                            "payoutRatioTTM": None,
                            "cashFlowPerShareAnnual": None,
                            "cashFlowPerShareQuarterly": None,
                            "cashFlowPerShareTTM": None,
                            "cashPerSharePerShareAnnual": None,
                            "cashPerSharePerShareQuarterly": None,
                            "pcfShareAnnual": None,
                            "pcfShareTTM": None,
                            "pfcfShareAnnual": None,
                            "pfcfShareTTM": None
                        },
                        "Efficiency Metrics": {
                            "assetTurnoverAnnual": None,
                            "assetTurnoverTTM": None,
                            "inventoryTurnoverAnnual": None,
                            "inventoryTurnoverTTM": None,
                            "receivablesTurnoverAnnual": None,
                            "receivablesTurnoverTTM": None,
                            "netIncomeEmployeeAnnual": None,
                            "netIncomeEmployeeTTM": None,
                            "revenueEmployeeAnnual": None,
                            "revenueEmployeeTTM": None
                        },
                        "Liquidity Metrics": {
                            "currentRatioAnnual": None,
                            "currentRatioQuarterly": None,
                            "quickRatioAnnual": None,
                            "quickRatioQuarterly": None
                        },
                        "Solvency and Leverage Metrics": {
                            "longTermDebt/equityAnnual": None,
                            "longTermDebt/equityQuarterly": None,
                            "totalDebt/totalEquityAnnual": None,
                            "totalDebt/totalEquityQuarterly": None
                        },
                        "Returns": {
                            "roa5Y": None,
                            "roaRfy": None,
                            "roaTTM": None,
                            "roe5Y": None,
                            "roeRfy": None,
                            "roeTTM": None,
                            "roi5Y": None,
                            "roiAnnual": None,
                            "roiTTM": None
                        },
                        "Earnings per Share (EPS) Metrics": {
                            "epsAnnual": None,
                            "epsTTM": None,
                            "epsBasicExclExtraItemsAnnual": None,
                            "epsBasicExclExtraItemsTTM": None,
                            "epsExclExtraItemsAnnual": None,
                            "epsExclExtraItemsTTM": None,
                            "epsInclExtraItemsAnnual": None,
                            "epsInclExtraItemsTTM": None,
                            "epsNormalizedAnnual": None
                        },
                        "Book Value Metrics": {
                            "bookValuePerShareAnnual": None,
                            "bookValuePerShareQuarterly": None,
                            "tangibleBookValuePerShareAnnual": None,
                            "tangibleBookValuePerShareQuarterly": None
                        },
                        "Risk Metric": {
                            "beta": None
                        }
                    }


    try:
        profile = client.company_profile2(symbol=ticker)
        metrics = client.company_basic_financials(symbol=ticker, metric="all")

        for categories in company_funamentals_dict:

            for key in company_funamentals_dict[categories]:
                company_funamentals_dict[categories][key] = metrics['metric'].get(key, None)

        return {
            "profile" : profile,
            # "financials": metrics.get("series", [])
            "financials": company_funamentals_dict
        }
    except Exception as e:
        return {"error": str(e)}