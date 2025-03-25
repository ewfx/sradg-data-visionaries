import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def train_unsupervised_anomaly_model(df, account):
    """
    Trains an unsupervised anomaly detection model (Isolation Forest) for a specific account.

    Args:
        df (pd.DataFrame): The input DataFrame.
        account (int): The account number to train the model for.

    Returns:
        tuple: (model, scaler)
            model: Trained Isolation Forest model.
            scaler:  Fitted StandardScaler.  None if not applicable.
    """
    # 1. Filter data for the given account
    account_df = df[df['account'] == account].copy()

    if len(account_df) == 0:
        return None, None  # Return None if no data for the account

    # 2. Feature Engineering
    account_df['asofdt'] = pd.to_datetime(account_df['asofdt'])
    account_df['year'] = account_df['asofdt'].dt.year
    account_df['month'] = account_df['asofdt'].dt.month
    account_df['day'] = account_df['asofdt'].dt.day

    # 3. Encode Categorical Variables
    categorical_cols = ['currency', 'primary account', 'secondary account', 'match status']
    account_df = pd.get_dummies(account_df, columns=categorical_cols, dummy_na=False)

     # 3. Select Features
    features = [
        'company', 'au', 'gl balance', 'ihub balance', 'balance difference',
        'year', 'month', 'day'
    ]  # Include  features
    X = account_df[features]

    # 4. Scale Numerical Features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 5. Train Isolation Forest Model
    model = IsolationForest(contamination='auto', random_state=0)
    model.fit(X_scaled)

    return model, scaler

def predict_anomalies_unsupervised(df, model, scaler, account):
    """
    Predicts anomalies using the trained Isolation Forest model for a specific account.

    Args:
        df (pd.DataFrame): The input DataFrame.
        model: Trained Isolation Forest model.
        scaler:  Fitted StandardScaler
        account (int): The account number to predict anomalies for.

    Returns:
        pd.DataFrame: The DataFrame with the 'anomaly' column added.
    """

    account_df = df[df['account'] == account].copy()

    if len(account_df) == 0:
        return account_df # Return if no data

    # 1. Feature Engineering
    account_df['asofdt'] = pd.to_datetime(account_df['asofdt'])
    account_df['year'] = account_df['asofdt'].dt.year
    account_df['month'] = account_df['asofdt'].dt.month
    account_df['day'] = account_df['asofdt'].dt.day

    # 2. Encode Categorical Variables
    categorical_cols = ['currency', 'primary account', 'secondary account', 'match status']
    account_df = pd.get_dummies(account_df, columns=categorical_cols, dummy_na=False)

    # 3. Select Features
    features = [
       'company', 'au', 'gl balance', 'ihub balance', 'balance difference',
        'year', 'month', 'day'
    ]
    X = account_df[features]

    # 4. Scale the data
    X_scaled = scaler.transform(X)  # Use the fitted scaler

    # 5. Predict Anomalies
    anomaly_scores = model.decision_function(X_scaled)
    account_df['anomaly_score'] = anomaly_scores
    account_df['anomaly'] = np.where(model.predict(X_scaled) == -1, 'Yes', 'No')

    return account_df




def main():
    """
    Main function to generate data, train the unsupervised anomaly detection model, and predict anomalies for each account.
    """
    # Generate data
    # df = generate_balance_data('2024-01-01')
    # Use the data from the csv
    df = pd.read_csv("historical_data.csv")


    # Get unique accounts
    accounts = df['account'].unique()

    # Create a list to hold the dataframes with predictions
    account_anomalies = []

    # Iterate through each account
    for account in accounts:
        # Train the model for the current account
        model, scaler = train_unsupervised_anomaly_model(df.copy(), account)
        if model is not None:
            # Predict anomalies for the current account
            account_df = predict_anomalies_unsupervised(df.copy(), model, scaler, account)
            # Check if any anomalies were detected for the account
            if (account_df['anomaly'] == 'Yes').any():
                account_anomalies.append({'account': account, 'anomaly': 'Yes'})
            else:
                account_anomalies.append({'account': account, 'anomaly': 'No'})
        else:
            print(f"Not enough data to train model for account {account}")
            account_anomalies.append({'account': account, 'anomaly': 'No'})

    # Convert to dataframe
    final_df = pd.DataFrame(account_anomalies)

    final_df.to_csv("predictions.csv", index=False)
    # Print the first few rows of the DataFrame with predictions
    print(final_df.head())


if __name__ == "__main__":
    main()
