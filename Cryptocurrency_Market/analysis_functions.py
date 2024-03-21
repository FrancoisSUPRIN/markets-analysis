import pandas as pd
from traitlets import Float

def find_imbalances_after_rise(df):
    # columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
    
    imbalances_after_rise = []
    for i in range(1, len(df)-1):
        if df['high'][i-1] < df['low'][i+1]:
            prev_candle = df.iloc[i-1]
            current_candle = df.iloc[i]
            next_candle = df.iloc[i+1]
            price_difference = float(next_candle['low']) - float(prev_candle['high'])
            imbalance = (*prev_candle, *current_candle, *next_candle, price_difference, current_candle['timestamp'])
            imbalances_after_rise.append(imbalance)
    return imbalances_after_rise

def find_imbalance_after_fall(df):
    # columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
    
    imbalances_after_fall = []
    for i in range(1, len(df)-1):
        if df['low'][i - 1] > df['high'][i + 1]:
            prev_candle = df.iloc[i-1]
            current_candle = df.iloc[i]
            next_candle = df.iloc[i+1]
            price_difference = float(prev_candle['low']) - float(next_candle['high'])
            imbalance = (current_candle.name, price_difference, *prev_candle, *current_candle, *next_candle )
            imbalances_after_fall.append(imbalance)
    return imbalances_after_fall