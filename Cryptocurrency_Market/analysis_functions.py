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
            imbalance = (current_candle['timestamp'], price_difference, prev_candle['timestamp'], next_candle['timestamp'], [*prev_candle], [*current_candle], [*next_candle])
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
            imbalance = (current_candle['timestamp'], price_difference, prev_candle['timestamp'], next_candle['timestamp'], [*prev_candle], [*current_candle], [*next_candle])
            imbalances_after_fall.append(imbalance)
    return imbalances_after_fall


"""class MarketCandle:
    def __init__(self, timestamp, open_price, high_price, low_price, close_price, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore):
        self.timestamp = timestamp
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
        self.close_time = close_time
        self.quote_asset_volume = quote_asset_volume
        self.number_of_trades = number_of_trades
        self.taker_buy_base_asset_volume = taker_buy_base_asset_volume
        self.taker_buy_quote_asset_volume = taker_buy_quote_asset_volume
        self.ignore = ignore

def create_market_candle(row):
    return MarketCandle(
        timestamp=row['timestamp'],
        open_price=row['open'],
        high_price=row['high'],
        low_price=row['low'],
        close_price=row['close'],
        volume=row['volume'],
        close_time=row['close_time'],
        quote_asset_volume=row['quote_asset_volume'],
        number_of_trades=row['number_of_trades'],
        taker_buy_base_asset_volume=row['taker_buy_base_asset_volume'],
        taker_buy_quote_asset_volume=row['taker_buy_quote_asset_volume'],
        ignore=row['ignore']
    )

def find_imbalance_after_fall(df):
    imbalances_after_fall = []
    for index, row in df.iterrows():
        if index == 0 or index == len(df) - 1:
            continue
        if df['low'][index - 1] > df['high'][index + 1]:
            prev_candle = create_market_candle(df.iloc[index - 1])
            current_candle = create_market_candle(row)
            next_candle = create_market_candle(df.iloc[index + 1])
            price_difference = prev_candle.low_price - next_candle.high_price
            imbalance = (index, price_difference, prev_candle, current_candle, next_candle)
            imbalances_after_fall.append(imbalance)
    return imbalances_after_fall

def find_imbalances_after_rise(df):
    imbalances_after_rise = []
    for index, row in df.iterrows():
        if index == 0 or index == len(df) - 1:
            continue
        if df['high'][index - 1] < df['low'][index + 1]:
            prev_candle = create_market_candle(df.iloc[index - 1])
            current_candle = create_market_candle(row)
            next_candle = create_market_candle(df.iloc[index + 1])
            price_difference = next_candle.low_price - prev_candle.high_price
            imbalance = (index, price_difference, prev_candle, current_candle, next_candle)
            imbalances_after_rise.append(imbalance)
    return imbalances_after_rise"""