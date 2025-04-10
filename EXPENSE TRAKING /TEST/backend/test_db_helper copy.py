import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BACKEND import db_helper

# from BACKEND import db_helper

# import os
# import sys

# print("**file**:",__file__)

def test_fetch_expenses_for_date():
    expense = db_helper.fetch_expenses_for_date("2024-08-15")

    assert len(expense) == 1
    assert expense[0]['amount'] == 10.0
    assert expense[0]['catagory'] == "Shopping"
    assert expense[0]["notes"] == "Bought potatoes"