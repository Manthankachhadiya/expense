from fastapi import FastAPI
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel


class Expense(BaseModel):
    amount: float
    category: str
    notes: str

app = FastAPI()




@app.get("/expenses/{expenses_date}", response_model=List[Expense])
def get_expenses(expenses_date: date):
    expenses = db_helper.fetch_expenses_for_date(expenses_date)
    return expenses
    

@app.post("/expenses/{expenses_date}")
def add_or_update_expense(expenses_date: date, expenses: List[Expense]):
    db_helper.delete_expense_for_date(expenses_date)
    for expense in expenses:
        db_helper.insert_expense(expenses_date, expense.amount, expense.category, expense.notes)

    return {"message": "Successfully updated"}
