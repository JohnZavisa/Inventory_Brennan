
class Product:
    """Represents a product with a name, price, and quantity.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
        quantity (int): The quantity of the product.

    Raises:
        ValueError: if 'price' or 'quantity' is negative.
    """
    def __init__(self, name: str, price: float, quantity: int):
        if price < 0:
            raise ValueError("Price can't be negative!")
        if quantity < 0:
            raise ValueError("Quantity can't be negative!")
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_value(self) -> float:
        """Calculates the total value of the product based on price and quantity.

        Returns:
            float: the total of the product.
        """
        return self.price * self.quantity

    def __repr__(self) -> str:
        """ Returns a string representation of the product, including name, price, and quantity."""
        return f'{self.name}, {self.price}, {self.quantity}'
    
    @staticmethod
    def from_string(product_str: str) -> 'Product':
        """Creates a Product instance from a comma-separated string.

        Args:
            product_str (str): A string representing a product in the format "name, price, quantity".

        Returns:
            Product: A new product instance created from the string.

        Raises:
            ValueError: If 'product_str' format is invalid or values are not appropriate.
        """
        name, price, quantity = product_str.strip().split(',')
        return Product(name, float(price), int(quantity))