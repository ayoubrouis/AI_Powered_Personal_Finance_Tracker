import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import * as api from '../services/api';

const DashboardScreen = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [monthlyData, setMonthlyData] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [spendingAnalysis, setSpendingAnalysis] = useState(null);

  const loadDashboardData = async () => {
    try {
      const [monthlyResponse, predictionsResponse, analysisResponse] = await Promise.all([
        api.getTransactions({ period: 'monthly' }),
        api.getExpensePredictions(),
        api.getSpendingAnalysis(),
      ]);

      setMonthlyData(monthlyResponse);
      setPredictions(predictionsResponse);
      setSpendingAnalysis(analysisResponse);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#3498db" />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Monthly Overview */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Monthly Overview</Text>
        {monthlyData && (
          <View style={styles.overviewContainer}>
            <View style={styles.overviewItem}>
              <Text style={styles.overviewLabel}>Income</Text>
              <Text style={styles.overviewAmount}>
                ${monthlyData.total_income.toFixed(2)}
              </Text>
            </View>
            <View style={styles.overviewItem}>
              <Text style={styles.overviewLabel}>Expenses</Text>
              <Text style={styles.overviewAmount}>
                ${monthlyData.total_expenses.toFixed(2)}
              </Text>
            </View>
          </View>
        )}
      </View>

      {/* Spending Trends */}
      {predictions && predictions.predictions && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Predicted Expenses</Text>
          <LineChart
            data={{
              labels: predictions.predictions
                .slice(0, 6)
                .map(p => p.date.split('-')[2]),
              datasets: [{
                data: predictions.predictions
                  .slice(0, 6)
                  .map(p => p.predicted_amount)
              }]
            }}
            width={350}
            height={200}
            chartConfig={{
              backgroundColor: '#ffffff',
              backgroundGradientFrom: '#ffffff',
              backgroundGradientTo: '#ffffff',
              decimalPlaces: 0,
              color: (opacity = 1) => `rgba(52, 152, 219, ${opacity})`,
            }}
            bezier
            style={styles.chart}
          />
          <Text style={styles.accuracy}>
            Model Accuracy: {predictions.model_accuracy}%
          </Text>
        </View>
      )}

      {/* Spending Analysis */}
      {spendingAnalysis && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Spending Insights</Text>
          <View style={styles.insightContainer}>
            <Text style={styles.insight}>
              Highest spending day: {spendingAnalysis.daily_patterns.highest_spending_day}
            </Text>
            <Text style={styles.insight}>
              Average monthly expenses: ${spendingAnalysis.monthly_patterns.average_monthly_expenses}
            </Text>
          </View>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  section: {
    backgroundColor: 'white',
    margin: 10,
    padding: 15,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#2c3e50',
  },
  overviewContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  overviewItem: {
    flex: 1,
    alignItems: 'center',
  },
  overviewLabel: {
    fontSize: 16,
    color: '#7f8c8d',
    marginBottom: 5,
  },
  overviewAmount: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  accuracy: {
    textAlign: 'center',
    color: '#7f8c8d',
    marginTop: 5,
  },
  insightContainer: {
    marginTop: 10,
  },
  insight: {
    fontSize: 16,
    color: '#2c3e50',
    marginBottom: 10,
  },
});

export default DashboardScreen;