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