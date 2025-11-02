import React from 'react';
import { render, waitFor } from '@testing-library/react-native';
import DashboardScreen from '../src/screens/DashboardScreen';
import * as api from '../src/services/api';

jest.mock('../src/services/api');

describe('DashboardScreen', () => {
  beforeEach(() => {
    api.getTransactions.mockResolvedValue({
      total_income: 5000,
      total_expenses: 3000
    });

    api.getExpensePredictions.mockResolvedValue({
      predictions: [
        { date: '2025-11-01', predicted_amount: 100 },
        { date: '2025-11-02', predicted_amount: 150 }
      ],
      model_accuracy: 85
    });

    api.getSpendingAnalysis.mockResolvedValue({
      daily_patterns: {
        highest_spending_day: 'Friday'
      },
      monthly_patterns: {
        average_monthly_expenses: 3000
      }
    });
  });

  it('renders loading state initially', () => {
    const { getByTestId } = render(<DashboardScreen />);
    expect(getByTestId('loading-indicator')).toBeTruthy();
  });

  it('renders dashboard data after loading', async () => {
    const { getByText } = render(<DashboardScreen />);

    await waitFor(() => {
      expect(getByText('Monthly Overview')).toBeTruthy();
      expect(getByText('$5000.00')).toBeTruthy();
      expect(getByText('$3000.00')).toBeTruthy();
    });
  });

  it('shows prediction data', async () => {
    const { getByText } = render(<DashboardScreen />);

    await waitFor(() => {
      expect(getByText('Predicted Expenses')).toBeTruthy();
      expect(getByText('Model Accuracy: 85%')).toBeTruthy();
    });
  });

  it('shows spending insights', async () => {
    const { getByText } = render(<DashboardScreen />);

    await waitFor(() => {
      expect(getByText('Spending Insights')).toBeTruthy();
      expect(getByText('Highest spending day: Friday')).toBeTruthy();
      expect(getByText('Average monthly expenses: $3000')).toBeTruthy();
    });
  });
});