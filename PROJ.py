import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

#--- DATABASE INITIALIZATION ---

def init_db():
    conn = sqlite3.connect("sarisari.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, 
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT NOT NULL,
            total REAL NOT NULL
        )
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER, 
            product_name TEXT,
            qty INTEGER,
            subtotal REAL,
            FOREIGN KEY (sale_id) REFERENCES sales(id)
        )
''')

    conn.commit()
    return conn

#--- MAIN APPLICATION UI ---

class SariSariApp:
    def __init__(self, root, db_conn):
        self.root = root
        self.conn = db_conn
        self.cursor = self.conn.cursor()

        self.root.title("Sari-Sari Store System")
        self.center_window(800, 600)

        self.cart = []
        self.cart_total = 0.0

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        self.tab_products = ttk.Frame(self.notebook)
        self.tab_sales = ttk.Frame(self.notebook)
        self.tab_reports = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_products, text="Manage Products")
        self.notebook.add(self.tab_sales, text="Process Sale")
        self.notebook.add(self.tab_reports, text="Sales Report")

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.setup_products_tab()
        self.setup_sales_tab()
        self.setup_reports_tab()

    def center_window(self, width, height):
        """Centers the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def on_tab_change(self, event):
        """Refresh data when switching tabs."""
        self.load_products()
        self.load_sales_products()
        self.load_reports()

    #--- MANAGE PRODUCTS TAB ---

    def setup_products_tab(self):
        input_frame = tk.Frame(self.tab_products, pady=10)
        input_frame.pack(fill='x')

        tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5)
        self.prod_name_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.prod_name_var).grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Price:").grid(row=0, column=2, padx=5)
        self.prod_price_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.prod_price_var).grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Stock:").grid(row=0, column=4, padx=5)
        self.prod_stock_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.prod_stock_var).grid(row=0, column=5, padx=5)

        tk.Button(input_frame, text="Add Product", command=self.add_product).grid(row=0, column=6, padx=10)
        tk.Button(input_frame, text="Update Selected", command=self.update_product).grid(row=0, column=7, padx=5)
        tk.Button(input_frame, text="Delete Selected", command=self.delete_product).grid(row=0, column=8, padx=5)

        columns = ("ID", "Name", "Price", "Stock")
        self.prod_tree = ttk.Treeview(self.tab_products, columns=columns, show='headings')
        for col in columns:
            self.prod_tree.heading(col, text=col)
            self.prod_tree.column(col, width=100, anchor=tk.CENTER)
        self.prod_tree.pack(expand=True, fill='both', pady=10)

        self.prod_tree.bind('<ButtonRelease-1>', self.select_product)
        self.load_products()

    def load_products(self):
        for row in self.prod_tree.get_children():
            self.prod_tree.delete(row)
        self.cursor.execute("SELECT * FROM products")
        for row in self.cursor.fetchall():
            formatted_row = (row[0], row[1], f"₱{row[2]:.2f}", row[3])
            self.prod_tree.insert("", tk.END, values=formatted_row)

    def select_product(self, event):
        selected = self.prod_tree.focus()
        if not selected:
            return
        values = self.prod_tree.item(selected, 'values')
        self.prod_name_var.set(values[1])
        self.prod_price_var.set(values[2].replace('₱', ''))
        self.prod_stock_var.set(values[3])

    def add_product(self):
        name = self.prod_name_var.get()
        try:
            price = float(self.prod_price_var.get())
            stock = int(self.prod_stock_var.get())
            if not name: raise ValueError
        except ValueError:
            messagebox.showerror("Error",
                                 "Invalid inputs. Ensure name is filled, price is a number, and stock is an integer.")
            return

        self.cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        self.conn.commit()
        self.clear_product_inputs()
        self.load_products()
        messagebox.showinfo("Success", "Product added!")

    def update_product(self):
        selected = self.prod_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a product to update.")
            return

        prod_id = self.prod_tree.item(selected, 'values')[0]
        try:
            name = self.prod_name_var.get()
            price = float(self.prod_price_var.get())
            stock = int(self.prod_stock_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid inputs.")
            return

        self.cursor.execute("UPDATE products SET name=?, price=?, stock=? WHERE id=?", (name, price, stock, prod_id))
        self.conn.commit()
        self.clear_product_inputs()
        self.load_products()
        messagebox.showinfo("Success", "Product updated!")

    def delete_product(self):
        selected = self.prod_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a product to delete.")
            return

        prod_id = self.prod_tree.item(selected, 'values')[0]
        self.cursor.execute("DELETE FROM products WHERE id=?", (prod_id,))
        self.conn.commit()
        self.clear_product_inputs()
        self.load_products()
        messagebox.showinfo("Success", "Product deleted!")

    def clear_product_inputs(self):
        self.prod_name_var.set("")
        self.prod_price_var.set("")
        self.prod_stock_var.set("")

    #--- SALES SYSTEM TAB ---

    def setup_sales_tab(self):
        # Left Panel (Products)
        left_frame = tk.Frame(self.tab_sales)
        left_frame.pack(side=tk.LEFT, expand=True, fill='both', padx=10, pady=10)

        tk.Label(left_frame, text="Available Products").pack()
        columns = ("ID", "Name", "Price", "Stock")
        self.sales_tree = ttk.Treeview(left_frame, columns=columns, show='headings')
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=80, anchor=tk.CENTER)
        self.sales_tree.pack(expand=True, fill='both')

        controls_frame = tk.Frame(left_frame, pady=10)
        controls_frame.pack()
        tk.Label(controls_frame, text="Qty:").grid(row=0, column=0)
        self.qty_var = tk.StringVar(value="1")
        tk.Entry(controls_frame, textvariable=self.qty_var, width=5).grid(row=0, column=1, padx=5)
        tk.Button(controls_frame, text="Add to Cart", command=self.add_to_cart).grid(row=0, column=2)

        right_frame = tk.Frame(self.tab_sales)
        right_frame.pack(side=tk.RIGHT, expand=True, fill='both', padx=10, pady=10)

        tk.Label(right_frame, text="Shopping Cart").pack()
        cart_cols = ("Name", "Qty", "Subtotal")
        self.cart_tree = ttk.Treeview(right_frame, columns=cart_cols, show='headings')
        for col in cart_cols:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100, anchor=tk.CENTER)
        self.cart_tree.pack(expand=True, fill='both')

        self.lbl_total = tk.Label(right_frame, text="Total: ₱0.00", font=("Arial", 14, "bold"))
        self.lbl_total.pack(pady=10)
        tk.Button(right_frame, text="Checkout", command=self.checkout, bg="green", fg="white", font=("Arial", 12)).pack(
            fill='x')

    def load_sales_products(self):
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)
        self.cursor.execute("SELECT * FROM products WHERE stock > 0")
        for row in self.cursor.fetchall():
            self.sales_tree.insert("", tk.END, values=(row[0], row[1], f"₱{row[2]:.2f}", row[3]))

    def add_to_cart(self):
        selected = self.sales_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a product to buy.")
            return

        values = self.sales_tree.item(selected, 'values')
        prod_id = int(values[0])
        name = values[1]
        price = float(values[2].replace('₱', ''))
        stock_available = int(values[3])

        try:
            qty = int(self.qty_var.get())
            if qty <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive quantity.")
            return

        if qty > stock_available:
            messagebox.showerror("Error", "Not enough stock available!")
            return

        subtotal = price * qty
        self.cart.append({"id": prod_id, "name": name, "qty": qty, "subtotal": subtotal})

        # Visually add to cart tree
        self.cart_tree.insert("", tk.END, values=(name, qty, f"₱{subtotal:.2f}"))

        # Update Total
        self.cart_total += subtotal
        self.lbl_total.config(text=f"Total: ₱{self.cart_total:.2f}")

    def checkout(self):
        if not self.cart:
            messagebox.showinfo("Cart Empty", "No items in cart to checkout.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. Insert into Sales
        self.cursor.execute("INSERT INTO sales (datetime, total) VALUES (?, ?)", (now, self.cart_total))
        sale_id = self.cursor.lastrowid

        for item in self.cart:
            # 2. Insert into Sale Items
            self.cursor.execute(
                "INSERT INTO sale_items (sale_id, product_name, qty, subtotal) VALUES (?, ?, ?, ?)",
                (sale_id, item['name'], item['qty'], item['subtotal'])
            )
            # 3. Deduct Stock
            self.cursor.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (item['qty'], item['id'])
            )

        self.conn.commit()
        messagebox.showinfo("Success", f"Transaction saved!\nTotal Paid: ₱{self.cart_total:.2f}")

        # Clear Cart
        self.cart.clear()
        self.cart_total = 0.0
        self.lbl_total.config(text="Total: ₱0.00")
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)

        self.load_sales_products()

    # ========================
    # 3. REPORTS TAB
    # ========================
    def setup_reports_tab(self):
        self.report_text = tk.Text(self.tab_reports, font=("Courier", 10))
        self.report_text.pack(expand=True, fill='both', padx=10, pady=10)

    def load_reports(self):
        self.report_text.delete(1.0, tk.END)
        self.cursor.execute("SELECT id, datetime, total FROM sales ORDER BY datetime DESC")
        sales = self.cursor.fetchall()

        if not sales:
            self.report_text.insert(tk.END, "No sales recorded yet.\n")
            return

        grand_total = 0.0
        self.report_text.insert(tk.END, f"{'=' * 40}\n")
        self.report_text.insert(tk.END, f"{'SALES REPORT'.center(40)}\n")
        self.report_text.insert(tk.END, f"{'=' * 40}\n\n")

        for sale in sales:
            sale_id, dt, total = sale
            grand_total += total
            self.report_text.insert(tk.END, f"Date: {dt} (Receipt #{sale_id})\n")

            # Get items for this sale
            self.cursor.execute("SELECT product_name, qty, subtotal FROM sale_items WHERE sale_id=?", (sale_id,))
            items = self.cursor.fetchall()

            for item in items:
                name, qty, subtotal = item
                self.report_text.insert(tk.END, f"  - {name} x{qty} = ₱{subtotal:.2f}\n")

            self.report_text.insert(tk.END, f"  SALE TOTAL: ₱{total:.2f}\n")
            self.report_text.insert(tk.END, f"{'-' * 40}\n")

        self.report_text.insert(tk.END, f"\nGRAND TOTAL ALL SALES: ₱{grand_total:.2f}\n")
        self.report_text.insert(tk.END, f"{'=' * 40}\n")


# ========================
# PROGRAM ENTRY POINT
# ========================
if __name__ == "__main__":
    db_connection = init_db()

    root = tk.Tk()
    app = SariSariApp(root, db_connection)


    # Handle window close to ensure DB connection is closed safely
    def on_closing():
        db_connection.close()
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()