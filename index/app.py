import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_sarisari_key'  # Required for session (shopping cart) and flash messages

# ========================
# DATABASE HELPER
# ========================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Please log in first.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sarisari.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
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
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT NOT NULL,
            total REAL NOT NULL
        )
''')
    # CHANGED HERE: Added 's' to sale_items
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
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            recovery_answer TEXT NOT NULL 
        )
''')
    conn.commit()
    conn.close()

with app.app_context():
    init_db()

# ========================
# ROUTES (WEB PAGES)
# ========================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        pw = generate_password_hash(request.form['password'])
        answer = request.form['recovery_answer'].lower()

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password, recovery_answer) VALUES (?, ?, ?)', (user, pw, answer))
            conn.commit()
            flash("Account created! You can now log in.")
            return redirect(url_for('login'))
        except:
            flash("Username already exists.")
        finally:
            conn.close()
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']

        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM users WHERE username = ?', (user,)).fetchone()
        conn.close()

        if user_data and check_password_hash(user_data['password'], pw):
            session['logged_in'] = True
            session['username'] = user
            return redirect(url_for('products'))
        flash("Invalid username or password.")
    return render_template('login.html')

@app.route('/logout')
def logout():  # <--- This name must be 'logout'
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        user = request.form['username']
        answer = request.form['recovery_answer'].lower()
        new_pw = generate_password_hash(request.form['new_password'])

        conn = get_db_connection()
        data = conn.execute('SELECT * FROM users WHERE username = ?', (user,)).fetchone()

        if data and data['recovery_answer'] == answer:
            conn.execute('UPDATE users SET password = ? WHERE username = ?', (new_pw, user))
            conn.commit()
            flash("Password updated successfully!")
            return redirect(url_for('login'))
        flash("Incorrect username or recovery answer.")
        conn.close()
    return render_template('forgot_password.html')

@app.route('/')
@login_required
def products():
    search_query = request.args.get('search', '')  # Get the text from the search bar
    conn = get_db_connection()

    if search_query:
        # Filter products by name using the LIKE operator
        query = "SELECT * FROM products WHERE name LIKE ?"
        products = conn.execute(query, ('%' + search_query + '%',)).fetchall()
    else:
        products = conn.execute('SELECT * FROM products').fetchall()

    conn.close()
    return render_template('products.html', products=products, active_tab='products', search_query=search_query)

@app.route('/add_product', methods=('POST',))
@login_required
def add_product():
    barcode = request.form.get('barcode')
    name = request.form.get('name')
    price = request.form.get('price')
    stock = request.form.get('stock')

    return redirect(url_for('products'))

@app.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Product deleted!')
    return redirect(url_for('products'))

@app.route('/edit_product/<int:id>')
@login_required
def edit_product(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/update_product/<int:id>', methods=('POST',))
@login_required
def update_product(id):
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']

    conn = get_db_connection()
    conn.execute('UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?',
                 (name, float(price), int(stock), id))
    conn.commit()
    conn.close()
    flash('Product updated successfully!')
    return redirect(url_for('products'))

@app.route('/sales')
@login_required
def sales():
    search_query = request.args.get('search', '')
    conn = get_db_connection()

    if search_query:

        products = conn.execute("SELECT * FROM products WHERE stock > 0 AND name LIKE ?",
                                ('%' + search_query + '%',)).fetchall()
    else:
        products = conn.execute('SELECT * FROM products WHERE stock > 0').fetchall()

    conn.close()
    return render_template('sales.html', products=products, cart=session.get('cart', []),
                           cart_total=session.get('cart_total', 0.0), active_tab='sales', search_query=search_query)

@app.route('/add_to_cart', methods=('POST',))
@login_required
def add_to_cart():
    prod_id = request.form.get('product_id')
    qty = int(request.form.get('quantity', 1))

    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (prod_id,)).fetchone()
    conn.close()

    if product and qty > 0 and qty <= product['stock']:
        subtotal = product['price'] * qty
        item = {'id': product['id'], 'name': product['name'], 'qty': qty, 'subtotal': subtotal}

        cart = session.get('cart', [])
        cart.append(item)
        session['cart'] = cart
        session['cart_total'] = session.get('cart_total', 0.0) + subtotal
        session.modified = True
    else:
        flash('Invalid quantity or insufficient stock.')

    return redirect(url_for('sales'))

