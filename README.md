# Inventory Management System (IMS)  

## 📌 Project Overview  
The **Inventory Management System (IMS)** is a **Flask-based web application** that enables businesses to efficiently manage their inventory, track product stock levels, record sales and purchases, and generate reports.  

## 🔹 Features  
✅ **User Authentication** – Secure login/logout system  
✅ **Product Management** – Add, edit, and delete products  
✅ **Stock Management** – Track product quantities in real time  
✅ **Sales Recording** – Record sales transactions and update stock accordingly  
✅ **Purchases Recording** – Record new product purchases and increase stock  
✅ **Monthly & Stock Reports** – Generate detailed reports for sales and inventory  

## 🛠️ Tech Stack  
- **Backend:** Flask (Python)  
- **Frontend:** HTML, CSS, Bootstrap  
- **Database:** MySQL with MySQL Connector  
- **Tools & Libraries:** Flask-Flash, Flask-Session  

## 📂 Project Structure  
/IMS │── /templates # HTML Templates
│ ├── add_product.html
│ ├── dashboard.html
│ ├── edit_product.html
│ ├── record_sales.html
│ ├── record_purchases.html
│ ├── monthly_report.html
│ ├── stock_report.html
│ ├── view_product.html
│── /static # Static files (CSS, JS)
│── main.py # Flask application
│── database.sql # SQL file to set up MySQL DB
│── README.md # Project documentation


## 🚀 Installation & Setup  
### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/yourusername/inventory-management.git
cd inventory-management
```

### 2️⃣ Install Dependencies
```bash
pip install flask mysql-connector-python
```

### 3️⃣ Set Up MySQL Database
Create a MySQL database
Run the database.sql file
Update main.py with your MySQL credentials

### 4️⃣ Run the Application
```bash
python main.py
```

## 📈 Future Improvements
Add REST API endpoints for external integrations
Implement role-based access control (RBAC) for different user roles
Integrate barcode scanning for inventory tracking

