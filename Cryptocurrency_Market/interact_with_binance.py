import pip

#!pip install python-binance
#!pip install pytz


import os
from binance.client import Client
from market_candles import MarketCandle
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

def fetch_ohlcv_as_df(client, symbol, interval, from_date):
    candles = client.get_historical_klines(symbol, interval, from_date)
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    
    # Conversion des types de données
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    df['quote_asset_volume'] = df['quote_asset_volume'].astype(float)
    df['number_of_trades'] = df['number_of_trades'].astype(int)
    df['taker_buy_base_asset_volume'] = df['taker_buy_base_asset_volume'].astype(float)
    df['taker_buy_quote_asset_volume'] = df['taker_buy_quote_asset_volume'].astype(float)
    df['ignore'] = df['ignore'].astype(float)  # Assurez-vous que c'est le bon type
    
    df.set_index('timestamp', inplace=True)  # Assurez-vous de conserver l'index après le set_index
    
    return df


def fetch_ohlcv(client, symbol, interval, from_date): #Client.KLINE_INTERVAL_1DAY
    historical_candles = client.get_historical_klines(symbol, interval, from_date)
    historical_candles = [MarketCandle(*candle) for candle in historical_candles]
    return historical_candles

def adjust_timestamps_to_local(df, timestamp_column):
    df[timestamp_column] = pd.to_datetime(df[timestamp_column], unit='ms', utc=True)
    df[timestamp_column] = df[timestamp_column].dt.tz_convert('Europe/Paris')
    return df


