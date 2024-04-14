import plotly.graph_objects as go

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
