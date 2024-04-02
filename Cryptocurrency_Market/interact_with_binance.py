import pip

#!pip install python-binance
#!pip install pytz


import os
from binance.client import Client
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
    candles = client.get_historical_klines(symbol, interval, from_date)
    return candles

def adjust_timestamps_to_local(df, timestamp_column):
    # Convertir la colonne de timestamp en datetime
    df[timestamp_column] = pd.to_datetime(df[timestamp_column], unit='ms', utc=True)
    # Convertir le timestamp à l'heure locale
    df[timestamp_column] = df[timestamp_column].dt.tz_convert('Europe/Paris')
    return df


class Trade:
    def __init__(self, res):
        self.event_type = res["e"]
        self.event_time = datetime.datetime.fromtimestamp(res['E'] / 1000, tz=datetime.timezone.utc)
        self.event_time = self.event_time.astimezone(pytz.timezone('Europe/Paris'))
        self.symbol = res["s"]
        self.trade_id = res["t"]
        self.price = float(res["p"])  # Convertir le prix en float
        self.quantity = float(res["q"])  # Convertir la quantité en float
        self.buyer_order_id = res["b"]
        self.selle_order_id = res["a"]
        self.trade_time = datetime.datetime.fromtimestamp(res['T'] / 1000, tz=datetime.timezone.utc)
        self.trade_time = self.trade_time.astimezone(pytz.timezone('Europe/Paris'))
        self.is_the_buyer_the_market_maker = res["m"]
        self.ignore = res["M"]
