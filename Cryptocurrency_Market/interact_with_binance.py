import pip

#!pip install python-binance

import os
from binance.client import Client
import pandas as pd

def get_trading_pairs(client):
    # Récupérer la liste des paires de trading disponibles sur Binance
    exchange_info = client.get_exchange_info()
    trading_pairs = [symbol['symbol'] for symbol in exchange_info['symbols']]
    nb_of_trading_pairs = len(exchange_info['symbols'])
    return nb_of_trading_pairs, trading_pairs

def get_available_timeframe_on_this_plateform(client):
    return "ok"

def fetch_ohlcv(client, symbol = "BTCUSDT", interval='1D', from_date= "1 Jan, 2015"):
    candles = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, from_date)
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df