from pathlib import Path
from models.product import Product
from managers.inventory_manager import InventoryManager

# Define root directory
root_dir = Path(__file__).resolve().parent.parent
# Define inventory file path inside "db" folder
inventory = root_dir / "db" / "inventory.txt"

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
    manager = InventoryManager(filename=str(inventory))

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