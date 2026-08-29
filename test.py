import json
import os
from datetime import datetime

PRODUCTS_FILE = "products.json"
SALES_FILE = "sales.json"


# ========================
# FILE HANDLING UTILITIES
# ========================
def load_data(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# Load existing data
products = load_data(PRODUCTS_FILE)
sales = load_data(SALES_FILE)


# ========================
# PRODUCT MANAGEMENT
# ========================
def add_product():
    print("\n--- Add New Product ---")
    name = input("Product name: ")

    try:
        price = float(input("Price: "))
        stock = int(input("Stock quantity: "))
    except ValueError:
        print("Invalid input.")
        return

    product = {
        "id": max([p["id"] for p in products], default=0) + 1,
        "name": name,
        "price": price,
        "stock": stock
    }

    products.append(product)
    save_data(PRODUCTS_FILE, products)
    print("Product added successfully!")


def view_products():
    print("\n--- Product List ---")
    if not products:
        print("No products found.")
        return

    for p in products:
        print(f"ID: {p['id']} | {p['name']} | ₱{p['price']} | Stock: {p['stock']}")


def update_product():
    view_products()
    try:
        prod_id = int(input("\nEnter Product ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    for p in products:
        if p["id"] == prod_id:
            print(f"Updating {p['name']}")
            p["name"] = input("New name: ")

            try:
                p["price"] = float(input("New price: "))
                p["stock"] = int(input("New stock: "))
            except ValueError:
                print("Invalid input.")
                return

            save_data(PRODUCTS_FILE, products)
            print("Product updated!")
            return

    print("Product not found.")


def delete_product():
    view_products()
    try:
        prod_id = int(input("\nEnter Product ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    for p in products:
        if p["id"] == prod_id:
            products.remove(p)
            save_data(PRODUCTS_FILE, products)
            print("Product deleted!")
            return

    print("Product not found.")


# ========================
# SALES SYSTEM
# ========================
def process_sale():
    cart = []
    total = 0

    while True:
        view_products()
        try:
            prod_id = int(input("\nEnter Product ID to buy (0 to checkout): "))
        except ValueError:
            print("Invalid input.")
            continue

        if prod_id == 0:
            break

        product = next((p for p in products if p["id"] == prod_id), None)

        if not product:
            print("Invalid ID.")
            continue

        try:
            qty = int(input("Quantity: "))
        except ValueError:
            print("Invalid quantity.")
            continue

        if qty > product["stock"] or qty <= 0:
            print("Not enough stock.")
            continue

        subtotal = product["price"] * qty
        cart.append({
            "name": product["name"],
            "qty": qty,
            "subtotal": subtotal
        })

        total += subtotal
        product["stock"] -= qty
        save_data(PRODUCTS_FILE, products)

        print("Added to cart!")

    if total == 0:
        print("No items purchased.")
        return

    sale_record = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": cart,
        "total": total
    }

    sales.append(sale_record)
    save_data(SALES_FILE, sales)

    print("\n=== RECEIPT ===")
    for item in cart:
        print(f"{item['name']} x{item['qty']} = ₱{item['subtotal']}")
    print(f"TOTAL: ₱{total}")
    print("Transaction saved!")


# ========================
# REPORTS
# ========================
def sales_report():
    print("\n--- Sales Report ---")

    # Reload sales data to ensure we have the latest data
    global sales
    sales = load_data(SALES_FILE)

    if not sales:
        print("No sales recorded.")
        return

    total_sales = 0
    for s in sales:
        try:
            print(f"\nDate: {s['datetime']}")
            for item in s["items"]:
                print(f" - {item['name']} x{item['qty']} = ₱{item['subtotal']}")
            print(f" Sale Total: ₱{s['total']}")
            total_sales += s["total"]
        except (KeyError, TypeError):
            print("Invalid sale record format.")
            continue

    print(f"\nTOTAL SALES: ₱{total_sales}")


# ========================
# MENUS
# ========================
def manage_products_menu():
    while True:
        print("""
=== PRODUCT MANAGEMENT ===
1. Add Product
2. View Products
3. Update Product
4. Delete Product
5. Back
""")
        choice = input("Choose: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def main_menu():
    while True:
        print("""
=== SARI-SARI STORE SYSTEM ===
1. Manage Products
2. Process Sale
3. View Sales Report
4. Exit
""")
        choice = input("Enter choice: ")

        if choice == "1":
            manage_products_menu()
        elif choice == "2":
            process_sale()
        elif choice == "3":
            sales_report()
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid option.")


# ========================
# PROGRAM ENTRY POINT
# ========================
if __name__ == "__main__":
    main_menu()
    input("\nPress Enter to exit...")