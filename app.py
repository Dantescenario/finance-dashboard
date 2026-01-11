import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

#1. Database Configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

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
    # fetch all transaction from the database
    transactions = Transaction.query.all()

    # use pandas to group data by category
    if transactions:
        data =  [{'Category': t.category, 'Amount': t.amount} for t in transactions]
        df = pd.DataFrame(data)

        # Sum the amount for each category
        summary = df.groupby('Category')['Amount'].sum().reset_index()

        # Prepare labels and values for chart.js
        labels = summary['Category'].tolist()
        values = summary['Amount'].tolist()
    else:
        labels, values = [], []

    return render_template('index.html', labels=labels, values=values)

    
   

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

            #loop through the rows and save to Database
            for index, row in df.iterrows():
                new_transaction = Transaction(
                    date=str(row['Date']),
                    category=row['Category'],
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

if __name__ == "__main__":
    app.run(debug=True)