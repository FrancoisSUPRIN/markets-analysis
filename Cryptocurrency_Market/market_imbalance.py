from datetime import datetime, timedelta
import numpy as np

# Classe représentant une imbalance sur le marché
class MarketImbalance:
    def __init__(
        self,
        imbalance_type,
        timestamp,
        open_price,
        close_price,
        delta_to_be_filled_in,
        is_full_filled=False,
        was_fullfilled_at=None,
        time_to_be_fullfilled=None,
        is_partially_filled=False,
        remaining_delta_open_price=None,
        remaining_delta_to_be_filled_in=None,
        candles_of_identification=None,
        candles_of_fullfilling=None,
        candles_of_partfilling=None,
        elapsed_time_since_creation=None,
    ):
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
        self.elapsed_time_since_creation = elapsed_time_since_creation

    def mark_as_full_filled(self, timestamp):
        self.is_full_filled = True
        self.was_fullfilled_at = timestamp
        self.elapsed_time_since_creation = None  # L'imbalance est comblée

    def mark_as_partially_filled(self):
        self.is_partially_filled = True

    def update_time_to_be_fullfilled(self, current_candle_timestamp):
        self.time_to_be_fullfilled = current_candle_timestamp - self.timestamp

    def update_elapsed_time_since_creation(self, current_time):
        if not self.is_full_filled:
            self.elapsed_time_since_creation = current_time - self.timestamp

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



