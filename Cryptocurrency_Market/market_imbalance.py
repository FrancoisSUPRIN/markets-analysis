from datetime import datetime, timedelta
import datetime

class MarketImbalance:
    def __init__(self, imbalance_type, timestamp, open_price, close_price, delta_to_be_filled_in, is_full_filled=False, was_fullfilled_at=None,
                 time_to_be_fullfilled=None, is_partially_filled=False, remaining_delta_open_price=None,
                 remaining_delta_to_be_filled_in=None, candles_of_identification=None, candles_of_fullfilling=None,
                 candles_of_partfilling=None):
        self.imbalance_type = str(imbalance_type)
        self.timestamp = int(timestamp)  # Timestamp (as ID)
        self.open_price = float(open_price)
        self.close_price = float(close_price)
        self.delta_to_be_filled_in = float(delta_to_be_filled_in)
        self.is_full_filled = bool(is_full_filled)
        self.was_fullfilled_at = was_fullfilled_at
        self.time_to_be_fullfilled = time_to_be_fullfilled
        self.is_partially_filled = bool(is_partially_filled)
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
                open_price = float(next_candle.high_price),
                close_price = float(prev_candle.low_price), 
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

def get_fullfilled_imbalances_after_fall(imbalances_after_fall, market_data_df) :
    for imbalance in imbalances_after_fall :
        imbalance_start = (imbalance.timestamp)     
        candles_after_imbalance = market_data_df[market_data_df['timestamp'] > imbalance_start] # filter df on candles after the imbalance
        highest_price_from_now = imbalance.open_price
        
        for index, row in candles_after_imbalance.iterrows() :
            if float(row.high) >= imbalance.close_price :
                MarketImbalance.mark_as_full_filled(imbalance, row['timestamp']) # update is_full_filled=False to True,and replace was_fullfilled_at=None by was_fullfilled_at=candle['timestamp']
                MarketImbalance.update_time_to_be_fullfilled(imbalance, row['timestamp'])
                break

            elif float(row.high) >= float(highest_price_from_now) : 
                highest_price_from_now = row['high']       

    fullfilled_imbalances = list(filter(lambda imbalance: imbalance.is_full_filled, imbalances_after_fall))
    return fullfilled_imbalances

def get_fullfilled_imbalances_after_rise(imbalances_after_rise, market_data_df) :
    for imbalance in imbalances_after_rise :
        imbalance_start = (imbalance.timestamp)     
        candles_after_imbalance = market_data_df[market_data_df['timestamp'] > imbalance_start] # filter df on candles after the imbalance
        lowest_price_from_now = imbalance.open_price
        
        for index, row in candles_after_imbalance.iterrows() :
            if float(row.low) <= imbalance.close_price :
                MarketImbalance.mark_as_full_filled(imbalance, row['timestamp']) # update is_full_filled=False to True,and replace was_fullfilled_at=None by was_fullfilled_at=candle['timestamp']
                MarketImbalance.update_time_to_be_fullfilled(imbalance, row['timestamp'])
                break

            elif float(row.low) <= float(lowest_price_from_now) : 
                highest_price_from_now = row['high']       

    fullfilled_imbalances = list(filter(lambda imbalance: imbalance.is_full_filled, imbalances_after_rise))
    return fullfilled_imbalances

def sort_imbalances_by_timestamp(unfilled_imbalances):
    sorted_imbalances = sorted(unfilled_imbalances, key=lambda imb: imb.timestamp)
    return sorted_imbalances

