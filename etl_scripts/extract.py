# Loading the necessary packages
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta

########################################

# Load enviroment variables
load_dotenv()

# Load the API KEY stored at the .env file
API_KEY = os.getenv('API_KEY')

########################################

"""
Function: get_currency_exchange_rate(from_currency, to_currency)

Purpose: Get the exchange rate trough the Alpha Vantage API

Input:
    - from_currency: currency you want to convert into another
    - to_currency: currency you want to convert the previous currency into

    Both currencies are represented by the code of the currency
    (USD for US dollars, or EUR for Euros for example), the complete list
    of both crypto and physical currencies available at this endpoint are found
    at the "physical_currency_list.csv" and "digital_currency_list.csv" 

Output:
    - exchange_rate: The value for the exchange rate for the conversion from_currency -> to_currency
    (from_currency = to_currency * exchange_rate)
    - last_refreshed_gmt3: time of data collection converted from the default UTC timezone to GMT-3 timezone
    (for my personal convenience)
"""

def get_currency_exchange_rate(from_currency, to_currency):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": "BRL",
        "to_currency": "USD",
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "Realtime Currency Exchange Rate" in data:
        exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        last_refreshed = data["Realtime Currency Exchange Rate"]["6. Last Refreshed"]
        # Conversion from UTC to GMT-3
        last_refreshed_utc = datetime.strptime(last_refreshed, "%Y-%m-%d %H:%M:%S")
        last_refreshed_gmt3 = last_refreshed_utc - timedelta(hours=3)
        return exchange_rate, last_refreshed_gmt3
    else:
        print(f"Erro ao buscar cotação de {from_currency} para {to_currency}.")
        return None, None



"""
Function: get_stock_data(symbol, name)

Purpose: Get the exchange rate trough the Alpha Vantage API

Input:
    - symbol: Stock code at the stock market
    - name: name of the stock the code represents
    ("PEP" is the code for "PepsiCo Inc" and "T" is the code for "AT&T Inc" for example) 

Output: data frame with the following structure
    - date: date of the last closing of market transactions
    - stock_code: symbol,
    - stock_name: name,
    - stock_value: the value that the stock closed at
"""
def get_stock_data(symbol, name):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" in data:
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index", dtype=float)
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. adjusted close": "Adj Close",
            "6. volume": "Volume"
        })
        df.index = pd.to_datetime(df.index)
        
        # Selecionar a data mais recente
        latest_date = df.index.max()
        latest_close = df.loc[latest_date, "Close"]

        # Criar a tabela consolidada
        return {
            "date": latest_date.strftime("%Y-%m-%d"),
            "stock_code": symbol,
            "stock_name": name,
            "stock_value": latest_close
        }
    else:
        print(f"Erro ao buscar dados para {symbol}: {data.get('Note', 'Sem mensagem de erro')}")
        return None



"""
Function: load_config(file_path)

Purpose: read the .json with the detailes of the stocks and currencies to be collected

Input:
    - file_path: path of the .json that has the details for the stocks and the currencies to be collected

Output: 
    - the data stored in the file
"""
def load_config(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
    


"""
Function: fetch_all_stocks(config_file)

Purpose: This function collects the data for every stock that is stored at the .json file, while storing and 
transforming it into a data frame at the format of the database for easier integration with the power bi and tableu

Input:
    - file_path: path of the .json that has the details for the stocks and the currencies to be collected 

Output: 
    - data frame formated to be ready for database implementation

"""
def fetch_all_stocks(file_path):
    config = load_config(file_path)
    results = []

    for stock_key, stock_data in config["stocks"].items():
        stock_code = stock_data["code"]
        stock_name = stock_data["name"]
        result = get_stock_data(stock_code, stock_name)
        if result:
            results.append(result)

    # Turn results into a dataframe
    return pd.DataFrame(results)



"""
Function: fetch_all_stocks(config_file)

Purpose: This function collects the data for every stock that is stored at the .json file, while storing and 
transforming it into a data frame at the format of the database for easier integration with the power bi and tableu

Input:
    - file_path: path of the .json that has the details for the stocks and the currencies to be collected 

Output: 
    - data frame formated to be ready for database implementation

"""
def fetch_currency_data(file_path):
    config = load_config(file_path)
    exchange_data = []
    for key, conversion in config["conversions"].items():
        rate, last_refreshed = get_currency_exchange_rate(
            conversion["from_currency"], conversion["to_currency"]
        )
        if rate is not None:
            exchange_data.append({
                "data": last_refreshed,
                "from_currency": conversion["from_currency"],
                "to_currency": conversion["to_currency"],
                "exchange_rate": rate
            })
    return pd.DataFrame(exchange_data)




# script to execute the code
if __name__ == "__main__":

    # Get stock data
    stock_df = fetch_all_stocks("follow_list.json")
    stock_df.to_csv("stock_data.csv", index=False)

    # Get currency data
    currency_df = fetch_currency_data("follow_list.json")
    currency_df.to_csv("currency_exchange_rates.csv", index=False)

