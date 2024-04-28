# pip install python-binance
from binance.client import Client
from convert_ts_to_datetime import format_elapsed_time
import numpy as np


# Conversion factors for each Kline interval
def conversion_factors():
    conversion_factors_dict = {
        Client.KLINE_INTERVAL_1MINUTE: 1000 * 60,
        Client.KLINE_INTERVAL_3MINUTE: 1000 * 60 * 3,
        Client.KLINE_INTERVAL_5MINUTE: 1000 * 60 * 5,
        Client.KLINE_INTERVAL_15MINUTE: 1000 * 60 * 15,
        Client.KLINE_INTERVAL_30MINUTE: 1000 * 60 * 30,
        Client.KLINE_INTERVAL_1HOUR: 1000 * 60 * 60,
        Client.KLINE_INTERVAL_2HOUR: 1000 * 60 * 60 * 2,
        Client.KLINE_INTERVAL_4HOUR: 1000 * 60 * 60 * 4,
        Client.KLINE_INTERVAL_6HOUR: 1000 * 60 * 60 * 6,
        Client.KLINE_INTERVAL_8HOUR: 1000 * 60 * 60 * 8,
        Client.KLINE_INTERVAL_12HOUR: 1000 * 60 * 60 * 12,
        Client.KLINE_INTERVAL_1DAY: 1000 * 60 * 60 * 24,
        Client.KLINE_INTERVAL_3DAY: 1000 * 60 * 60 * 24 * 3,
        Client.KLINE_INTERVAL_1WEEK: 1000 * 60 * 60 * 24 * 7,
        Client.KLINE_INTERVAL_1MONTH: 1000 * 60 * 60 * 24 * 30,
    }
    return conversion_factors_dict


# Function to calculate statistics given a Kline interval
def calculate_statistics(times_to_fill):

    # Convert the times to the appropriate unit based on the Kline interval
    times_converted = [ms for ms in times_to_fill]

    # Calculate statistics
    min_val = np.min(times_converted)
    max_val = np.max(times_converted)
    mean_val = np.mean(times_converted)  # Mean
    median_val = np.median(times_converted)  # Median
    std_dev_val = np.std(times_converted)  # Standard deviation

    # Calculate percentiles
    percentiles = {
        "25th": np.percentile(times_converted, 25),
        "50th": np.percentile(times_converted, 50),  # Median
        "75th": np.percentile(times_converted, 75),
        "80th": np.percentile(times_converted, 80),
        "90th": np.percentile(times_converted, 90),
        "95th": np.percentile(times_converted, 95),
        "98th": np.percentile(times_converted, 98),
    }

    # Return a dictionary with the timeframe and calculated statistics
    result = {
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
        "median": median_val,
        "std_dev": std_dev_val,
        "percentiles": percentiles,
    }
    
    percentiles = result['percentiles']
    
    result_as_french = f"""
    Le temps minimum pour combler un imbalance est de {format_elapsed_time(result['min'])}
    Le temps minimum pour combler un imbalance est de {format_elapsed_time(result['min'])}
    Le temps moyen pour combler un imbalance est de {format_elapsed_time(result['mean'])}
    
    Dans 25% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['25th'])}
    Dans 50% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['50th'])}
    Dans 75% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['75th'])}
    Dans 80% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['80th'])}
    Dans 90% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['90th'])}
    Dans 95% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['95th'])}
    Dans 98% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['98th'])}
    """
    
    return result, result_as_french

"""    # Affichage des statistiques dans un langage humain
    print(f"Le temps minimum pour combler un imbalance est de {format_elapsed_time(result['min'])}")
    print(f"Le temps maximum pour combler un imbalance est de {format_elapsed_time(result['max'])}")
    print(f"Le temps moyen pour combler un imbalance est de {format_elapsed_time(result['mean'])}")

    # Percentiles
  
    print(f"Dans 25% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['25th'])}")
    print(f"Dans 50% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['50th'])}")
    print(f"Dans 75% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['75th'])}")
    print(f"Dans 80% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['80th'])}")
    print(f"Dans 90% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['90th'])}")
    print(f"Dans 95% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['95th'])}")
    print(f"Dans 98% des cas, pour combler un imbalance, il faut {format_elapsed_time(percentiles['98th'])}")
    
"""

import matplotlib.pyplot as plt
import numpy as np

# Fonction pour créer un histogramme avec la médiane indiquée
def plot_fill_time_histogram(num_bins, median_time, times_to_fill):
    # Créer l'histogramme
    plt.figure(figsize=(12, 6))
    plt.hist(times_to_fill, bins=num_bins, edgecolor='black')  # Histogramme avec contours noirs

    # Ajouter des labels et un titre
    plt.xlabel("Temps de comblement en heures")
    plt.ylabel("Nombre d'imbalances comblés")
    plt.title("Distribution des temps de comblement des imbalances")

    # Ajouter une ligne verticale pour la médiane
    plt.axvline(median_time, color='red', linestyle='dashed', linewidth=2, label=f'Médiane: {median_time:.2f} heures')

    # Ajouter une légende pour la ligne de médiane
    plt.legend()

    # Afficher l'histogramme
    plt.show()
