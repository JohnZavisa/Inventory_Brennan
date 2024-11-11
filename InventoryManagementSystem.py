from pathlib import Path
import tempfile
import shutil
import logging
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inventory Management System

# Create a simple inventory management system for a small store. This problem will help you practice using classes, methods, loops, conditionals, and basic data structures.

# Requirements:
# 1. Create a `Product` class with the following attributes:
#   -[x] name (string)
#   -[x] price (float)
#   -[x] quantity (int)

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

    def __repr__(self):
        """ Returns a string representation of the product, including name, price, and quantity."""
        return f'{self.name}, {self.price}, {self.quantity}'
    
    @staticmethod
    def from_string(product_str: str):
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
    
# BONUS Category class
class Category:
    def __init__(self, category: str):
        self.category = category
        pass

# 2. Create an `InventoryManager` class that will manage a list of `Product` objects. It should have the following methods:
#   -[x] `add_product(self, product)`: Adds a new product to the inventory
#   -[x] `remove_product(self, product_name)`: Removes a product from the inventory by name
#   -[x] `update_quantity(self, product_name, new_quantity)`: Updates the quantity of a product
#   -[x] `get_total_inventory_value(self)`: Calculates and returns the total value of all products in the inventory
#   -[x] `list_low_stock_products(self, threshold)`: Returns a list of products with quantity below the given threshold

class InventoryManager:
    """Manages inventory of products with file persistence.
    
    Attributes:
        filename (str): Path to inventory file
        inventory (List[Product]): List of products in inventory
    """
    def __init__(self, filename="inventory.txt"):
        """Initializes the InventoryManager with an optional filename for inventory persistence.
        
        Args:
            filename (str): Path to the file for loading and saving inventory.
        """
        self.filename = filename
        self.inventory = self.load_inventory()

    def load_inventory(self):
        """Loads inventory from file and creates Product instances from each line.

        Returns:
            List[Product]: A list of products in the inventory.

        Raises:
            FileNotFoundError: If the inventory file does not exist.
        """
        inventory = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    inventory.append(Product.from_string(line))
        except FileNotFoundError:
            logger.error(f'{self.filename} not found.')
        return inventory
    
    def save_inventory(self):
        """Save inventory to file with atomic write operation that ensures data integrity by using a temp file and replacing the original file if successful.

        Raises: 
            IOError: If an error occures trying to save the file.
        """
        inventory_path = Path(self.filename)
        # Create directory if it doesn't exist
        inventory_path.parent.mkdir(parents=True, exist_ok=True)

        # Use temporary file for atomic write
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            try:
                for product in self.inventory:
                    tmp_file.write(f'{product}\n')
                tmp_file.flush()
                shutil.move(tmp_file.name, self.filename)
            except Exception as e:
                Path(tmp_file.name).unlink(missing_ok=True)
                raise IOError(f'Failed to save inventory: {e}')

    def add_product(self, product):
        """Adds a new product to the inventory and saves the updated inventory to the file.
        
        Args:
            product (Product): The product added to inventory.

        Logs:
            Logs product if adding is successfull and notifies if product already exists.
        """
        for existing_product in self.inventory:
            logger.info(f'Adding product: {product.name}')
            if product.name == existing_product.name:
                logger.info(f"{product.name} already exists. Please enter a new product, or select '3' to update quantity.")
        self.inventory.append(product)
        self.save_inventory()
        logger.info(f"Product: {product.name} (x{product.quantity}) has been added at ${product.price}")

    # -[ ] Look into using filter() or list comprehension!!
    def remove_product(self, product_name):
        """Removes a product from inventory.

        Args:
            product_name: Name of product to remove.

        Raises:
            KeyError: If the product is not found in inventory.
        """
        for product in self.inventory:
            if product.name == product_name:
                self.inventory.remove(product)
                self.save_inventory()
                logger.info(f"Removed: {product_name}")
                return
        logger.info(f"Product {product_name} not found in inventory.")

    def update_quantity(self, product_name: str, new_quantity: int) -> None:
        """Updates the quantity of a product in inventory.
        
        Args:
            product_name: Name of product to update
            new_quantity: New quantity to set

        Raises:
            ValueError: If new_quantity is negative
        """
        for product in self.inventory:
            if product.name == product_name:
                product.quantity = new_quantity
                self.save_inventory()
                logger.info(f"Product {product.name} has been updated to new quantity:  {product.quantity} ")
                return
        logger.error(f"Product {product_name} not found.")

    def get_total_inventory_value(self):
        """ Calculates the total value of all inventory.

        Returns:
            float: Total value of all inventory products.
        """
        return sum(product.get_value() for product in self.inventory)

    def list_low_stock_products(self, threshold=5) -> List[str]:
        """ Generates a list of low stock products based on threshold.

        Args:
            threshold (int): Default threshold. Products with quantities below this value are 'low stock.'

        Returns:
            list (str): Product names from inventory with quantities below threshold.
        """
        return [product.name for product in self.inventory if product.quantity < threshold]

