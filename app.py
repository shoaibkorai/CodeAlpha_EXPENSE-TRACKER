from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.balance = 0

    def set_salary(self, salary):
        self.balance = salary

    def add_expense(self, amount, category):
        self.expenses.append({
            'amount': amount,
            'category': category.lower(),  # Convert category to lowercase
            'date': datetime.now().strftime("%Y-%m-%d")  # Add current date
        })

    def get_summary(self):
        total_expenses = sum(expense['amount'] for expense in self.expenses)
        category_summary = {}
        for expense in self.expenses:
            category = expense['category'].upper()  # Convert category to uppercase
            if category not in category_summary:
                category_summary[category] = []
            category_summary[category].append({'amount': expense['amount'], 'date': expense['date']})
        balance = self.balance - total_expenses
        return total_expenses, balance, category_summary

tracker = ExpenseTracker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = float(request.form['amount'])
    category = request.form['category']
    tracker.add_expense(amount, category)
    return render_template('index.html', message="Expense added successfully!")

@app.route('/view_summary')
def view_summary():
    total_expenses, balance, category_summary = tracker.get_summary()
    return render_template('summary.html', total_expenses=total_expenses, balance=balance, category_summary=category_summary)

@app.route('/set_salary', methods=['POST'])
def set_salary():
    salary = float(request.form['salary'])
    tracker.set_salary(salary)
    return render_template('index.html', message="Salary set successfully!")

if __name__ == '__main__':
    app.run(debug=True)
