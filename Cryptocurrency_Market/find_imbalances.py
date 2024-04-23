# Fonction pour trouver les imbalances après une baisse
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
            
            imbalance = MarketImbalance(
                imbalance_type="imbalance_after_fall",
                timestamp=current_candle.timestamp,
                open_price=float(next_candle.high_price),
                close_price=float(prev_candle.low_price),
                delta_to_be_filled_in=delta_to_be_filled_in,
                is_full_filled=False,
                was_fullfilled_at=None,
                time_to_be_fullfilled=None,
                is_partially_filled=False,
                remaining_delta_open_price=None,
                remaining_delta_to_be_filled_in=None,
                candles_of_identification=(prev_candle, current_candle, next_candle),
                candles_of_fullfilling=None,
                candles_of_partfilling=None,
                elapsed_time_since_creation=None,
            )
            
            imbalances_after_fall.append(imbalance)
    return imbalances_after_fall

# Fonction pour trouver les imbalances après une hausse
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
            
            imbalance = MarketImbalance(
                imbalance_type="imbalance_after_rise",
                timestamp=current_candle.timestamp,
                open_price=next_candle.low_price,
                close_price=prev_candle.high_price,
                delta_to_be_filled_in=delta_to_be_filled_in,
                is_full_filled=False,
                was_fullfilled_at=None,
                time_to_be_fullfilled=None,
                is_partially_filled=False,
                remaining_delta_open_price=None,
                remaining_delta_to_be_filled_in=None,
                candles_of_identification=(prev_candle, current_candle, next_candle),
                candles_of_fullfilling=None,
                candles_of_partfilling=None,
                elapsed_time_since_creation=None,
            )
            
            imbalances_after_rise.append(imbalance)
    return imbalances_after_rise

# Fonction pour trier les imbalances par timestamp
def sort_imbalances_by_timestamp(unfilled_imbalances):
    sorted_imbalances = sorted(unfilled_imbalances, key=lambda imb: imb.timestamp)
    return sorted_imbalances