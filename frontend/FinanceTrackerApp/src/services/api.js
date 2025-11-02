import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const login = async (username, password) => {
  try {
    const response = await api.post('/auth/login/', { username, password });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const register = async (userData) => {
  try {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getTransactions = async (params) => {
  try {
    const response = await api.get('/transactions/', { params });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const addTransaction = async (transactionData) => {
  try {
    const response = await api.post('/transactions/', transactionData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getCategories = async () => {
  try {
    const response = await api.get('/categories/');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getBudgets = async () => {
  try {
    const response = await api.get('/budgets/');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const updateBudget = async (budgetId, budgetData) => {
  try {
    const response = await api.patch(`/budgets/${budgetId}/`, budgetData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getSavingsGoals = async () => {
  try {
    const response = await api.get('/savings-goals/');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const updateSavingsGoal = async (goalId, goalData) => {
  try {
    const response = await api.patch(`/savings-goals/${goalId}/`, goalData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getExpensePredictions = async () => {
  try {
    const response = await api.get('/financial-metrics/predictions/');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getSpendingAnalysis = async () => {
  try {
    const response = await api.get('/financial-metrics/spending-analysis/');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export default api;