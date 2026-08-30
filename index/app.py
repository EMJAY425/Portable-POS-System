import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
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
    db_url = os.environ.get('DATABASE_URL')

    # Render Production Environment (PostgreSQL)
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return psycopg2.connect(db_url, cursor_factory=RealDictCursor)

    # Local PC Environment (SQLite)
    else:
        db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sarisari.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn


def init_db():
    db_url = os.environ.get('DATABASE_URL')
    conn = get_db_connection()
    cursor = conn.cursor()

    if db_url:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                barcode TEXT,
                name TEXT NOT NULL,
                price NUMERIC ( 10, 2 ) NOT NULL,
                stock INTEGER NOT NULL 
            );
                
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                datetime TEXT NOT NULL,
                total NUMERIC ( 10, 2 ) NOT NULL 
            );

            CREATE TABLE IF NOT EXISTS sale_items (
                id SERIAL PRIMARY KEY,
                sale_id INTEGER,
                product_name TEXT,
                qty INTEGER,
                subtotal NUMERIC ( 10, 2 ), 
                FOREIGN KEY (sale_id) REFERENCES sales (id)
            );

            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                recovery_answer TEXT NOT NULL
            );
        ''')

    else:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT, 
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL 
            );

            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
                total REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER,
                product_name TEXT,
                qty INTEGER,
                subtotal REAL, 
                FOREIGN KEY (sale_id) REFERENCES sales(id)
            );

            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                recovery_answer TEXT NOT NULL
            );
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
        user = request.form.get('username', '').strip()
        pw = request.form.get('password', '').strip()
        answer = request.form.get('recovery_answer', '').strip()

        if not user or not pw or not answer:
            flash('All fields are required.')
            return render_template('signup.html')

        conn = get_db_connection()
        cursor = conn.cursor()
        db_url = os.environ.get('DATABASE_URL')
        param = '%s' if db_url else '?'

        # Check if username already exists to protect existing accounts
        cursor.execute(f"SELECT id FROM users WHERE username = {param}", (user,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            flash('Username already taken. Please choose another one.')
            return render_template('signup.html')

        # Hash password and store new user record
        hashed_pw = generate_password_hash(pw)
        cursor.execute(
            f"INSERT INTO users (username, password, recovery_answer) VALUES ({param}, {param}, {param})",
            (user, hashed_pw, answer)
        )
        conn.commit()
        conn.close()

        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('username', '').strip()
        pw_input = request.form.get('password', '').strip()

        conn = get_db_connection()
        cursor = conn.cursor()
        db_url = os.environ.get('DATABASE_URL')
        param = '%s' if db_url else '?'

        cursor.execute(f"SELECT * FROM users WHERE username = {param}", (user_input,))
        user = cursor.fetchone()
        conn.close()

        # Check plain password or hashed password for backwards compatibility
        if user and (user['password'] == pw_input or check_password_hash(user['password'], pw_input)):
            session['logged_in'] = True
            session['username'] = user['username']
            return redirect(url_for('products'))
        else:
            flash('Invalid username or password.')

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
        cursor = conn.cursor()
        db_url = os.environ.get('DATABASE_URL')
        param = '%s' if db_url else '?'

        cursor.execute(f'SELECT * FROM users WHERE username = {param}', (user,))
        data = cursor.fetchone()

        if data and data['recovery_answer'] == answer:
            cursor.execute(f'UPDATE users SET password = {param} WHERE username = {param}', (new_pw, user))
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

    cursor = conn.cursor()
    db_url = os.environ.get('DATABASE_URL')
    param = '%s' if db_url else '?'

    if search_query:
        query = f"SELECT * FROM products WHERE name LIKE {param}"
        cursor.execute(query, ('%' + search_query + '%',))
        products = cursor.fetchall()
    else:
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()

    conn.close()
    return render_template('products.html', products=products, active_tab='products', search_query=search_query)

@app.route('/add_product', methods=('POST',))
@login_required
def add_product():
    barcode = request.form.get('barcode', '').strip()
    name = request.form.get('name')
    price = float(request.form.get('price'))
    stock = int(request.form.get('stock'))

    conn = get_db_connection()
    cursor = conn.cursor()
    db_url = os.environ.get('DATABASE_URL')
    param = '%s' if db_url else '?'

    cursor.execute(
        f'INSERT INTO products (barcode, name, price, stock) VALUES ({param}, {param}, {param}, {param})',
        (barcode, name, price, stock)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('products'))

@app.route('/get_product_by_barcode/<barcode>')
@login_required
def get_product_by_barcode(barcode):
    conn = get_db_connection()
    cursor = conn.cursor()
    db_url = os.environ.get('DATABASE_URL')
    param = '%s' if db_url else '?'

    cursor.execute(f'SELECT * FROM products WHERE barcode = {param}', (barcode,))
    product = cursor.fetchone()
    conn.close()

    if product:
        return {'success': True, 'id': product['id'], 'name': product['name'], 'price': product['price'], 'stock': product['stock']}
    return {'success': False, 'message': 'Product not registered in inventory!'}

@app.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    param = '%s' if os.environ.get('DATABASE_URL') else '?'
    cursor.execute(f'DELETE FROM products WHERE id = {param}', (id,))
    conn.commit()
    conn.close()
    flash('Product deleted!')
    return redirect(url_for('products'))

@app.route('/edit_product/<int:id>')
@login_required
def edit_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    param = '%s' if os.environ.get('DATABASE_URL') else '?'
    cursor.execute(f'SELECT * FROM products WHERE id = {param}', (id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/update_product/<int:id>', methods=('POST',))
@login_required
def update_product(id):
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']

    conn = get_db_connection()
    cursor = conn.cursor()
    param = '%s' if os.environ.get('DATABASE_URL') else '?'
    cursor.execute(f'UPDATE products SET name = {param}, price = {param}, stock = {param} WHERE id = {param}',(name, float(price), int(stock), id))
    conn.commit()
    conn.close()
    flash('Product updated successfully!')
    return redirect(url_for('products'))

@app.route('/sales')
@login_required
def sales():
    search_query = request.args.get('search', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    db_url = os.environ.get('DATABASE_URL')
    param = '%s' if db_url else '?'

    if search_query:
        # Using ILIKE for PostgreSQL case-insensitive search
        like_op = 'ILIKE' if db_url else 'LIKE'
        query = f"SELECT * FROM products WHERE stock > 0 AND name {like_op} {param}"
        cursor.execute(query, (f"%{search_query}%",))
    else:
        cursor.execute('SELECT * FROM products WHERE stock > 0')

    products = cursor.fetchall()
    conn.close()

    return render_template(
        'sales.html',
        products=products,
        cart=session.get('cart', []),
        cart_total=session.get('cart_total', 0.0),
        active_tab='sales',
        search_query=search_query
    )

@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    prod_id = request.form.get('product_id')
    qty = int(request.form.get('quantity', 1))

    conn = get_db_connection()
    cursor = conn.cursor()
    db_url = os.environ.get('DATABASE_URL')
    param = '%s' if db_url else '?'

    # Notice the f-string 'f' before the SQL query
    cursor.execute(f'SELECT * FROM products WHERE id = {param}', (prod_id,))
    product = cursor.fetchone()
    conn.close()

    if product and qty > 0 and qty <= product['stock']:
        subtotal = float(product['price']) * int(qty)
        item = {
            'id': product['id'],
            'name': product['name'],
            'price': float(product['price']),
            'qty': int(qty),
            'subtotal': float(subtotal)
        }

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
    cursor = conn.cursor()
    db_url = os.environ.get('DATABASE_URL')

    if db_url:
        cursor.execute('INSERT INTO sales (datetime, total) VALUES (%s, %s) RETURNING id', (now, cart_total))
        sale_id = cursor.fetchone()['id']

        for item in cart:
            cursor.execute('INSERT INTO sale_items (sale_id, product_name, qty, subtotal) VALUES (%s, %s, %s, %s)',
                           (sale_id, item['name'], item['qty'], item['subtotal']))
            cursor.execute('UPDATE products SET stock = stock - %s WHERE id = %s', (item['qty'], item['id']))
    else:
        cursor.execute('INSERT INTO sales (datetime, total) VALUES (?, ?)', (now, cart_total))
        sale_id = cursor.lastrowid

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

    cursor = conn.cursor()
    db_url = os.environ.get('DATABASE_URL')
    param = '%s' if db_url else '?'

    # 2. FETCH SALES
    if filter_date:
        cursor.execute(f'SELECT * FROM sales WHERE datetime LIKE {param} ORDER BY datetime DESC', (f'{filter_date}%',))
        sales_rows = cursor.fetchall()
    else:
        cursor.execute('SELECT * FROM sales ORDER BY datetime DESC')
        sales_rows = cursor.fetchall()

    processed_sales = []
    for row in sales_rows:
        sale_dict = dict(row)
        cursor.execute(f'SELECT * FROM sale_items WHERE sale_id = {param}', (sale_dict['id'],))
        item_rows = cursor.fetchall()
        sale_dict['products_list'] = [dict(item) for item in item_rows]
        processed_sales.append(sale_dict)

    # 4. CALCULATE TOTALS
    today = datetime.now().strftime('%Y-%m-%d')
    this_month = datetime.now().strftime('%Y-%m')
    this_year = datetime.now().strftime('%Y')

    cursor.execute(f"SELECT SUM(total) FROM sales WHERE datetime LIKE {param}", (f'{today}%',))
    res = cursor.fetchone()
    total_day = (res['sum'] or res[0]) if res and (res['sum'] or res[0]) else 0

    cursor.execute(f"SELECT SUM(total) FROM sales WHERE datetime LIKE {param}", (f'{this_month}%',))
    res = cursor.fetchone()
    total_month = (res['sum'] or res[0]) if res and (res['sum'] or res[0]) else 0

    cursor.execute(f"SELECT SUM(total) FROM sales WHERE datetime LIKE {param}", (f'{this_year}%',))
    res = cursor.fetchone()
    total_year = (res['sum'] or res[0]) if res and (res['sum'] or res[0]) else 0

    cursor.execute("SELECT SUM(total) FROM sales")
    res = cursor.fetchone()
    total_all = (res['sum'] or res[0]) if res and (res['sum'] or res[0]) else 0

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
