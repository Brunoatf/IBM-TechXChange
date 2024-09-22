import json
import os

class CartDatabase:
    def __init__(self, catalog_db, filename='cart.json'):
        # Get the parent directory of the current script and use it as the base path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))  # This is the parent directory

        # Construct the path to the cart.json file in the parent directory
        self.filename = os.path.join(parent_dir, filename)
        self.catalog_db = catalog_db

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
        # Get product details from catalog
        product_details = self.catalog_db.get_product_by_name(product_name)
        if product_details is None:
            return "Product not found in catalog."

        product_price = product_details['price']

        # Check if product is already in the cart
        for item in self.cart:
            if item['name'] == product_name:
                item['quantity'] += quantity
                item['total_price'] = item['quantity'] * product_price
                self._save_cart()
                return "Product quantity updated in cart."

        # If not, add a new product entry with name, quantity, and price
        self.cart.append({
            'name': product_name,
            'quantity': quantity,
            'price_per_unit': product_price,
            'total_price': quantity * product_price
        })
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
