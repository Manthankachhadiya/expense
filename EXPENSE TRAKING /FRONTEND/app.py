import streamlit as st
import pandas as pd
from datetime import datetime
import requests

API_URL = "http://127.0.0.1:8001"

st.title("💰 Expenses Management System")

tab1, tab2 = st.tabs(["➕ ADD / UPDATE", "📊 ANALYTICS"])

with tab1:
    selected_date = st.date_input("Select Date", datetime(2024, 8, 1))

    # Format the date to match the FastAPI expected input
    date_str = selected_date.strftime("%Y-%m-%d")

    try:
        response = requests.get(f"{API_URL}/expenses/{date_str}")
        if response.status_code == 200:
            existing_expenses = response.json()
            st.subheader("🧾 Existing Expenses")
            if existing_expenses:
                df = pd.DataFrame(existing_expenses)
                st.dataframe(df)
            else:
                st.info("No expenses found for the selected date.")
        else:
            st.error("Failed to fetch expenses from the backend.")
            existing_expenses = []
    except requests.exceptions.ConnectionError:
        st.error("🚨 Backend server is not running. Please start FastAPI server (server.py).")
        st.stop()

    st.subheader("➕ Add New Expense")
    with st.form("expense_form", clear_on_submit=True):
        amount = st.number_input("Amount", min_value=0.0, step=0.5)
        category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
        notes = st.text_input("Notes")
        submitted = st.form_submit_button("Add / Update")

        if submitted:
            new_expense = [{
                "amount": amount,
                "category": category,
                "notes": notes
            }]

            try:
                post_response = requests.post(f"{API_URL}/expenses/{date_str}", json=new_expense)
                if post_response.status_code == 200:
                    st.success("✅ Expense saved successfully!")
                    st.experimental_rerun()  # Refresh page to show updated data
                else:
                    st.error("❌ Failed to save expense.")
            except requests.exceptions.ConnectionError:
                st.error("🚨 Failed to connect to backend. Is FastAPI running?")


# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import requests

# # API configuration
# API_URL = "http://127.0.0.1:8080"

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
#         st.rerun()  # Updated from experimental_rerun
    
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
#                         st.rerun()  # Updated from experimental_rerun
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
#                     st.rerun()  # Updated from experimental_rerun
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






import streamlit as st
import pandas as pd
from datetime import datetime
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Expenses management system")

tab1, tab2 = st.tabs(["ADD/UPDATE", "ANALYTICS"])

with tab1:
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")
    response = requests.get("{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
        st.write("existing_expenses")
    else:
        st.error("fail")
        existing_expenses = []


# st.title("Expenses management system")

# st.header("Streamlit Core Features")
# st.subheader("Text Elements")
# st.text("This is a simple text elements")

# st.subheader("Data Display")
# st.write("Here is a simple table:")

# df = pd.DataFrame({
#     "Date": ["2025-08-01", "2025-08-02", "2025-08-02"],
#     "Amount": [250, 134, 340]
# })
# st.table(df)

# st.subheader("chat")
# st.line_chart([1,2,3,4])

# st.subheader("User Input")
# value = st.slider("select a value", 0, 100)
# st.write(f"selected value: {value}")

# st.title("Interactive Widgets Example")

# if st.checkbox("Show/Hide"):
#     st.write("Checkbox is checked!")

# option = st.selectbox("Select a number", [1, 2, 3, 4])
# st.write(f"You selected: {option}")

# options = st.multiselect("Select multiple numbers", [1, 2, 3, 4])
# st.write(f"You selected: {options}")

# expense_dt = st.date_input("Expense Date:")

# if expense_dt:
#     st.write(f"Fetchng expenses for {expense_dt}")

