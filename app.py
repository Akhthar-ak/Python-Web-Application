
from flask import Flask, render_template, request, redirect, send_file
import json, os, csv
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
FILE_NAME = "expenses.json"

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_expenses(expenses):
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f, indent=4)

@app.route("/")
def index():
    expenses = load_expenses()
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += float(e["amount"])
    return render_template("index.html", expenses=expenses, totals=totals)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        expenses = load_expenses()
        expense = {
            "id": len(expenses) + 1,
            "date": request.form["date"],
            "title": request.form["title"],
            "category": request.form["category"],
            "amount": request.form["amount"]
        }
        expenses.append(expense)
        save_expenses(expenses)
        return redirect("/")
    return render_template("add.html")

@app.route("/delete/<int:eid>")
def delete(eid):
    expenses = load_expenses()
    expenses = [e for e in expenses if e["id"] != eid]
    save_expenses(expenses)
    return redirect("/")

@app.route("/export")
def export():
    expenses = load_expenses()
    file_path = "expenses.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Title", "Category", "Amount"])
        for e in expenses:
            writer.writerow([e["date"], e["title"], e["category"], e["amount"]])
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
