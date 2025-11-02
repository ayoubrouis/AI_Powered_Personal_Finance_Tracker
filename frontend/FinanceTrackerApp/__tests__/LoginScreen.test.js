import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import LoginScreen from '../src/screens/LoginScreen';
import { AuthProvider } from '../src/context/AuthContext';

jest.mock('@react-native-async-storage/async-storage', () => ({
  setItem: jest.fn(),
  getItem: jest.fn(),
  removeItem: jest.fn()
}));

describe('LoginScreen', () => {
  const mockNavigation = {
    navigate: jest.fn()
  };

  it('renders correctly', () => {
    const { getByPlaceholderText, getByText } = render(
      <AuthProvider>
        <LoginScreen navigation={mockNavigation} />
      </AuthProvider>
    );

    expect(getByPlaceholderText('Username')).toBeTruthy();
    expect(getByPlaceholderText('Password')).toBeTruthy();
    expect(getByText('Login')).toBeTruthy();
    expect(getByText('Don\'t have an account? Register')).toBeTruthy();
  });

  it('shows error when fields are empty', async () => {
    const { getByText } = render(
      <AuthProvider>
        <LoginScreen navigation={mockNavigation} />
      </AuthProvider>
    );

    fireEvent.press(getByText('Login'));

    await waitFor(() => {
      expect(getByText('Please fill in all fields')).toBeTruthy();
    });
  });

  it('navigates to register screen', () => {
    const { getByText } = render(
      <AuthProvider>
        <LoginScreen navigation={mockNavigation} />
      </AuthProvider>
    );

    fireEvent.press(getByText('Don\'t have an account? Register'));
    expect(mockNavigation.navigate).toHaveBeenCalledWith('Register');
  });
});