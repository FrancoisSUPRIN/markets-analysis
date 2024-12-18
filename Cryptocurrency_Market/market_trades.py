class MarketTrade:
    def __init__(self, res):
        self.event_type = res["e"]
        self.event_time = res['E']
        self.symbol = res["s"]
        self.trade_id = res["t"]
        self.price = float(res["p"])  # Convertir le prix en float
        self.quantity = float(res["q"])  # Convertir la quantité en float
        #self.buyer_order_id = res["B"]
        #self.seller_order_id = res["a"]
        self.trade_time = res['T']
        self.is_the_buyer_the_market_maker = res["m"]
        self.ignore = res["M"]
        
        """class Trade:
    def __init__(self, res):
        self.event_type = res["e"]
        self.event_time = datetime.datetime.fromtimestamp(res['E'] / 1000, tz=datetime.timezone.utc).astimezone(pytz.timezone('Europe/Paris'))
        self.symbol = res["s"]
        self.trade_id = res["t"]
        self.price = float(res["p"])  # Convertir le prix en float
        self.quantity = float(res["q"])  # Convertir la quantité en float
        self.buyer_order_id = res["b"]
        self.seller_order_id = res["a"]
        self.trade_time = datetime.datetime.fromtimestamp(res['T'] / 1000, tz=datetime.timezone.utc)
        self.trade_time = self.trade_time.astimezone(pytz.timezone('Europe/Paris'))
        self.is_the_buyer_the_market_maker = res["m"]
        self.ignore = res["M"]"""
        
# when a signal is detected, create a Trade
# the Trade Object should be usable with Binance REST API