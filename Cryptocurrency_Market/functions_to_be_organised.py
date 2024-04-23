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