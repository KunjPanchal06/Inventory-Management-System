from flask import Flask, render_template, request, url_for, redirect, session, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Kunj@2006"

userName = "root"
passWord = "root"
hostName = "localhost"
databaseName = "inventory_management"

class Database:
    @staticmethod
    def initializeDatabase():
        conn = mysql.connector.connect(
            host = hostName,
            user = userName,
            password = passWord,
            database = databaseName
        )
        cursor = conn.cursor()
        cursor.close()

    @staticmethod
    def getConnection():
        conn = mysql.connector.connect(
            host = hostName,
            user = userName,
            password = passWord,
            database = databaseName
        )
        return conn

class Authentication:
    @app.route('/auth', methods=['GET', 'POST'])
    def auth():
        if request.method == 'POST':
            action = request.form.get('action')  # Login or Register
            username = request.form['username']
            password = request.form['password']

            conn = Database.getConnection()
            cursor = conn.cursor(dictionary=True)

            if action == "Login":
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
                user = cursor.fetchone()
                cursor.close()
                conn.close()

                if user:
                    session['user'] = user['username']
                    session['role'] = user['role']
                    flash("Login successful!", "success")
                    return redirect(url_for('dashboard'))
                else:
                    flash("Invalid username or password. Please try again.", "danger")

            elif action == "Register":
                role = request.form['role'].lower()

                if role not in ["admin", "staff"]:
                    flash("Invalid role. Please enter 'Admin' or 'Staff'.", "danger")
                    return redirect(url_for('auth'))

                try:
                    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                                (username, password, role))
                    conn.commit()
                    session['user'] = username
                    session['role'] = role
                    flash("Registration successful! You are now logged in.", "success")
                    return redirect(url_for('dashboard'))
                except mysql.connector.IntegrityError:
                    flash("Username already exists. Please choose a different one.", "danger")
                finally:
                    cursor.close()
                    conn.close()

        return render_template('auth.html')
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: 
        return redirect(url_for('auth'))  
    return render_template('dashboard.html')

@app.route('/view_product')
def viewProduct():
    conn = Database.getConnection()
    cursor = conn.cursor(dictionary=True) 
    cursor.execute("SELECT id, product_name, product_quantity, product_price FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('view_product.html', products=products)

@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    conn = Database.getConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    conn.close()
    flash("Product deleted successfully!", "success")
    return redirect(url_for("viewProduct"))

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    conn = Database.getConnection()
    cursor = conn.cursor(dictionary=True)  # Fetch results as dictionaries

    if request.method == "POST":
        product_name = request.form["product_name"]
        product_price = request.form["product_price"]
        product_quantity = request.form["product_quantity"]

        # Update query
        query = """
        UPDATE products
        SET product_name = %s, product_price = %s, product_quantity = %s
        WHERE id = %s
        """
        cursor.execute(query, (product_name, product_price, product_quantity, product_id))
        conn.commit()  # Save changes

        flash("Product updated successfully!", "success")
        cursor.close()
        conn.close()
        return redirect(url_for("viewProduct"))  # Redirect to product list

    # Fetch product details for pre-filling the form
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()

    cursor.close()
    conn.close()

    if product:
        return render_template("edit_product.html", product=product)
    else:
        flash("Product not found!", "danger")
        return redirect(url_for("viewProduct"))


@app.route('/add_product', methods=['GET', 'POST'])
def addProduct():
    if request.method == 'POST':
        product_name = request.form['product_name']
        category = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']

        conn = Database.getConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (product_name, category, price, quantity) VALUES (?, ?, ?, ?)", 
                     (product_name, category, price, quantity))
        conn.commit()
        conn.close()

        flash("Product added successfully.", 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_product.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('auth'))

@app.route('/monthly_report')
def monthly_report():
    conn = Database.getConnection()
    cursor = conn.cursor(dictionary=True)

    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # SQL query to get sales data for the current month
    query = """
    SELECT p.product_name AS product_name, 
       SUM(t.quantity) AS total_quantity, 
       SUM(t.total_price) AS total_sales
    FROM transactions t
    JOIN products p ON t.product_id = p.id
    WHERE t.transaction_type = 'sale' 
        AND MONTH(t.transaction_date) = %s
        AND YEAR(t.transaction_date) = %s
    GROUP BY p.product_name;


    """
    
    cursor.execute(query, (current_month, current_year))
    sales_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('monthly_report.html', sales_data=sales_data)

