import pip

#!pip install python-binance
#!pip install pytz


import os
from binance.client import Client
from market_imbalance import MarketCandle
import pandas as pd
import datetime
import pytz

def get_trading_pairs(client):
    # Récupérer la liste des paires de trading disponibles sur Binance
    exchange_info = client.get_exchange_info()
    trading_pairs = [symbol['symbol'] for symbol in exchange_info['symbols']]
    nb_of_trading_pairs = len(exchange_info['symbols'])
    return nb_of_trading_pairs, trading_pairs

def get_available_timeframe_on_this_plateform(client):
    return "ok"

def fetch_ohlcv_as_df(client, symbol, interval, from_date): #Client.KLINE_INTERVAL_1DAY
    candles = client.get_historical_klines(symbol, interval, from_date)
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=False)
    return df

def fetch_ohlcv(client, symbol, interval, from_date): #Client.KLINE_INTERVAL_1DAY
    historical_candles = client.get_historical_klines(symbol, interval, from_date)
    historical_candles = [MarketCandle(*candle) for candle in historical_candles]
    return historical_candles

def adjust_timestamps_to_local(df, timestamp_column):
    # Convertir la colonne de timestamp en datetime
    df[timestamp_column] = pd.to_datetime(df[timestamp_column], unit='ms', utc=True)
    # Convertir le timestamp à l'heure locale
    df[timestamp_column] = df[timestamp_column].dt.tz_convert('Europe/Paris')
    return df
