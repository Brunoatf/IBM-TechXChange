import json

class CartDatabase:
    def __init__(self, filename='cart.json'):
        self.filename = filename
        # Initialize the cart file if it doesn't exist
        try:
            with open(self.filename, 'r') as f:
                self.cart = json.load(f)
            if not isinstance(self.cart, list):
                self.cart = []
        except (FileNotFoundError, json.JSONDecodeError):
            self.cart = []
            self._save_cart()

    def _save_cart(self):
        with open(self.filename, 'w') as f:
            json.dump(self.cart, f, indent=4)

    def add_product(self, product_name, quantity):
        # Check if product already in cart
        for item in self.cart:
            if item['name'] == product_name:
                item['quantity'] += quantity
                self._save_cart()
                return "Product quantity updated in cart."
        # If not, add new product
        self.cart.append({'name': product_name, 'quantity': quantity})
        self._save_cart()
        return "Product added to cart."

    def remove_product(self, product_name):
        for item in self.cart:
            if item['name'] == product_name:
                self.cart.remove(item)
                self._save_cart()
                return "Product removed from cart."
        return "Product not found in cart."

    def clear_cart(self):
        self.cart = []
        self._save_cart()

    def get_cart(self):
        return self.cart