# 3. Implement a simple command-line interface that allows the user to:
#   -[x] Add new products
#   -[x] Remove products
#   -[x] Update product quantities
#   -[x] View the total inventory value
#   -[x] List low stock products

def main():
    """Main function to run Inventory Manager application.
    
    This function provides a simple command-line interface that allows the user to:
        - View the inventory including names, prices, and quantities.
        - Add new products with price and quantities.
        - Remove a product from inventory.
        - Update quantity of a product.
        - Display the total value of inventory.
        - List low stock products.
        - Add Category to product from inventory (PLACEHOLDER).
        - Search products from inventory by category (PLACEHOLDER).
        - Generate report (PLACEHOLDER).

    Input:
        User input determines which action to take for inventory.

    Raises:
        ValueError: If invalid input is received for price or quantity.
    """
    manager = InventoryManager()

    while True:
        print("\n--- Inventory Manager ---")
        print("0. View Inventory")
        print("1. Add new products")
        print("2. Remove products")
        print("3. Update product quantities")
        print("4. View the total Inventory value")
        print("5. List low stock products")
        print("6. Add Category") # Not working
        print("7. Search by Category") # Not working
        print("8. Report") # Not working
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "0":
            if len(manager.inventory) == 0:
                print("The inventory is empty.")
            else:
                for product in manager.inventory:
                    print(f"{product.name}: ${product.price}, x{product.quantity}")

        elif choice == "1":
            name = input("Enter name of product: ")
            while True:
                try:
                    price = float(input("Enter price of product: "))
                    break
                except ValueError:
                    print("Please enter a valid number")

            while True:
                try:
                    quantity = int(input("Enter quantity of product: "))
                    break
                except ValueError:
                    print("Please enter a valid INTEGER!")
            product = Product(name, price, quantity)
            manager.add_product(product)
        
        elif choice == "2":
            product = input("What product to remove: ")
            manager.remove_product(product)

        elif choice == "3":
            product_name = input("Enter name of product: ")
            while True:
                try:
                    new_quantity = int(input("Enter new quantity of product: "))
                    manager.update_quantity(product_name, new_quantity)
                    break
                except ValueError:
                    print("Invalid quantity. Please enter a number.")

        elif choice == "4":
            print(f"Total Inventory value: ${manager.get_total_inventory_value()}")

        elif choice == "5":
            print(f"Low stock: {manager.list_low_stock_products()}")

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

# 4. Use appropriate error handling to deal with invalid inputs or actions (e.g., removing a non-existent product).

# 5. Implement a simple data persistence mechanism to save and load the inventory from a file.
    # -[x] DONE!

## Bonus Challenges:

# 1. Add a `Category` class and allow products to be assigned to categories.
# 2. Implement a search function to find products by name or category.
# 3. Add a simple reporting feature that generates a summary of the inventory status.

# This problem covers several important programming concepts:
# - Object-Oriented Programming (classes and objects)
# - Control structures (loops and conditionals)
# - Data structures (lists, dictionaries)
# - File I/O
# - Error handling
# - User input and output

# Good luck, and happy coding!