@app.route('/checkout', methods=('POST',))
@login_required
def checkout():
    cart = session.get('cart', [])
    cart_total = session.get('cart_total', 0.0)

    if not cart:
        flash('Cart is empty!')
        return redirect(url_for('sales'))

    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Record Sale
    cursor.execute('INSERT INTO sales (datetime, total) VALUES (?, ?)', (now, cart_total))
    sale_id = cursor.lastrowid

    # 2. Record Items and Deduct Stock
    for item in cart:
        cursor.execute('INSERT INTO sale_items (sale_id, product_name, qty, subtotal) VALUES (?, ?, ?, ?)',
                       (sale_id, item['name'], item['qty'], item['subtotal']))
        cursor.execute('UPDATE products SET stock = stock - ? WHERE id = ?', (item['qty'], item['id']))

    conn.commit()
    conn.close()

    receipt_data = {
        'items': cart,  # 'cart' should be your list of items from line 243
        'total': cart_total,
        'transaction_id': sale_id,
        'date': now
    }

    session['last_receipt'] = receipt_data
    session.pop('cart', None)
    session.pop('cart_total', None)

    return redirect(url_for('receipt'))


@app.route('/receipt')
@login_required
def receipt():
    receipt_data = session.get('last_receipt')
    if not receipt_data:
        return redirect(url_for('sales'))

    return render_template('receipt.html', receipt=receipt_data)


@app.route('/reports')
@login_required
def reports():
    conn = get_db_connection()

    # 1. CAPTURE THE FILTER DATE (Critical for the filter to work!)
    filter_date = request.args.get('date')

    # 2. FETCH SALES (Apply filter if date is picked)
    if filter_date:
        # We match the date part of the timestamp
        sales_rows = conn.execute('SELECT * FROM sales WHERE datetime LIKE ? ORDER BY datetime DESC',
                                  (f'{filter_date}%',)).fetchall()
    else:
        sales_rows = conn.execute('SELECT * FROM sales ORDER BY datetime DESC').fetchall()

    # 3. ATTACH PRODUCTS (Rename to products_list to avoid crash)
    processed_sales = []
    for row in sales_rows:
        sale_dict = dict(row)
        item_rows = conn.execute('SELECT * FROM sale_items WHERE sale_id = ?', (sale_dict['id'],)).fetchall()
        # renamos it here to match the HTML fix below
        sale_dict['products_list'] = [dict(item) for item in item_rows]
        processed_sales.append(sale_dict)

    # 4. CALCULATE DASHBOARD TOTALS (Keep your current logic here)
    today = datetime.now().strftime('%Y-%m-%d')
    this_month = datetime.now().strftime('%Y-%m')
    this_year = datetime.now().strftime('%Y')

    total_day = conn.execute("SELECT SUM(total) FROM sales WHERE datetime LIKE ?", (f'{today}%',)).fetchone()[0] or 0
    total_month = conn.execute("SELECT SUM(total) FROM sales WHERE datetime LIKE ?", (f'{this_month}%',)).fetchone()[
                      0] or 0
    total_year = conn.execute("SELECT SUM(total) FROM sales WHERE datetime LIKE ?", (f'{this_year}%',)).fetchone()[
                     0] or 0
    total_all = conn.execute('SELECT SUM(total) FROM sales').fetchone()[0] or 0

    conn.close()

    # 5. RETURN PROCESSED DATA
    return render_template('reports.html',
                           sales=processed_sales,  # Send the processed list
                           total_day=total_day,
                           total_month=total_month,
                           total_year=total_year,
                           total_all=total_all)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
