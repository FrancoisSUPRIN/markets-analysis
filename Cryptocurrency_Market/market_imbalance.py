from datetime import datetime, timedelta


class MarketImbalance:
    def __init__(self, imbalance_type, timestamp, open_price, close_price, delta_to_be_filled_in, is_full_filled=False, was_fullfilled_at=None,
                 time_to_be_fullfilled=None, is_partially_filled=False, remaining_delta_open_price=None,
                 remaining_delta_to_be_filled_in=None, candles_of_identification=None, candles_of_fullfilling=None,
                 candles_of_partfilling=None):
        self.imbalance_type = imbalance_type
        self.timestamp = timestamp  # Timestamp (as ID)
        self.open_price = open_price
        self.close_price = close_price
        self.delta_to_be_filled_in = delta_to_be_filled_in
        self.is_full_filled = is_full_filled
        self.was_fullfilled_at = was_fullfilled_at
        self.time_to_be_fullfilled = time_to_be_fullfilled
        self.is_partially_filled = is_partially_filled
        self.remaining_delta_open_price = remaining_delta_open_price
        self.remaining_delta_to_be_filled_in = remaining_delta_to_be_filled_in
        self.candles_of_identification = candles_of_identification
        self.candles_of_fullfilling = candles_of_fullfilling
        self.candles_of_partfilling = candles_of_partfilling
        
    def mark_as_full_filled(self, timestamp):
        self.is_full_filled = True
        self.was_fullfilled_at = timestamp

    def mark_as_partially_filled(self):
        self.is_partially_filled = True

    def update_time_to_be_fullfilled(self, current_candle_timestamp):
        if self.is_partially_filled:
            self.time_to_be_fullfilled = current_candle_timestamp - self.timestamp

    def update_remaining_deltas(self, remaining_delta_open_price, remaining_delta_to_be_filled_in):
        self.remaining_delta_open_price = remaining_delta_open_price
        self.remaining_delta_to_be_filled_in = remaining_delta_to_be_filled_in

    def add_candle_of_identification(self, candle):
        if self.candles_of_identification is None:
            self.candles_of_identification = []
        self.candles_of_identification.append(candle)

    def add_candle_of_fullfilling(self, candle):
        if self.candles_of_fullfilling is None:
            self.candles_of_fullfilling = []
        self.candles_of_fullfilling.append(candle)

    def add_candle_of_partfilling(self, candle):
        if self.candles_of_partfilling is None:
            self.candles_of_partfilling = []
        self.candles_of_partfilling.append(candle)
        
def create_market_imbalance(imbalance_type, timestamp, open_price, close_price, delta_to_be_filled_in,
                                is_full_filled=False, was_fullfilled_at=None, time_to_be_fullfilled=None,
                                is_partially_filled=False, remaining_delta_open_price=None,
                                remaining_delta_to_be_filled_in=None, candles_of_identification=None,
                                candles_of_fullfilling=None, candles_of_partfilling=None):
    return MarketImbalance(
    imbalance_type = imbalance_type,    
    timestamp=timestamp,
    open_price=open_price,
    close_price=close_price,
    delta_to_be_filled_in=delta_to_be_filled_in,
    is_full_filled=is_full_filled,
    was_fullfilled_at=was_fullfilled_at,
    time_to_be_fullfilled=time_to_be_fullfilled,
    is_partially_filled=is_partially_filled,
    remaining_delta_open_price=remaining_delta_open_price,
    remaining_delta_to_be_filled_in=remaining_delta_to_be_filled_in,
    candles_of_identification=candles_of_identification,
    candles_of_fullfilling=candles_of_fullfilling,
    candles_of_partfilling=candles_of_partfilling
    )
    
    
class MarketCandle:
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

def find_imbalances_after_fall(df):
    imbalances_after_fall = []
    for index, row in df.iterrows():
        if index == 0 or index == len(df) - 1:
            continue
        if df['low'][index - 1] > df['high'][index + 1]:
            prev_candle = create_market_candle(df.iloc[index - 1])
            current_candle = create_market_candle(row)
            next_candle = create_market_candle(df.iloc[index + 1])
            delta_to_be_filled_in = float(prev_candle.low_price) - float(next_candle.high_price)
            
            imbalance = create_market_imbalance(
                imbalance_type = "imbalance_after_fall",
                timestamp = current_candle.timestamp,
                open_price = next_candle.high_price,
                close_price = prev_candle.low_price, 
                delta_to_be_filled_in = delta_to_be_filled_in, 
                is_full_filled = False, 
                was_fullfilled_at = None,
                time_to_be_fullfilled = None, 
                is_partially_filled = False, 
                remaining_delta_open_price = None,
                remaining_delta_to_be_filled_in = None, 
                candles_of_identification = (prev_candle, current_candle, next_candle), 
                candles_of_fullfilling = None,
                candles_of_partfilling = None)
            
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
            delta_to_be_filled_in = float(next_candle.low_price) - float(prev_candle.high_price)
            
            imbalance = create_market_imbalance(
                imbalance_type = "imbalance_after_rise",
                timestamp = current_candle.timestamp,
                open_price = next_candle.low_price,
                close_price = prev_candle.high_price, 
                delta_to_be_filled_in = delta_to_be_filled_in, 
                is_full_filled = False, 
                was_fullfilled_at = None,
                time_to_be_fullfilled = None, 
                is_partially_filled = False, 
                remaining_delta_open_price = None,
                remaining_delta_to_be_filled_in = None, 
                candles_of_identification = (prev_candle, current_candle, next_candle), 
                candles_of_fullfilling = None,
                candles_of_partfilling = None)
            
            imbalances_after_rise.append(imbalance)
    return imbalances_after_rise