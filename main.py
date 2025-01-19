import mysql.connector

class Database:
    @staticmethod
    def initializeDatabase():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="inventory_management"
        )
        cursor = conn.cursor()
        cursor.close()

class Function:
    @staticmethod
    def displayMenu():
        print("------------------Inventory Management System------------------")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

    @staticmethod
    def login():
        username = input("Enter your Username: ")
        password = input("Enter your Password: ")

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="inventory_management"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            print(f"Login Successful. Welcome {username}")
        else:
            print("Invalid username or password. Please try again.")

    @staticmethod
    def register():
        username = input("Enter your Username: ")
        password = input("Enter your Password: ")

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="inventory_management"
        )
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            print("Registration Successful")
        except mysql.connector.IntegrityError:
            print("Username already exists. Please try again.")
        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    Database.initializeDatabase()
    run = True
    while run:
        Function.displayMenu()
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue

        if choice == 1:
            Function.login()
        elif choice == 2:
            Function.register()
        elif choice == 3:
            print("Exiting Inventory Management System.")
            run = False
        else:
            print("Enter a valid choice.")