import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Using the code from python_ui_account_search.py
def search_and_display(account_number_entry, predictions_tree, historical_tree):
    """
    Searches for an account number in predictions.csv and displays the result,
    along with the account's historical data from historical_data.csv.

    Args:
        account_number_entry (ttk.Entry): Entry widget containing the account number to search for.
        predictions_tree (ttk.Treeview): Treeview widget to display the prediction result.
        historical_tree (ttk.Treeview): Treeview widget to display the historical data.
    """
    account_number = account_number_entry.get()

    if not account_number:
        messagebox.showerror("Error", "Please enter an account number.")
        return

    try:
        account_number = int(account_number)
    except ValueError:
        messagebox.showerror("Error", "Invalid account number. Please enter a number.")
        return

    try:
        predictions_df = pd.read_csv("predictions.csv")
        historical_df = pd.read_csv("historical_data.csv")
    except FileNotFoundError:
        messagebox.showerror("Error", "One or both of the CSV files (predictions.csv, historical_data.csv) not found.  Please make sure they are in the same directory as the script.")
        return

    # Clear previous results
    for item in predictions_tree.get_children():
        predictions_tree.delete(item)
    for item in historical_tree.get_children():
        historical_tree.delete(item)

    # Search for the account in predictions.csv
    prediction_result = predictions_df[predictions_df['account'] == account_number]
    if not prediction_result.empty:
        predictions_tree.insert("", "end", values=prediction_result.iloc[0].to_list())
    else:
        predictions_tree.insert("", "end", values=["Account not found in predictions.csv"])

    # Display historical data for the account
    historical_data = historical_df[historical_df['account'] == account_number]
    if not historical_data.empty:
        for _, row in historical_data.iterrows():
            historical_tree.insert("", "end", values=row.to_list())
    else:
        historical_tree.insert("", "end", values=["No historical data found for this account."])

def create_ui():
    """
    Creates the main Tkinter UI window with labels, entry fields, buttons, and treeviews.
    """
    root = tk.Tk()
    root.title("Account Search")

    # Label and entry for account number
    account_label = ttk.Label(root, text="Enter Account Number:")
    account_label.pack(pady=10)
    account_number_entry = ttk.Entry(root)
    account_number_entry.pack(pady=10)

    # Search button
    search_button = ttk.Button(root, text="Search", command=lambda: search_and_display(account_number_entry, predictions_tree, historical_tree))
    search_button.pack(pady=10)

    # Treeview for predictions.csv result
    predictions_label = ttk.Label(root, text="Prediction Result (predictions.csv):")
    predictions_label.pack(pady=10)
    predictions_tree = ttk.Treeview(root, columns=list(pd.read_csv("predictions.csv").columns), show="headings")
    for col in list(pd.read_csv("predictions.csv").columns):
        predictions_tree.heading(col, text=col)
    predictions_tree.pack(pady=10)

    # Treeview for historical data
    historical_label = ttk.Label(root, text="Historical Data (historical_data.csv):")
    historical_label.pack(pady=10)
    historical_frame = ttk.Frame(root)  # Create a frame for the Treeview and scrollbar
    historical_frame.pack(pady=10, fill="both", expand=True)
    historical_tree = ttk.Treeview(historical_frame, columns=list(pd.read_csv("historical_data.csv").columns), show="headings", yscrollcommand=lambda *args: y_scrollbar.set(*args), xscrollcommand=lambda *args: x_scrollbar.set(*args))
    for col in list(pd.read_csv("historical_data.csv").columns):
        historical_tree.heading(col, text=col)
        historical_tree.column(col, width=100)  # Set a default width, adjust as needed
    historical_tree.pack(side="left", fill="both", expand=True)

    y_scrollbar = ttk.Scrollbar(historical_frame, orient="vertical", command=historical_tree.yview)
    y_scrollbar.pack(side="right", fill="y")
    x_scrollbar = ttk.Scrollbar(historical_frame, orient="horizontal", command=historical_tree.xview)
    x_scrollbar.pack(side="bottom", fill="x")

    historical_tree.configure(xscrollcommand=x_scrollbar.set)
    historical_tree.configure(yscrollcommand=y_scrollbar.set)


    root.mainloop()

if __name__ == "__main__":
    create_ui()

