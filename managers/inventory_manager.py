from pathlib import Path
import tempfile
import shutil
import logging
from typing import List, Optional
from models.product import Product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    def load_inventory(self) -> List[Product]:
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

    def add_product(self, product) -> None:
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
    def remove_product(self, product_name) -> None:
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

    def get_total_inventory_value(self) -> float:
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