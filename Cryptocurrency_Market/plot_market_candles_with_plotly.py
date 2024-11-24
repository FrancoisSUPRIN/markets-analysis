'''import plotly.graph_objects as go

def plot_market_candles_with_plotly(historical_candles_df):
    """
    Plots candlestick chart using Plotly.

    Args:
    - historical_candles_df (DataFrame): DataFrame containing historical candlestick data.
    """

    # Tracer les bougies avec Plotly
    fig = go.Figure(data=[go.Candlestick(x=historical_candles_df.index,
                    open=historical_candles_df['open'],
                    high=historical_candles_df['high'],
                    low=historical_candles_df['low'],
                    close=historical_candles_df['close'])])
    
    # Mettre à jour le layout du graphique
    fig.update_layout(title='Bougies BTCUSDT',
                      xaxis_title='Date',
                      yaxis_title='Prix',
                      height=1000)  # Ajustez la hauteur ici selon vos besoins
    
    # Afficher le graphique
    fig.show()
    
    
import datetime  # Pour obtenir le timestamp actuel

def plot_market_candles_with_imbalances(historical_candles_df, imbalances):
    """
    Plots a candlestick chart using Plotly and adds rectangles for unfulfilled imbalances.

    Args:
    - historical_candles_df (DataFrame): DataFrame containing historical candlestick data.
    - imbalances (list): List of imbalance objects with information for rectangles.
    """

    # Créer le graphique des chandeliers
    fig = go.Figure(data=[go.Candlestick(
        x=historical_candles_df.index,
        open=historical_candles_df['open'],
        high=historical_candles_df['high'],
        low=historical_candles_df['low'],
        close=historical_candles_df['close']
    )])

    # Obtenir le timestamp actuel pour x1
    now_timestamp = datetime.datetime.now().timestamp() * 1000  # en millisecondes

    # Ajouter des rectangles pour les imbalances
    for imbalance in imbalances:
        fig.add_shape(
            type="rect",
            x0=imbalance.timestamp,
            x1=now_timestamp,  # Actuel timestamp pour x1
            y0=imbalance.open_price,
            y1=imbalance.close_price,
            line=dict(color="black"),  # Couleur des bordures
            fillcolor="grey",  # Couleur de remplissage grise
            opacity=0.5,  # 50% d'opacité
        )

    # Mettre à jour le layout du graphique
    fig.update_layout(
        title="Bougies avec Imbalances",
        xaxis_title="Date",
        yaxis_title="Prix",
        height=1000,
    )

    # Afficher le graphique
    fig.show()'''

import plotly.graph_objects as go

def plot_market_candles_with_plotly(fig, historical_candles_df):
    """
    Updates candlestick chart using Plotly.

    Args:
    - fig (Figure): Plotly figure object to update.
    - historical_candles_df (DataFrame): DataFrame containing historical candlestick data.
    """

    # Mettre à jour les données des bougies dans la figure
    fig.data[0].x = historical_candles_df.index
    fig.data[0].open = historical_candles_df['open']
    fig.data[0].high = historical_candles_df['high']
    fig.data[0].low = historical_candles_df['low']
    fig.data[0].close = historical_candles_df['close']
    
    # Mettre à jour le layout du graphique
    fig.update_layout(title='Bougies BTCUSDT',
                      xaxis_title='Date',
                      yaxis_title='Prix',
                      height=1000)  # Ajustez la hauteur ici selon vos besoins

def plot_market_candles_with_imbalances(fig, historical_candles_df, imbalances):
    """
    Updates candlestick chart with imbalances rectangles using Plotly.

    Args:
    - fig (Figure): Plotly figure object to update.
    - historical_candles_df (DataFrame): DataFrame containing historical candlestick data.
    - imbalances (list): List of imbalance objects with information for rectangles.
    """

    # Mettre à jour les données des bougies dans la figure
    fig.data[0].x = historical_candles_df.index
    fig.data[0].open = historical_candles_df['open']
    fig.data[0].high = historical_candles_df['high']
    fig.data[0].low = historical_candles_df['low']
    fig.data[0].close = historical_candles_df['close']

    # Obtenir le timestamp actuel pour x1
    now_timestamp = datetime.datetime.now().timestamp() * 1000  # en millisecondes

    # Ajouter ou mettre à jour les rectangles pour les imbalances
    for i, imbalance in enumerate(imbalances):
        if len(fig.data) <= i + 1:
            # Si la trace n'existe pas, ajoutez-la
            fig.add_shape(
                type="rect",
                x0=imbalance.timestamp,
                x1=now_timestamp,  # Actuel timestamp pour x1
                y0=imbalance.open_price,
                y1=imbalance.close_price,
                line=dict(color="black"),  # Couleur des bordures
                fillcolor="grey",  # Couleur de remplissage grise
                opacity=0.5,  # 50% d'opacité
            )
        else:
            # Si la trace existe, mettez à jour ses coordonnées
            fig.data[i + 1].x0 = imbalance.timestamp
            fig.data[i + 1].x1 = now_timestamp
            fig.data[i + 1].y0 = imbalance.open_price
            fig.data[i + 1].y1 = imbalance.close_price

    # Supprimer les traces supplémentaires s'il y en a
    if len(fig.data) > len(imbalances) + 1:
        fig.data = fig.data[:len(imbalances) + 1]

    # Mettre à jour le layout du graphique
    fig.update_layout(
        title="Bougies avec Imbalances",
        xaxis_title="Date",
        yaxis_title="Prix",
        height=1000,
    )

