from langchain_core.tools import tool
from alpha_vantage.techindicators import TechIndicators
from twelvedata import TDClient, exceptions
from requests.exceptions import RequestException
from config import ALPHA_VANTAGE_API_KEY, TWELVEDATA_API_KEY

@tool
async def get_technical_indicators_alpha_vantage_tool(ticker: str) -> dict:
    """
    Fetch RSI, SMA, EMA, and STOCH indicators for the given NASDAQ ticker using Alpha Vantage API.
    """
    print("----"*10)
    print("Tool called: get_technical_indicators_alpha_vantage_tool")
    print("----"*10)

    try:
        ti = TechIndicators(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        indicators = {}

        # Helper to fetch and handle indicator data
        def safe_fetch(fetch_func, name, *args, **kwargs):
            try:
                data, meta = fetch_func(*args, **kwargs)
                if data.empty or "Note" in meta.get("Information", "") or "Error Message" in meta.get("Information", ""):
                    print(f"Warning: No data or access issue for {name} of {ticker}")
                    return None
                return data
            except RequestException as re:
                print(f"Network error while fetching {name} for {ticker}: {re}")
                return None
            except Exception as ex:
                print(f"Error while fetching {name} for {ticker}: {ex}")
                return None

        # Fetch each indicator with error handling
        indicators["RSI"] = safe_fetch(ti.get_rsi, "RSI", symbol=ticker, interval='monthly', time_period=14, series_type='close')
        indicators["SMA"] = safe_fetch(ti.get_sma, "SMA", symbol=ticker, interval='monthly', time_period=14, series_type='close')
        indicators["EMA"] = safe_fetch(ti.get_ema, "EMA", symbol=ticker, interval='monthly', time_period=14, series_type='close')
        indicators["STOCH"] = safe_fetch(ti.get_stoch, "STOCH", symbol=ticker, interval='monthly',)
        indicators["ADX"] = safe_fetch(ti.get_adx, "ADX", symbol=ticker, interval='monthly', time_period=14)
        indicators["CCI"] = safe_fetch(ti.get_cci, "CCI", symbol=ticker, interval='monthly', time_period=14)
        indicators["BBANDS"] = safe_fetch(ti.get_bbands, "BBANDS", symbol=ticker, interval='monthly', time_period=14, series_type='close')
        indicators["AROON"] = safe_fetch(ti.get_aroon, "AROON", symbol=ticker, interval='monthly', time_period=14, series_type='close')

        return {"data": indicators}

    except Exception as e:
        print(f"General error in fetching indicators for {ticker}: {e}")
        return {"error": str(e)}

@tool
async def get_technical_indicators_twelvedata_tool(ticker: str) -> dict:
    """
    Fetch daily OHLC, volume, RSI, SMA and MACD for a given NASDAQ ticker via Twelve Data.
    """
    print("----"*10)
    print("Tool called: get_technical_indicators_twelvedata_tool")
    print("----"*10)

    try:
        td = TDClient(apikey=TWELVEDATA_API_KEY)

        # Build the time series request and chain indicators
        ts = (
            td.time_series(
                symbol=ticker,
                interval="1day",
                outputsize=100
            )
            .with_rsi(time_period=14, series_type="close")
            .with_sma(time_period=14, series_type="close")
            .with_cci(time_period=14, )
            .with_bbands(time_period=14, series_type="close")
            .with_ema(time_period=14, series_type="close")
            .with_adx(time_period=14, )
            .with_stoch()
            .with_aroon(time_period=14, )
        ).without_ohlc()

        # Execute and get JSON-serializable data
        data = ts.as_json()
        return {"data": data}

    except exceptions.TwelveDataError as e:
        return {"error": f"Twelve Data API error: {e}"}
    except RequestException as e:
        return {"error": f"Network error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}
