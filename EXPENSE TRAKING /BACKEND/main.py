# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(title="Expense Management API")

# Enable CORS to allow requests from Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for expenses
class Expense(BaseModel):
    id: Optional[int] = None
    date: str
    amount: float
    category: str
    description: str

# In-memory database for development
expenses_db = []
expense_id_counter = 1

# Sample data
expenses_db.append(
    Expense(
        id=expense_id_counter,
        date="2024-08-01",
        amount=25.50,
        category="Food",
        description="Lunch at restaurant"
    )
)
expense_id_counter += 1

expenses_db.append(
    Expense(
        id=expense_id_counter,
        date="2024-08-01",
        amount=35.00,
        category="Transportation",
        description="Uber ride"
    )
)
expense_id_counter += 1

# API Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to Expense Management API"}

@app.get("/expenses/{date}", response_model=List[Expense])
def get_expenses_by_date(date: str):
    """Get all expenses for a specific date"""
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Filter expenses by date
    filtered_expenses = [expense for expense in expenses_db if expense.date == date]
    return filtered_expenses

@app.post("/expenses/", response_model=Expense)
def create_expense(expense: Expense):
    """Create a new expense"""
    global expense_id_counter
    
    # Validate date format
    try:
        datetime.strptime(expense.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Add ID and save to database
    expense.id = expense_id_counter
    expense_id_counter += 1
    expenses_db.append(expense)
    return expense

@app.put("/expenses/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, updated_expense: Expense):
    """Update an existing expense"""
    for i, expense in enumerate(expenses_db):
        if expense.id == expense_id:
            # Keep the same ID
            updated_expense.id = expense_id
            expenses_db[i] = updated_expense
            return updated_expense
    
    raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    """Delete an expense"""
    for i, expense in enumerate(expenses_db):
        if expense.id == expense_id:
            del expenses_db[i]
            return {"message": f"Expense with ID {expense_id} deleted successfully"}
    
    raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)





# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import requests

# # API configuration
# API_URL = "http://127.0.0.1:8000"

# # App title
# st.title("Expenses Management System")

# # Create tabs
# tab1, tab2 = st.tabs(["ADD/UPDATE", "ANALYTICS"])

# # Function to safely fetch expenses
# def fetch_expenses(date_str):
#     try:
#         response = requests.get(f"{API_URL}/expenses/{date_str}", timeout=5)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             st.error(f"Failed to fetch data: HTTP {response.status_code}")
#             return []
#     except requests.exceptions.ConnectionError:
#         st.error("⚠️ Cannot connect to the API server. Make sure your FastAPI server is running at " + API_URL)
#         return []
#     except Exception as e:
#         st.error(f"⚠️ An error occurred: {str(e)}")
#         return []

# # Tab 1: ADD/UPDATE
# with tab1:
#     st.subheader("View and Manage Expenses")
    
#     selected_date = st.date_input("Select Date", datetime(2024, 8, 1))
    
#     # Format the date as YYYY-MM-DD
#     formatted_date = selected_date.strftime("%Y-%m-%d")
    
#     # Add a button to refresh the data
#     if st.button("Refresh Expenses"):
#         st.experimental_rerun()
    
#     # Show a loading indicator while fetching data
#     with st.spinner(f"Loading expenses for {formatted_date}..."):
#         existing_expenses = fetch_expenses(formatted_date)
    
#     # Display existing expenses if any
#     if existing_expenses and len(existing_expenses) > 0:
#         st.success(f"Found {len(existing_expenses)} expenses for {formatted_date}")
        
#         # Convert to DataFrame for better display
#         df = pd.DataFrame(existing_expenses)
#         st.dataframe(df)
        
#         # Allow deleting expenses
#         if st.checkbox("Delete an expense"):
#             expense_id = st.selectbox("Select expense to delete", 
#                                      [(exp["id"], f"${exp['amount']} - {exp['category']} - {exp['description']}") 
#                                       for exp in existing_expenses],
#                                      format_func=lambda x: x[1])
            
#             if st.button("Delete Selected Expense"):
#                 try:
#                     response = requests.delete(f"{API_URL}/expenses/{expense_id[0]}")
#                     if response.status_code == 200:
#                         st.success("Expense deleted successfully!")
#                         st.experimental_rerun()
#                     else:
#                         st.error(f"Failed to delete: {response.text}")
#                 except Exception as e:
#                     st.error(f"Error: {str(e)}")
#     else:
#         st.info(f"No expenses found for {formatted_date}")
    
#     # Form to add a new expense
#     st.subheader("Add New Expense")
#     with st.form("add_expense_form"):
#         expense_date = st.date_input("Expense Date", selected_date)
#         expense_amount = st.number_input("Amount", min_value=0.01, step=0.01, value=10.00)
#         expense_category = st.selectbox("Category", 
#                                       ["Food", "Transportation", "Housing", "Entertainment", "Utilities", 
#                                        "Healthcare", "Shopping", "Education", "Travel", "Other"])
#         expense_description = st.text_input("Description")
        
#         submit_button = st.form_submit_button("Add Expense")
        
#         if submit_button:
#             # Format the date
#             formatted_expense_date = expense_date.strftime("%Y-%m-%d")
            
#             # Create the expense object
#             new_expense = {
#                 "date": formatted_expense_date,
#                 "amount": expense_amount,
#                 "category": expense_category,
#                 "description": expense_description
#             }
            
#             try:
#                 response = requests.post(f"{API_URL}/expenses/", json=new_expense)
                
#                 if response.status_code == 200 or response.status_code == 201:
#                     st.success("Expense added successfully!")
#                     st.experimental_rerun()  # Refresh to show the new expense
#                 else:
#                     st.error(f"Failed to add expense: {response.text}")
#             except Exception as e:
#                 st.error(f"Error adding expense: {str(e)}")

# # Tab 2: ANALYTICS
# with tab2:
#     st.header("Expense Analytics")
    
#     # Date range selection for analytics
#     st.subheader("Select Date Range")
#     col1, col2 = st.columns(2)
#     with col1:
#         start_date = st.date_input("Start Date", datetime(2024, 8, 1))
#     with col2:
#         end_date = st.date_input("End Date", datetime(2024, 8, 31))
    
#     if start_date <= end_date:
#         st.info("Analytics feature is in development. This will show expense summaries and charts.")
        
#         # Placeholder for future analytics features
#         st.write("Some analytics features you could implement:")
#         st.write("1. Total expenses by category (pie chart)")
#         st.write("2. Daily expense trend (line chart)")
#         st.write("3. Monthly comparison (bar chart)")
#     else:
#         st.error("Error: End date must be after start date")