import os
import numpy as np
import pandas as pd
import datetime
import pytz
from binance.client import Client
import plotly.graph_objects as go
import matplotlib.pyplot as plt

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

# Classe représentant une bougie de marché
class MarketCandle:
    def __init__(self, timestamp, open_price, high_price, low_price, close_price, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore):
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

# Fonction de conversion timestamp vers datetime
def convert_ts_to_datetime(ts):
    return datetime.datetime.fromtimestamp(ts / 1000, tz=pytz.timezone('Europe/Paris'))

# Fonction de formatage du temps écoulé
def format_elapsed_time(ms):
    total_seconds = ms / 1000
    days = int(total_seconds // (24 * 3600))
    remainder_seconds = total_seconds % (24 * 3600)
    hours = int(remainder_seconds // 3600)
    remainder_seconds %= 3600
    minutes = int(remainder_seconds // 60)
    seconds = int(remainder_seconds % 60)
    return f"{days}days {hours:02}h:{minutes:02}m:{seconds:02}s"

# Fonction de tri des imbalances par timestamp
def sort_imbalances_by_timestamp(imbalances):
    return sorted(imbalances, key=lambda imb: imb.timestamp)

# Fonction pour trouver les imbalances après une chute
def find_imbalances_after_fall(historical_candles):
    imbalances_after_fall = []
    for index in range(1, len(historical_candles) - 1):
        prev_candle = historical_candles[index - 1]
        current_candle = historical_candles[index]
        next_candle = historical_candles[index + 1]
        if prev_candle.low_price > next_candle.high_price:
            delta_to_be_filled_in = prev_candle.low_price - next_candle.high_price
            imbalance = MarketImbalance(
                imbalance_type="imbalance_after_fall",
                timestamp=current_candle.timestamp,
                open_price=next_candle.high_price,
                close_price=prev_candle.low_price,
                delta_to_be_filled_in=delta_to_be_filled_in,
                candles_of_identification=(prev_candle, current_candle, next_candle),
            )
            imbalances_after_fall.append(imbalance)
    return imbalances_after_fall

# Fonction pour trouver les imbalances après une hausse
def find_imbalances_after_rise(historical_candles):
    imbalances_after_rise = []
    for index in range(1, len(historical_candles) - 1):
        prev_candle = historical_candles[index - 1]
        current_candle = historical_candles[index]
        next_candle = historical_candles[index + 1]
        if prev_candle.high_price < next_candle.low_price:
            delta_to_be_filled_in = next_candle.low_price - prev_candle.high_price
            imbalance = MarketImbalance(
                imbalance_type="imbalance_after_rise",
                timestamp=current_candle.timestamp,
                open_price=next_candle.low_price,
                close_price=prev_candle.high_price,
                delta_to_be_filled_in=delta_to_be_filled_in,
                candles_of_identification=(prev_candle, current_candle, next_candle),
            )
            imbalances_after_rise.append(imbalance)
    return imbalances_after_rise

# Fonction de vérification si les imbalances sont comblés
def check_if_imbalance_filled(imbalances, candles):
    for imbalance in imbalances:
        if imbalance.is_full_filled:
            continue
        relevant_candles = [candle for candle in candles if candle.timestamp > imbalance.timestamp]
        for candle in relevant_candles:
            if imbalance.imbalance_type == "imbalance_after_fall" and candle.high_price >= imbalance.close_price:
                imbalance.mark_as_full_filled(candle.timestamp)
                imbalance.add_candle_of_fullfilling(candle)
                imbalance.update_time_to_be_fullfilled(candle.timestamp)
                break
            elif imbalance.imbalance_type == "imbalance_after_rise" and candle.low_price <= imbalance.close_price:
                imbalance.mark_as_full_filled(candle.timestamp)
                imbalance.add_candle_of_fullfilling(candle)
                imbalance.update_time_to_be_fullfilled(candle.timestamp)
                break

# Fonction pour obtenir les imbalances non comblés
def get_unfilled_imbalances(imbalances):
    return [imbalance for imbalance in imbalances if not imbalance.is_full_filled]

# Fonction pour obtenir les imbalances comblés
def get_fullfilled_imbalances(imbalances):
    return [imbalance for imbalance in imbalances if imbalance.is_full_filled]

# Fonction pour calculer le pourcentage d'imbalances comblés
def calculate_fulfillment_percentage(total_imbalances, fullfilled_imbalances):
    if not total_imbalances:
        raise ValueError("Le nombre total d'imbalances ne peut pas être zéro.")
    return round((len(fullfilled_imbalances) / len(total_imbalances)) * 100, 2)

# Fonction de calcul des statistiques
def calculate_statistics(times_to_fill):
    times_converted = [ms for ms in times_to_fill]
    result = {
        "min": np.min(times_converted),
        "max": np.max(times_converted),
        "mean": np.mean(times_converted),
        "median": np.median(times_converted),
        "std_dev": np.std(times_converted),
        "percentiles": {percentile: np.percentile(times_converted, percentile) for percentile in [25, 50, 75, 80, 90, 95, 98]},
    }
    percentiles = result['percentiles']
    result_as_french = f"""
    Le temps minimum pour combler un imbalance est de {format_elapsed_time(result['min'])}
    Le temps maximum pour combler un imbalance est de {format_elapsed_time(result['max'])}
    La moyenne du temps pour combler un imbalance est de {format_elapsed_time(result['mean'])}
    La médiane du temps pour combler un imbalance est de {format_elapsed_time(result['median'])}
    L'écart-type du temps pour combler un imbalance est de {format_elapsed_time(result['std_dev'])}
    Les percentiles sont les suivants :
        25e percentile: {format_elapsed_time(percentiles[25])}
        50e percentile: {format_elapsed_time(percentiles[50])}
        75e percentile: {format_elapsed_time(percentiles[75])}
        80e percentile: {format_elapsed_time(percentiles[80])}
        90e percentile: {format_elapsed_time(percentiles[90])}
        95e percentile: {format_elapsed_time(percentiles[95])}
        98e percentile: {format_elapsed_time(percentiles[98])}
    """
    return result, result_as_french

# Fonction pour tracer les chandeliers de marché avec les imbalances
def plot_market_candles_with_imbalances(fig, df, all_imbalances):
    for imbalance in all_imbalances:
        fig.add_shape(
            type="rect",
            x0=convert_ts_to_datetime(imbalance.timestamp),
            x1=convert_ts_to_datetime(imbalance.timestamp + 3600000),  # Assuming hourly candles
            y0=imbalance.open_price,
            y1=imbalance.close_price,
            line=dict(color="RoyalBlue" if imbalance.imbalance_type == "imbalance_after_rise" else "Orange"),
        )

# Fonction de tracé de l'histogramme du temps pour combler les imbalances
def plot_fill_time_histogram(bins, median, times_to_fill):
    plt.hist(times_to_fill, bins=bins, alpha=0.75, color='blue', edgecolor='black')
    plt.axvline(median, color='red', linestyle='dashed', linewidth=1, label=f'Median: {format_elapsed_time(median)}')
    plt.xlabel('Time to fill (ms)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Time to Fill Imbalances')
    plt.legend()
    plt.grid(True)
    plt.show()

# Fonction pour récupérer les données OHLCV depuis Binance en DataFrame
def fetch_ohlcv_as_df(client, symbol, interval, from_date):
    klines = client.get_historical_klines(symbol, interval, from_date)
    data = []
    for kline in klines:
        candle = {
            'timestamp': kline[0],
            'open': float(kline[1]),
            'high': float(kline[2]),
            'low': float(kline[3]),
            'close': float(kline[4]),
            'volume': float(kline[5]),
            'close_time': kline[6],
            'quote_asset_volume': float(kline[7]),
            'number_of_trades': kline[8],
            'taker_buy_base_asset_volume': float(kline[9]),
            'taker_buy_quote_asset_volume': float(kline[10]),
            'ignore': kline[11],
        }
        data.append(candle)
    return pd.DataFrame(data)

# Fonction pour créer une MarketCandle à partir d'une DataFrame
def create_market_candle_from_dataframe(row):
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
        ignore=row['ignore'],
    )

# Initialiser les clés API de Binance (utiliser des variables d'environnement pour la sécurité)
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

# Initialiser le client Binance
client = Client(API_KEY, API_SECRET)

# Récupérer les données historiques des chandeliers
symbol = 'BTCUSDT'
interval = Client.KLINE_INTERVAL_1HOUR
from_date = '1 Jan, 2020'
historical_candles_df = fetch_ohlcv_as_df(client, symbol, interval, from_date)

# Convertir la DataFrame en une liste d'objets MarketCandle
historical_candles = [create_market_candle_from_dataframe(row) for index, row in historical_candles_df.iterrows()]

# Identifier les imbalances après une chute et une hausse
imbalances_after_fall = find_imbalances_after_fall(historical_candles)
imbalances_after_rise = find_imbalances_after_rise(historical_candles)

# Combiner les imbalances
all_imbalances = imbalances_after_fall + imbalances_after_rise

# Vérifier si les imbalances sont comblés par les bougies suivantes
check_if_imbalance_filled(all_imbalances, historical_candles)

# Séparer les imbalances comblés et non comblés
fullfilled_imbalances = get_fullfilled_imbalances(all_imbalances)
unfilled_imbalances = get_unfilled_imbalances(all_imbalances)

# Calculer les statistiques pour le temps nécessaire pour combler les imbalances
times_to_fill = [imbalance.time_to_be_fullfilled for imbalance in fullfilled_imbalances if imbalance.time_to_be_fullfilled is not None]
stats, stats_as_french = calculate_statistics(times_to_fill)

# Afficher les statistiques en français
print(stats_as_french)

# Tracer les chandeliers de marché avec les imbalances mis en évidence
fig = go.Figure(data=[go.Candlestick(
    x=historical_candles_df.index,
    open=historical_candles_df['open'],
    high=historical_candles_df['high'],
    low=historical_candles_df['low'],
    close=historical_candles_df['close']
)])

plot_market_candles_with_imbalances(fig, historical_candles_df, all_imbalances)

# Afficher la figure Plotly
fig.show()

# Tracer un histogramme des temps pour combler les imbalances
median_time = np.median(times_to_fill)
plot_fill_time_histogram(50, median_time, times_to_fill)
