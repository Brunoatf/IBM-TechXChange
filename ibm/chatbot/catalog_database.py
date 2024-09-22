class CatalogDatabase:
    def __init__(self, products):
        self.products = products

    def get_catalog_prompt(self):
        # Convert the products list into a formatted string for the prompt
        product_lines = [f"{idx + 1}. {product['name']} - ${product['price']}"
                         for idx, product in enumerate(self.products)]
        catalog_text = "\n".join(product_lines)
        return f"Product Catalog:\n{catalog_text}\n"

    def get_product_list(self):
        return [product['name'] for product in self.products]