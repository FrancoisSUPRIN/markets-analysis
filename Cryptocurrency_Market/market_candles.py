class MarketCandle:
    def __init__(self, 
        timestamp, 
        open_price, 
        high_price, 
        low_price, 
        close_price, 
        volume, 
        close_time, 
        quote_asset_volume, 
        number_of_trades, 
        taker_buy_base_asset_volume, 
        taker_buy_quote_asset_volume, 
        ignore,
    ):
        self.timestamp = int(timestamp)
        self.open_price = float(open_price)
        self.high_price = float(high_price)
        self.low_price = float(low_price)
        self.close_price = float(close_price)
        self.volume = float(volume)
        self.close_time = int(close_time)
        self.quote_asset_volume = float(quote_asset_volume)
        self.number_of_trades = int(number_of_trades)
        self.taker_buy_base_asset_volume = float(taker_buy_base_asset_volume)
        self.taker_buy_quote_asset_volume = float(taker_buy_quote_asset_volume)
        self.ignore = ignore
        
class MarketCandleV2:
    def __init__(self, res):
        self.timestamp = int(res[0])
        self.open_price = float(res[1])
        self.high_price = float(res[2])
        self.low_price = float(res[3])
        self.close_price = float(res[4])
        self.volume = float(res[5])
        self.close_time = int(res[6])
        self.quote_asset_volume = float(res[7])
        self.number_of_trades = int(res[8])
        self.taker_buy_base_asset_volume = float(res[9])
        self.taker_buy_quote_asset_volume = float(res[10])
        self.ignore = res[11]
        
        # Example
        # from market_candles import MarketCandleV2
        # responses = client.get_historical_klines(symbol, interval_value, from_date)
        # historical_candles_v2 = [MarketCandleV2(res) for res in responses]
        # historical_candles_v2

def create_market_candle_from_dataframe(row): # compatible with Binance Rest API
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