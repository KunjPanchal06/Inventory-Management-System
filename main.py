import mysql.connector
from prettytable import PrettyTable
from datetime import datetime

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

class Menu:
    @staticmethod
    def displayStartMenu():
        print("------------------Inventory Management System------------------")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

    @staticmethod
    def displayStaffMenu():
        print("------------------Inventory Management System------------------")
        print("1. View Products")
        print("2. Add Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. Back")

    @staticmethod
    def displayAdminMenu():
        print("------------------Inventory Management System------------------")
        print("1. View Products")
        print("2. Add Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. Generate Monthly Report")
        print("6. Generate Stock Report")
        print("7. Record Sales")
        print("8. Record Purchases")
        print("9. Back")

class Authentication:
    @staticmethod
    def login():
        username = input("Enter your Username: ")
        password = input("Enter your Password: ")

        conn = Database.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            print(f"Login Successful. Welcome {username}")
            role = user[3]
            return True, role
        else:
            print("Invalid username or password. Please try again.")
            return False

    @staticmethod
    def register():
        username = input("Enter your Username: ")
        password = input("Enter your Password: ")
        role = input("Enter your Role (Admin/Staff): ").lower()

        if role not in ["admin", "staff"]:
            print("Invalid role. Please enter 'Admin' or 'Staff'.")
            return

        conn = Database.getConnection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                           (username, password, role))
            conn.commit()
            print("Registration Successful")
        except mysql.connector.IntegrityError:
            print("Username already exists. Please try again.")
        finally:
            cursor.close()
            conn.close()


class Product:
    @staticmethod
    def viewProducts():
        conn = Database.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Product ID", "Product Name", "Product Quantity", "Product Price"]
        for product in products:
            table.add_row(product)
        print(table)
        cursor.close()
        conn.close()

    @staticmethod
    def addProduct():
        conn = Database.getConnection()
        cursor = conn.cursor()
        product_name = input("Enter the name of the product: ")
        product_quantity = input("Enter the quantity of the product: ")
        product_price = input("Enter the price of the product: ")
        cursor.execute("INSERT INTO products (product_name, product_quantity, product_price) VALUES (%s, %s, %s)", (product_name,product_quantity, product_price))
        conn.commit()
        cursor.close()
        conn.close()
        print("Product added successfully.")

    @staticmethod
    def editProduct():
        conn = Database.getConnection()
        cursor = conn.cursor()
        product_id = input("Enter the ID of the product to edit: ")
        product_name = input("Enter the new name of the product: ")
        product_quantity = input("Enter the new quantity of the product: ")
        product_price = input("Enter the new price of the product: ")
        cursor.execute("UPDATE products SET product_name = %s, product_quantity = %s, product_price = %s WHERE id = %s", (product_name,product_quantity, product_price, product_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def deleteProduct():
        conn = Database.getConnection()
        cursor = conn.cursor()
        product_id = input("Enter the ID of the product to delete: ")
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Product deleted successfully.")

class Report:
    @staticmethod
    def generateMonthlyReport():
        today = datetime.today().date()
        month_start = today.replace(day=1)
        conn = Database.getConnection()
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT p.product_name, SUM(t.quantity) AS total_quantity, SUM(t.total_price) AS total_sales
                    FROM transactions t
                    JOIN products p ON t.product_id = p.id
                    WHERE DATE(t.transaction_date) >= %s
                    GROUP BY p.product_name
                """, (month_start,))

        sales_data = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Product Name", "Quantity Sold", "Total Sales"]

        for row in sales_data:
            table.add_row(row)

        print(f"--- Monthly Sales Report for {today.strftime('%B %Y')} ---")
        print(table)

        cursor.close()
        conn.close()

    @staticmethod
    def generateStockReport():
        conn = Database.getConnection()
        cursor = conn.cursor()
        cursor.execute(' SELECT product_name, product_quantity FROM products ')
        stock_data = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Product Name", "Stock Quantity"]

        for row in stock_data:
            table.add_row(row)

        print("--- Current Stock Report ---")
        print(table)

        cursor.close()
        conn.close()

class Transactions:
    @staticmethod
    def recordSale():
        conn = Database.getConnection()
        cursor = conn.cursor()

        try:
            product_id = int(input("Enter the Product ID: "))
            quantity = int(input("Enter the Quantity Sold: "))
            cursor.execute("SELECT product_price, product_quantity FROM products WHERE id = %s", (product_id,))
            result = cursor.fetchone()

            if not result:
                print("Invalid Product ID.")
                return

            product_price, current_quantity = result

            if quantity > current_quantity:
                print("Insufficient stock. Sale cannot be processed.")
                return

            total_price = product_price * quantity
            cursor.execute("INSERT INTO transactions (product_id, quantity, total_price, transaction_date) VALUES (%s, %s, %s, %s)",
                           (product_id, quantity, total_price, datetime.now()))
            cursor.execute("UPDATE products SET product_quantity = product_quantity - %s WHERE id = %s",
                           (quantity, product_id))
            conn.commit()
            print(f"Sale recorded successfully. Total Price: {total_price:.2f}")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def recordPurchase():
        conn = Database.getConnection()
        cursor = conn.cursor()

        try:
            product_id = int(input("Enter the Product ID: "))
            quantity = int(input("Enter the Quantity Purchased: "))
            cursor.execute("SELECT product_price FROM products WHERE id = %s", (product_id,))
            result = cursor.fetchone()

            if not result:
                print("Invalid Product ID.")
                return

            product_price = result[0]
            total_price = product_price * quantity

            cursor.execute("UPDATE products SET product_quantity = product_quantity + %s WHERE id = %s",
                           (quantity, product_id))
            conn.commit()
            print(f"Purchase recorded successfully. Total Cost: {total_price:.2f}")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    Database.initializeDatabase()
    run = True
    while run:
        Menu.displayStartMenu()
        try:
            choice = int(input("Enter your choice: "))
            if choice < 1 or choice > 3:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue

        if choice == 1:
            success, role = Authentication.login()
            if success:
                if role == "admin":
                    while True:
                        Menu.displayAdminMenu()
                        try:
                            admin_choice = int(input("Enter your choice: "))
                            if admin_choice < 1 or admin_choice > 9:
                                raise ValueError
                        except ValueError:
                            print("Invalid input. Please enter a number between 1 and 9.")

                        if admin_choice == 1:
                            Product.viewProducts()
                        elif admin_choice == 2:
                            Product.addProduct()
                        elif admin_choice == 3:
                            Product.editProduct()
                        elif admin_choice == 4:
                            Product.deleteProduct()
                        elif admin_choice == 5:
                            Report.generateMonthlyReport()
                        elif admin_choice == 6:
                            Report.generateStockReport()
                        elif admin_choice == 7:
                            Transactions.recordSale()
                        elif admin_choice == 8:
                            Transactions.recordPurchase()
                        elif admin_choice == 9:
                            break

                elif role == "staff":
                    while True:
                        Menu.displayStaffMenu()
                        try:
                            menu_choice = int(input("Enter your choice: "))
                            if menu_choice < 1 or menu_choice > 5:
                                raise ValueError
                        except ValueError:
                            print("Invalid input. Please enter a number between 1 and 5.")
                            continue

                        if menu_choice == 1:
                            Product.viewProducts()
                        elif menu_choice == 2:
                            Product.addProduct()
                        elif menu_choice == 3:
                            Product.editProduct()
                        elif menu_choice == 4:
                            Product.deleteProduct()
                        elif menu_choice == 5:
                            break

        elif choice == 2:
            Authentication.register()

        elif choice == 3:
            print("Exiting Inventory Management System.")
            run = False
