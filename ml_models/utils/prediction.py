import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

def prepare_transaction_data(transactions):
    """Convert transaction queryset to DataFrame and prepare features."""
    df = pd.DataFrame(list(transactions.values()))
    if df.empty:
        return None
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Create time-based features
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_month'] = df['date'].dt.day
    
    # Create category dummies
    category_dummies = pd.get_dummies(df['category_id'], prefix='category')
    df = pd.concat([df, category_dummies], axis=1)
    
    return df

def predict_future_expenses(transactions, days_ahead=30):
    """Predict future expenses based on historical data."""
    df = prepare_transaction_data(transactions)
    if df is None or len(df) < 30:  # Need enough data for meaningful predictions
        return {
            'error': 'Not enough historical data for predictions',
            'required_data_points': 30,
            'current_data_points': len(df) if df is not None else 0
        }
    
    # Filter for expenses only
    expense_df = df[df['transaction_type'] == 'EXPENSE']
    
    # Prepare features and target
    features = ['month', 'day_of_week', 'day_of_month'] + \
              [col for col in expense_df.columns if col.startswith('category_')]
    X = expense_df[features]
    y = expense_df['amount']
    
    # Split data and train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Generate future dates and their features
    future_dates = [datetime.now().date() + timedelta(days=i) for i in range(1, days_ahead + 1)]
    future_features = []
    
    for date in future_dates:
        features_dict = {
            'month': date.month,
            'day_of_week': date.weekday(),
            'day_of_month': date.day
        }
        # Add category columns with zeros
        for col in X.columns:
            if col.startswith('category_'):
                features_dict[col] = 0
        future_features.append(features_dict)
    
    future_df = pd.DataFrame(future_features)
    predictions = model.predict(future_df)
    
    # Prepare response
    response = {
        'predictions': [
            {
                'date': date.strftime('%Y-%m-%d'),
                'predicted_amount': round(float(amount), 2)
            }
            for date, amount in zip(future_dates, predictions)
        ],
        'model_accuracy': round(model.score(X_test, y_test) * 100, 2)
    }
    
    return response

def analyze_spending_patterns(transactions):
    """Analyze spending patterns and provide insights."""
    df = prepare_transaction_data(transactions)
    if df is None:
        return {'error': 'No transaction data available'}
    
    # Filter for expenses
    expense_df = df[df['transaction_type'] == 'EXPENSE']
    
    # Monthly spending analysis
    monthly_spending = expense_df.groupby(['month'])['amount'].agg(['sum', 'mean', 'count'])
    highest_spending_month = monthly_spending['sum'].idxmax()
    lowest_spending_month = monthly_spending['sum'].idxmin()
    
    # Day of week analysis
    dow_spending = expense_df.groupby('day_of_week')['amount'].mean()
    highest_spending_day = dow_spending.idxmax()
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Category analysis
    category_spending = expense_df.groupby('category_id')['amount'].sum()
    top_categories = category_spending.nlargest(3)
    
    # Unusual expenses detection
    mean_expense = expense_df['amount'].mean()
    std_expense = expense_df['amount'].std()
    unusual_threshold = mean_expense + (2 * std_expense)
    unusual_expenses = expense_df[expense_df['amount'] > unusual_threshold]
    
    analysis = {
        'monthly_patterns': {
            'highest_spending_month': highest_spending_month,
            'lowest_spending_month': lowest_spending_month,
            'average_monthly_expenses': round(monthly_spending['mean'].mean(), 2)
        },
        'daily_patterns': {
            'highest_spending_day': day_names[highest_spending_day],
            'spending_by_day': {
                day_names[i]: round(float(amt), 2)
                for i, amt in dow_spending.items()
            }
        },
        'category_insights': {
            'top_spending_categories': [
                {'category_id': int(cat_id), 'total_amount': round(float(amount), 2)}
                for cat_id, amount in top_categories.items()
            ]
        },
        'unusual_expenses': {
            'threshold': round(float(unusual_threshold), 2),
            'count': len(unusual_expenses),
            'examples': [
                {
                    'date': row['date'].strftime('%Y-%m-%d'),
                    'amount': round(float(row['amount']), 2),
                    'category_id': int(row['category_id'])
                }
                for _, row in unusual_expenses.head(5).iterrows()
            ]
        }
    }
    
    return analysis