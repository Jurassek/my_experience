class StockExchange:
    def __init__(self):
        self.orders = {}
        self.best_buy_price = None
        self.best_sell_price = None

    def add_order(self, transaction_id, order, type, price, quantity):
        if order not in ['Buy', 'Sell'] or type not in ['Add', 'Remove']:
            print(f"Invalid order or type for id: {transaction_id}")
            return

        if type == 'Add':
            if order == 'Buy':
                if self.best_buy_price is None or price < self.best_buy_price:
                    self.best_buy_price = price
            elif order == 'Sell':
                if self.best_sell_price is None or price > self.best_sell_price:
                    self.best_sell_price = price
            self.orders[transaction_id] = {'type': order, 'price': price, 'quantity': quantity}
            
        elif type == 'Remove':
            if transaction_id in self.orders:
                removed_price = self.orders.pop(transaction_id)['price']
                if order == 'Buy' and removed_price == self.best_buy_price:
                    self.best_buy_price = max(self.orders.values(), key=lambda x: x['price'])['price'] if self.orders else None
                elif order == 'Sell' and removed_price == self.best_sell_price:
                    self.best_sell_price = min(self.orders.values(), key=lambda x: x['price'])['price'] if self.orders else None
            else:
                print(f"Order {transaction_id} not found.")

    def display_summary(self):
        print(f"Best Buy Price: {self.best_buy_price if self.best_buy_price is not None else 'No Buy Orders'}")
        print(f"Best Sell Price: {self.best_sell_price if self.best_sell_price is not None else 'No Sell Orders'}")
        print("Orders:")
        for transaction_id, order_info in self.orders.items():
            print(f"  Order {transaction_id}: Type-{order_info['type']}, Price-{order_info['price']}, Quantity-{order_info['quantity']}")


# Example usage
exchange = StockExchange()
exchange.add_order("001", "Buy", "Add", 20.0, 100)
exchange.add_order("002", "Sell", "Add", 25.0, 200)
exchange.add_order("003", "Buy", "Add", 23.0, 50)
exchange.add_order("004", "Buy", "Add", 23.0, 70)
exchange.add_order("003", "Buy", "Remove", 23.0, 50)
exchange.add_order("005", "Sell", "Add", 28.0, 100)

exchange.display_summary()