@app.route('/stock_report')
def stock_report():
    conn = Database.getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT product_name, product_quantity, product_price FROM products")
    stock_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('stock_report.html', stock_data=stock_data)

from datetime import datetime

@app.route('/record_sales', methods=['GET', 'POST'])
def record_sales():
    conn = Database.getConnection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch available products (with stock > 0)
    cursor.execute("SELECT id, product_name, product_quantity, product_price FROM products WHERE product_quantity > 0")
    products = cursor.fetchall()
    
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        customer_name = request.form['customer']
        transaction_date = request.form['date']  # Get transaction date from form

        # Get product details
        cursor.execute("SELECT product_price, product_quantity FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            flash("Invalid product selection.", "danger")
        elif quantity > product['product_quantity']:
            flash("Not enough stock available!", "danger")
        else:
            total_price = product['product_price'] * quantity

            # Insert the sales record into transactions table
            cursor.execute("""
                INSERT INTO transactions (product_id, quantity, total_price, transaction_date, transaction_type, customer_name)
                VALUES (%s, %s, %s, %s, 'sale', %s)
            """, (product_id, quantity, total_price, transaction_date, customer_name))

            # Update product stock
            cursor.execute("UPDATE products SET product_quantity = product_quantity - %s WHERE id = %s", 
                           (quantity, product_id))
            conn.commit()
            flash("Sale recorded successfully!", "success")

    cursor.execute("""
        SELECT t.transaction_id, p.product_name, t.quantity, t.total_price, t.transaction_date, t.customer_name
        FROM transactions t
        JOIN products p ON t.product_id = p.id
        WHERE t.transaction_type = 'sale'
        ORDER BY t.transaction_date DESC
    """)
    sales_records = cursor.fetchall()
    
    conn.close()
    return render_template('record_sales.html', products=products, sales_records = sales_records)

@app.route('/record_purchase', methods=['GET', 'POST'])
def record_purchase():
    conn = Database.getConnection()
    cursor = conn.cursor(dictionary=True)

    # Fetch existing products for the dropdown
    cursor.execute("SELECT id, product_name FROM products")
    products = cursor.fetchall()

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        new_product_name = request.form.get('new_product_name')
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        date = request.form['date']
        supplier = request.form['supplier']

        # If the user selects an existing product
        if product_id and product_id != "new":
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()

            if product:
                # Update existing product stock
                cursor.execute("UPDATE products SET product_quantity = product_quantity + %s WHERE id = %s",
                               (quantity, product_id))
            else:
                flash("Invalid product selection.", "danger")
                return redirect(url_for('record_purchase'))

        # If the user adds a new product
        elif new_product_name:
            cursor.execute("INSERT INTO products (product_name, product_quantity, product_price) VALUES (%s, %s, %s)",
                           (new_product_name, quantity, price))
            conn.commit()
            product_id = cursor.lastrowid  # Get the new product ID

        else:
            flash("Please select a product or add a new one.", "danger")
            return redirect(url_for('record_purchase'))

        # Insert into transactions table
        cursor.execute("""
            INSERT INTO transactions (product_id, quantity, total_price, transaction_date, transaction_type, supplier_name)
            VALUES (%s, %s, %s, %s, 'purchase', %s)
        """, (product_id, quantity, price * quantity, date, supplier))

        conn.commit()
        flash("Purchase recorded successfully!", "success")

    # Fetch all purchase records to display
    cursor.execute("""
        SELECT t.transaction_id, p.product_name, t.quantity, t.total_price, t.transaction_date, t.supplier_name
        FROM transactions t
        JOIN products p ON t.product_id = p.id
        WHERE t.transaction_type = 'purchase'
        ORDER BY t.transaction_date DESC
    """)
    purchase_records = cursor.fetchall()

    conn.close()
    return render_template('record_purchase.html', products=products, purchase_records=purchase_records)

if __name__ == '__main__':
    Database.initializeDatabase()
    app.run(debug = True)
