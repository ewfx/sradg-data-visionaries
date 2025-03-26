import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_balance_data(start_date, num_months=6):
    """Generates balance data with random 7-digit accounts, 4-digit 'au', specified secondary accounts, various currencies, and company numbers from 0 to 100, with 5-10 records per account and mixed match statuses."""

    data = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    account_au_map = {}  # Dictionary to store account-au mappings

    secondary_accounts = ['deferred costs', 'deferred origination fees', 'principal']
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF']

    for _ in range(num_months):
        account_dates = {}  # Dictionary to track (account, asofdt) pairs for uniqueness this month
        num_accounts = np.random.randint(3, 6)  # Generate 3 to 5 accounts per month
        for _ in range(num_accounts):
            account = np.random.randint(1000000, 9999999)  # 7-digit account number

            # Generate 'au' if account is new, otherwise retrieve from map
            if account not in account_au_map:
                au = np.random.randint(1000, 9999)  # 4-digit 'au'
                account_au_map[account] = au
            else:
                au = account_au_map[account]

            num_records = np.random.randint(5, 11)  # Generate 5-10 records per account
            for _ in range(num_records):
                asofdt_str = current_date.strftime('%Y-%m-%d')
                # Ensure unique (account, asofdt) combination for the month
                while (account, asofdt_str) in account_dates:
                    current_date += timedelta(days=1)  # Increment date if duplicate
                    asofdt_str = current_date.strftime('%Y-%m-%d')

                account_dates[(account, asofdt_str)] = True  # Mark combination as used

                gl_balance = np.random.randint(10000, 30000)
                # Introduce some logic to ensure a mix of matches and breaks
                if np.random.rand() < 0.8:  # Adjust probability as needed (e.g., 0.8 for 80% matches)
                    ihub_balance = gl_balance + np.random.randint(-1, 2)  # Small difference for "Match"
                else:
                    ihub_balance = gl_balance + np.random.randint(-5000, 5000)  # Larger difference for "Break"

                balance_difference = gl_balance - ihub_balance

                if abs(balance_difference) <= 1:
                    match_status = "Match"
                    comments = "Difference is within tolerance (less than 1 USD)"
                else:
                    match_status = "Break"
                    comments = ""

                secondary_account = np.random.choice(secondary_accounts)
                currency = np.random.choice(currencies)
                company = np.random.randint(0, 101)  # Random company number from 0 to 100

                data.append({
                    "asofdt": asofdt_str,
                    "company": company,
                    "account": account,
                    "au": au,
                    "currency": currency,
                    "primary account": "all other loans",
                    "secondary account": secondary_account,
                    "gl balance": gl_balance,
                    "ihub balance": ihub_balance,
                    "balance difference": balance_difference,
                    "match status": match_status,
                    "comments": comments,
                })
        current_date += timedelta(days=30)
    return pd.DataFrame(data)

# Generate data starting from '2024-01-01'
df = generate_balance_data('2024-01-01')

# Export the DataFrame to a CSV file
df.to_csv("historical_data.csv", index=False)
