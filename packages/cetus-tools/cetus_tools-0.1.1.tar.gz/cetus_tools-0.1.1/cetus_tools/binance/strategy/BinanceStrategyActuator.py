import math

class BinanceStrategyActuator:
    def __init__(self, connection, config):
        self.connection = connection
        self.config = config
    
    def canBeUsed(order, orderBook):
        pass
    
    def act(order, orderBook):
        pass
    
    def adjustPrice(self, price):
        adjustedPrice = math.floor(price / self.config['tickSize']) * self.config['tickSize']
        return round(adjustedPrice, self.config['decimals'])
    
    def adjustQuantity(self, quantity):
        return round(quantity, self.config['quantityDecimals'])
    
    def findOrder(self, orderId):
        orders = self.connection.get_all_orders(symbol=self.config['symbol'], orderId=orderId, recvWindow=2000)
        for order in orders:
            if str(order['orderId']) == str(orderId):
                return order
        return None