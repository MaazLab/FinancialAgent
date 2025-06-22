from langchain_core.tools import tool
import yfinance as yf
import requests
from config import FMP_API_KEY

@tool
async def get_stock_info_yf(ticker_symbol: str) -> dict:
    """
    Fetches key stock information for the given ticker using yfinance.
    """
    print("----"*10)
    print("Tool called: get_stock_info_yf")
    print("----"*10)

    try:
        keys = [
        'dayHigh', 'dayLow', 'previousClose', 'open', 'close',
        'volume', 'lastPrice', 'lastVolume', 'marketCap', 'shares',
        'yearHigh', 'yearLow', 'yearChange'
    ]

        # Fetch the ticker data
        stock = yf.Ticker(ticker_symbol)
        stock_info = stock.fast_info

        result = {}
        for key in keys:
            try:
                # getattr will call fast.__getattr__(key) internally
                value = getattr(stock_info, key)
            except (AttributeError, KeyError):
                # if the scraper didn’t provide that field
                value = None
            result[key] = value
        
        return result
    except Exception as e:
        print(f"Error while getting stock data from yfinance: {e}")
        return {"error": str(e)}

@tool
def get_stock_info_fmp(symbol: str) -> dict:
    """
    Fetches key stock information for the given ticker using financialmodelingprep.
    """
    print("----"*10)
    print("Tool called: get_stock_info_fmp")
    print("----"*10)

    url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}'
    params = {'apikey': FMP_API_KEY}
    q = requests.get(url, params=params).json()[0]

    prev = q.get('previousClose')
    last = q.get('price')

    return {
        'dayHigh':      q.get('dayHigh'),
        'dayLow':       q.get('dayLow'),
        'previousClose': prev,
        'open':         q.get('open'),
        'close':        last,
        'volume':       q.get('volume'),
        'lastPrice':    last,
        'lastVolume':   q.get('volume'),
        'marketCap':    q.get('marketCap'),
        'shares':       q.get('sharesOutstanding'),
        'yearHigh':     q.get('yearHigh'),
        'yearLow':      q.get('yearLow'),
        'yearChange':   q.get('changesPercentage') / 100 if q.get('changesPercentage') else None
    }