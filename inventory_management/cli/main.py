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
        - View the inventory including names, prices, quantities, and categories.
        - Add new products with price, quantities, and categories.
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
        print("4. Update product category")
        print("5. View the total Inventory value")
        print("6. List low stock products")
        print("7. Search by Category") # Not working
        print("8. Report") # Not working
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "0":
            if len(manager.inventory) == 0:
                print("The inventory is empty.")
            else:
                for product in manager.inventory:
                    print(f"{product.name}: ${product.price}, x{product.quantity}, {product.category}")

        # Add new products
        elif choice == "1":
            name = input("Enter name of product: ").strip().title()
            
            # Check if product already exists.
            if any(product.name == name for product in manager.inventory):
                print(f"'{name}' already exists in inventory.")
                continue

            while True:
                try:
                    price = float(input("Enter price of product: "))
                    break
                except ValueError:
                    print("Please enter a valid number.")

            while True:
                try:
                    quantity = int(input("Enter quantity of product: "))
                    break
                except ValueError:
                    print("Please enter a valid INTEGER!")
            
            category = input("Enter Category of product:  ").title()
            
            product = Product(name, price, quantity, category)
            manager.add_product(product)
        
        # Remove products
        elif choice == "2":
            if len(manager.inventory) == 0:
                print("The inventory is empty.")
            else:
                product = input("What product to remove: ").strip().title()
                manager.remove_product(product)

        # Update product quantities
        elif choice == "3":
            if len(manager.inventory) == 0:
                print("The inventory is empty.")
            else:
                product_name = input("Enter name of product: ").strip().title()
                while True:
                    try:
                        new_quantity = int(input("Enter new quantity of product: "))
                        manager.update_quantity(product_name, new_quantity)
                        break
                    except ValueError:
                        print("Invalid quantity. Please enter a number.")

        # Update Category
        elif choice == "4":
            if len(manager.inventory) == 0:
                print("The inventory is empty.")
            else:
                while True:
                    try:
                        product_name = input("Enter name of product: ").strip().title()
                        if not product_name.strip():
                            print("Product name cannot be empty.")
                            continue
                    except KeyError:
                        print(f"Error: '{product_name}' not found.")
                    try:
                        new_category = input("Enter new category: ").strip().title()
                        manager.update_category(product_name, new_category)
                        break
                    except KeyError:
                        print(f"Error: Product '{product_name}' not found.")

        # View the total Inventory value
        elif choice == "5":
            print(f"Total Inventory value: ${manager.get_total_inventory_value()}")

        # List low stock products
        elif choice == "6":
            print(f"Low stock: {manager.list_low_stock_products()}")

        # Seach by category
        elif choice == "7":
            if len(manager.inventory) == 0:
                print("The inventory is empty.")
            else:
                category = input("Enter a category to search: ").strip().title()
                if not category:
                    print("Category cannot be empty.")
                    return
                results = manager.category_search(category)
                if results:
                    print(f"\nProducts in category '{category}':")
                    for product in results:
                        print(f"- {product.name}: ${product.price}, x{product.quantity}")
                else:
                    print(f"No products found in category '{category}'.")

        # Generate report
        elif choice == "8":
            if len(manager.inventory) == 0:
                print("The inventory is empty.")
            else:
                report = manager.generate_report()
                print("\n--- Inventory Report by Category ---")
                print(report)

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()