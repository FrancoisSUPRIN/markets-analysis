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

class MarketAccount:
    def __init__(self, assets, total_value):
        self.assets = assets
        self.total_value = total_value
        

class TradedPair:
    def __init__(self, pair, trades, input_value, output_value, won_trades, loss_trades ):
        self.pair = pair
        self.trades = trades
        self.input_value = input_value
        self.output_value = output_value
        self.won_trades = won_trades
        self.loss_trades = loss_trades


class MarketTrade:
    def __init__(self, is_running, order_type, open_price, take_profit, risk_ratio, stop_loss, estimate_gain, realized_gain, open_time, close_time, duration):
        
        self.is_running = is_running
        self.order_type = order_type
        self.open_price = open_price
        self.take_profit = take_profit
        self.risk_ratio = risk_ratio
        self.stop_loss = stop_loss
        self.estimate_gain = estimate_gain
        self.realized_gain = realized_gain
        self.open_time = open_time
        self.close_time = close_time
        self.duration = duration
        

'''from enum import Enum

class Timeframe(Enum):
    D'accord, voici la liste des durées pour chaque intervalle de temps sans "millisecondes" :

- `KLINE_INTERVAL_1MINUTE`: 60000
- `KLINE_INTERVAL_3MINUTE`: 180000
- `KLINE_INTERVAL_5MINUTE`: 300000
- `KLINE_INTERVAL_15MINUTE`: 900000
- `KLINE_INTERVAL_30MINUTE`: 1800000
- `KLINE_INTERVAL_1HOUR`: 3600000
- `KLINE_INTERVAL_2HOUR`: 7200000
- `KLINE_INTERVAL_4HOUR`: 14400000
- `KLINE_INTERVAL_6HOUR`: 21600000
- `KLINE_INTERVAL_8HOUR`: 28800000
- `KLINE_INTERVAL_12HOUR`: 43200000
- `KLINE_INTERVAL_1DAY`: 86400000
- `KLINE_INTERVAL_3DAY`: 259200000
- `KLINE_INTERVAL_1WEEK`: 604800000
- `KLINE_INTERVAL_1MONTH`: Variable, dépendant du nombre de jours dans le mois'''

        
             
def add_one_minute(timestamp):
    # Convert the timestamp to a datetime object
    dt = datetime.datetime.fromtimestamp(timestamp / 1000)

    # Add one minute to the datetime object
    dt += datetime.timedelta(minutes=1)

    # Convert the updated datetime object back to a timestamp
    updated_timestamp = int(dt.timestamp() * 1000)

    return updated_timestamp