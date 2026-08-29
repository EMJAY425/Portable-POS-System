import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

PRODUCTS_FILE = "products.json"
SALES_FILE = "sales.json"

# ========================
# FILE HANDLING
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

products = load_data(PRODUCTS_FILE)
sales = load_data(SALES_FILE)

def get_next_id():
    return max([p["id"] for p in products], default=0) + 1

# ========================
# MAIN WINDOW
# ========================
root = tk.Tk()
root.title("Sari-Sari Store System")
root.geometry("600x400")

# ========================
# PRODUCT FUNCTIONS
# ========================
def refresh_products():
    product_list.delete(0, tk.END)
    for p in products:
        product_list.insert(
            tk.END,
            f"ID:{p['id']} | {p['name']} | ₱{p['price']} | Stock:{p['stock']}"
        )

def add_product():
    try:
        product = {
            "id": get_next_id(),
            "name": name_entry.get(),
            "price": float(price_entry.get()),
            "stock": int(stock_entry.get())
        }
    except ValueError:
        messagebox.showerror("Error", "Invalid input")
        return

    products.append(product)
    save_data(PRODUCTS_FILE, products)
    refresh_products()
    messagebox.showinfo("Success", "Product added")

def update_product():
    selection = product_list.curselection()
    if not selection:
        return

    index = selection[0]
    try:
        products[index]["name"] = name_entry.get()
        products[index]["price"] = float(price_entry.get())
        products[index]["stock"] = int(stock_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid input")
        return

    save_data(PRODUCTS_FILE, products)
    refresh_products()
    messagebox.showinfo("Updated", "Product updated")

def delete_product():
    selection = product_list.curselection()
    if not selection:
        return

    products.pop(selection[0])
    save_data(PRODUCTS_FILE, products)
    refresh_products()
    messagebox.showinfo("Deleted", "Product deleted")

# ========================
# SALES FUNCTIONS
# ========================
cart = []

def add_to_cart():
    selection = product_list.curselection()
    if not selection:
        return

    product = products[selection[0]]
    try:
        qty = int(qty_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid quantity")
        return

    if qty > product["stock"]:
        messagebox.showwarning("Stock", "Not enough stock")
        return

    subtotal = product["price"] * qty
    cart.append({"product": product, "qty": qty, "subtotal": subtotal})
    cart_list.insert(tk.END, f"{product['name']} x{qty} = ₱{subtotal}")

def checkout():
    if not cart:
        messagebox.showwarning("Empty", "Cart is empty")
        return

    total = 0
    for item in cart:
        item["product"]["stock"] -= item["qty"]
        total += item["subtotal"]

    save_data(PRODUCTS_FILE, products)

    sale = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": cart,
        "total": total
    }
    sales.append(sale)
    save_data(SALES_FILE, sales)

    receipt = "=== RECEIPT ===\n"
    for item in cart:
        receipt += f"{item['product']['name']} x{item['qty']} = ₱{item['subtotal']}\n"
    receipt += f"\nTOTAL: ₱{total}"

    messagebox.showinfo("Receipt", receipt)

    cart.clear()
    cart_list.delete(0, tk.END)
    refresh_products()

# ========================
# UI LAYOUT
# ========================
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Product Name").grid(row=0, column=0)
tk.Label(frame, text="Price").grid(row=1, column=0)
tk.Label(frame, text="Stock").grid(row=2, column=0)

name_entry = tk.Entry(frame)
price_entry = tk.Entry(frame)
stock_entry = tk.Entry(frame)

name_entry.grid(row=0, column=1)
price_entry.grid(row=1, column=1)
stock_entry.grid(row=2, column=1)

tk.Button(frame, text="Add", command=add_product).grid(row=3, column=0)
tk.Button(frame, text="Update", command=update_product).grid(row=3, column=1)
tk.Button(frame, text="Delete", command=delete_product).grid(row=3, column=2)

product_list = tk.Listbox(root, width=70)
product_list.pack(pady=10)

refresh_products()

tk.Label(root, text="Quantity").pack()
qty_entry = tk.Entry(root)
qty_entry.pack()

tk.Button(root, text="Add to Cart", command=add_to_cart).pack(pady=5)

cart_list = tk.Listbox(root, width=70)
cart_list.pack()

tk.Button(root, text="Checkout", command=checkout).pack(pady=10)

# ========================
# RUN APP
# ========================
root.mainloop()