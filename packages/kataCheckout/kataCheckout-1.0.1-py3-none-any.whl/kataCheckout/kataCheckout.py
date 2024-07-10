# Domain Objects
class Product:
    def __init__(self, name, price):
        self.__name = name
        self.__price = price

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value

class Rules:
    def __init__(self, product, quantity=None, discount=None):
        self.product = product
        self.quantity = quantity
        self.discount = discount

# Checkout
class Checkout:
    def __init__(self, rules):
        self.rules = rules
        self.items = {}

    def scan(self, product):
        if product.name not in self.rules:
            return "Item not in list"
        if product in self.items:
            self.items[product] += 1
        else:
            self.items[product] = 1

    def total(self):
        total= 0
        for product, count in self.items.items():
            rule = self.rules.get(product.name)
            if rule and rule.quantity:
                quantity, discount = rule.quantity, rule.discount
                total += discount * (count //quantity)
                count %= quantity
            total += count * product.price
        return total