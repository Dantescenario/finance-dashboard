Markdown

# 📊 Personal Finance Dashboard

A full-stack Python web application designed to help users track, categorize, and analyze their spending habits. This tool transforms messy bank CSV exports into clear visual insights and professional PDF reports.



## 🚀 Features

* **Smart Categorization:** Automatically assigns categories (like 'Transport' or 'Groceries') by scanning transaction descriptions for specific keywords (Uber, Amazon, etc.).
* **Dynamic Visualizations:** Interactive doughnut charts powered by **Chart.js** to visualize spending by category.
* **Month Filtering:** Quickly filter data to view spending for specific months or the entire year.
* **PDF Reporting:** Generate and download a professional-formatted PDF summary of all transactions.
* **CSV Data Ingestion:** Upload standard bank CSV files to populate the dashboard instantly.
* **Database Management:** Full CRUD (Create, Read, Update, Delete) capabilities using **SQLAlchemy** and **SQLite**.

---

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask
* **Data Processing:** Pandas (for grouping and totals)
* **Database:** SQLAlchemy (SQLite)
* **Frontend:** HTML5, CSS3, JavaScript (Chart.js)
* **PDF Generation:** FPDF

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd finance-dashboard
Create and activate a virtual environment:

PowerShell

python -m venv venv
.\venv\Scripts\activate
Install dependencies:

Bash

pip install flask flask-sqlalchemy pandas fpdf
Run the application:

Bash

python app.py
The app will be available at http://127.0.0.1:5000/

📂 Project Structure
Plaintext

├── app.py              # Main Flask application logic & routes
├── finance.db          # SQLite database (generated automatically)
├── uploads/            # Temporary storage for uploaded CSVs
├── templates/          # HTML files (index.html, upload.html)
├── static/
│   ├── css/            # Custom styling
│   └── js/             # Frontend chart logic
└── venv/               # Python virtual environment
📝 How to use
Prepare a CSV file with headers: Date, Category, Description, Amount.

Click Upload CSV and select your file.

View your Total Spending and Category Chart on the main dashboard.

Use the Filter by Month dropdown to drill down into specific data.

Click Download PDF Report to save a hard copy of your finances.