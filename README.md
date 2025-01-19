# Inventory Management System

This project is a **role-based Inventory Management System** built using Python and MySQL. It provides tools for managing inventory, tracking sales and purchases, and generating insightful reports to streamline business operations.

## 🚀 Features

### 📦 Inventory Management
- View available products in a tabular format.
- Add, edit, and delete product details.

### 🔑 Role-Based Access Control
- **Admin Role**: Full access to all features, including reporting and transactions.
- **Staff Role**: Limited access to inventory management tasks.

### 📊 Reporting
- **Monthly Sales Report**: Summarizes sales data for better decision-making.
- **Stock Report**: Displays current inventory levels.

### 💰 Transactions
- Record sales to update stock levels automatically.
- Record purchases to add new stock to the inventory.

## 🛠️ Tech Stack
- **Python**: Backend logic and user interaction.
- **MySQL**: Database management for secure and efficient data handling.
- **PrettyTable**: Used for displaying data in a clean tabular format.
- **Flask Framework** (Future Integration): Transforming the system into a web application.
- **HTML & CSS** (Future Development): Building a visually appealing and intuitive user interface.

## 📂 Database Setup
Ensure your MySQL database is set up with the following tables:

### `users` Table
| Column    | Type          | Description                |
|-----------|---------------|----------------------------|
| id        | INT (Primary Key) | Unique user ID            |
| username  | VARCHAR(50)   | User's login name          |
| password  | VARCHAR(50)   | User's password            |
| role      | VARCHAR(10)   | Role: `admin` or `staff`   |

### `products` Table
| Column           | Type          | Description                |
|-------------------|---------------|----------------------------|
| id               | INT (Primary Key) | Unique product ID         |
| product_name      | VARCHAR(100)  | Name of the product        |
| product_quantity  | INT           | Available quantity         |
| product_price     | DECIMAL(10, 2)| Price per unit             |

### `transactions` Table
| Column           | Type            | Description                |
|-------------------|-----------------|----------------------------|
| id               | INT (Primary Key) | Unique transaction ID      |
| product_id       | INT             | ID of the product involved |
| quantity         | INT             | Quantity sold/purchased    |
| total_price      | DECIMAL(10, 2)  | Total cost of transaction  |
| transaction_date | DATETIME        | Date and time of transaction |

## 🔧 Configuration
1. Replace the following placeholders in the code with your MySQL credentials:
   ```python
   userName = "your_username"
   passWord = "your_password"
   hostName = "your_hostName"
   databaseName = "your_databaseName"
