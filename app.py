import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from fpdf import FPDF
from flask import make_response

app = Flask(__name__)

#1. Database Configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

CATEGORY_MAP = {
    'uber': 'Transport',
    'lyft': 'Transport',
    'amazon': 'Shopping',
    'netflix': 'Entertainment',
    'starbucks': 'Food & Drink',
    'walmart': 'Groceries',
    'shell': 'Fuel',
    'apple': 'Tech/Subscriptions'
}

# 2. The transaction Model

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)

# 3. Create the database file
with app.app_context():
    db.create_all()

# 4. Main route
@app.route('/')
def index():
     
     #to get the month from the browser data(eg/ month = 01)
    selected_month = request.args.get('month', '')
    
    #start a query for all transactions
    query = Transaction.query

    if selected_month:
        query = query.filter(Transaction.date.contains(f"-{selected_month}-"))

    transactions = query.all()

    total_spent = 0 # Default if no data exists
    
    if transactions:
        data = [{'Category': t.category, 'Amount': t.amount} for t in transactions]
        df = pd.DataFrame(data)

        #calculate total
        total_spent = df['Amount'].sum()
        
        summary = df.groupby('Category')['Amount'].sum().reset_index()
        labels = summary['Category'].tolist()
        values = summary['Amount'].tolist()
    else:
        labels, values = [], []

    # Pass 'transactions' into the template
    return render_template('index.html', labels=labels, values=values, transactions=transactions,total_spent=total_spent,selected_month=selected_month)

    
   

@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # checking if a file was actually sent
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']

    if file.filename == '':
        return 'no selected file'

    if 'file' and file.filename.endswith('.csv'):
        # save the file temprory
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Read the CSV using Pandas
        try:
            df = pd.read_csv(filepath)

            
            for index, row in df.iterrows():

                desc = str(row.get('Description', "")).lower()
                final_category = row['Category'] # Fallback to CSV value

                # Check if any keyword matches the description
                for keyword, mapped_category in CATEGORY_MAP.items():
                    if keyword in desc:
                        final_category = mapped_category
                        break

                 #loop through the rows and save to Database

                new_transaction = Transaction(
                    date=str(row['Date']),
                    category=final_category,
                    description=row.get('Description', ""),
                    amount=float(row['Amount'])
                )
                db.session.add(new_transaction)

            db.session.commit()

            # deletes the file after reading it
            os.remove(filepath)
            return redirect(url_for('index'))

        except Exception as e:
            return f"Error procssing file: {e}"
    return "Invalid file type.Please upload a CSV."

@app.route('/clear')
def clear_data():
    try:
        #To delete all rows in the transaction table
        db.session.query(Transaction).delete()
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error clearing data: {e}"
    
@app.route('/export')
def export_pdf():

    # to get the data
    transactions = Transaction.query.all()

    # pdf setup
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "Personal Finance Report", ln=True, align="C")
    pdf.ln(10) #Line break

    # Table Header
    pdf.set_font('Arial', "B", 12)
    pdf.cell(40, 10, "Date", 1)
    pdf.cell(50, 10, "Category", 1)
    pdf.cell(60, 10, "Description", 1)
    pdf.cell(40, 10, "Amount", 1)
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", size=10)
    total = 0
    for t in transactions:
        pdf.cell(40, 10, str(t.date), 1)
        pdf.cell(50, 10, str(t.category), 1)
        pdf.cell(60, 10, str(t.description), 1)
        pdf.cell(40, 10, f"${t.amount:.2f}", 1)
        pdf.ln()
        total += t.amount

    #  Final Total
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, f"Total Spending: ${total:.2f}", 0, 1, 'R')

    # Send to Browser
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Dispostion'] = 'inline; filename=report.pdf'
    return response

if __name__ == "__main__":
    app.run(debug=True)