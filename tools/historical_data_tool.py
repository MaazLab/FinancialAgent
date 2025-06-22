from langchain_core.tools import tool
import pandas as pd
from pandas_datareader import data as pdr
import datetime
from config import FMP_API_KEY
import requests

@tool
def get_historical_data_stooq(
    ticker: str
) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for the past 6 months for a given ticker symbol using the Stooq data source.

    Parameters:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').

    Returns:
        pd.DataFrame: DataFrame indexed by date with columns ['Open', 'High', 'Low', 'Close', 'Volume'] for the past 6 months.

    Raises:
        ImportError: If pandas_datareader is not installed.
        ValueError: If no data is returned.
        RuntimeError: If fetching data fails.
    """

    print("----"*10)
    print("Tool called: get_historical_data_stooq")
    print("----"*10)

    # Calculate date range: last 6 months (~182 days)
    today = datetime.datetime.now()
    start_date = today - datetime.timedelta(days=182)
    end_date = today

    try:
        data = pdr.DataReader(ticker, 'stooq', start_date, end_date)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch data for {ticker}: {e}")
    
    # Drop incomplete rows
    data.dropna(how='any', inplace=True)
    if data.empty:
        raise RuntimeError(f"No data returned for ticker {ticker}.")


    # Stooq returns data in descending order by date; sort ascending
    data.sort_index(inplace=True)

    # Return only relevant OHLCV columns
    return data[['Open', 'High', 'Low', 'Close', 'Volume']]




@tool
def get_historical_data_fmp(
    ticker: str,
) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for the past six months for a given ticker symbol
    using the Financial Modeling Prep API.

    Parameters:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').

    Returns:
        pd.DataFrame: DataFrame indexed by date with columns ['Open', 'High', 'Low', 'Close', 'Volume']
                      for the past six months.

    Raises:
        ValueError: If ticker is empty.
        RuntimeError: If API key is missing, HTTP request fails, or API returns no data.
    """
    if not ticker:
        raise ValueError("Ticker symbol must be provided.")

    # Obtain API key
    key = FMP_API_KEY
    if not key:
        raise RuntimeError(
            "FMP API key not provided. Set FMP_API_KEY environment variable or pass `api_key` argument."
        )

    # Calculate date range for past 6 months
    end_dt = datetime.date.today()
    start_dt = end_dt - datetime.timedelta(days=183)
    from_date = start_dt.isoformat()
    to_date = end_dt.isoformat()

    # Build request URL
    url = (
        f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}"
        f"?from={from_date}&to={to_date}&apikey={key}"
    )

    # Fetch data
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch data for {ticker}: HTTP {response.status_code}"
        )

    json_data = response.json()
    historical = json_data.get('historical')
    if not historical:
        raise RuntimeError(
            f"No historical data found for ticker {ticker} via FMP API."
        )

    # Convert to DataFrame
    df = pd.DataFrame(historical)
    # Ensure required columns exist
    required_cols = {'date', 'open', 'high', 'low', 'close', 'volume'}
    if not required_cols.issubset(df.columns):
        raise RuntimeError(
            f"Unexpected response format, missing columns: {required_cols - set(df.columns)}"
        )

    # Rename and reformat
    df = df.rename(columns={
        'date': 'Date',
        'open': 'Open',
        'high': 'High',
        'low':  'Low',
        'close':'Close',
        'volume':'Volume'
    })
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)

    return df[['Open', 'High', 'Low', 'Close', 'Volume']]



