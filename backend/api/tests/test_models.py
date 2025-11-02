from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Category, Transaction, Budget, SavingsGoal, FinancialMetric
from django.utils import timezone
from datetime import timedelta

class ModelTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description',
            user=self.user
        )

    def test_category_creation(self):
        """Test category creation and string representation"""
        self.assertEqual(str(self.category), 'Test Category')
        self.assertEqual(self.category.user, self.user)
        self.assertEqual(self.category.description, 'Test Description')

    def test_transaction_creation(self):
        """Test transaction creation and validation"""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('100.50'),
            transaction_type='EXPENSE',
            description='Test Transaction',
            date=timezone.now().date()
        )
        
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.amount, Decimal('100.50'))
        self.assertEqual(transaction.transaction_type, 'EXPENSE')

    def test_budget_creation(self):
        """Test budget creation and validation"""
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('1000.00'),
            start_date=start_date,
            end_date=end_date
        )
        
        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.category, self.category)
        self.assertEqual(budget.amount, Decimal('1000.00'))
        self.assertEqual(budget.start_date, start_date)
        self.assertEqual(budget.end_date, end_date)

    def test_savings_goal_creation(self):
        """Test savings goal creation and validation"""
        target_date = timezone.now().date() + timedelta(days=365)
        
        goal = SavingsGoal.objects.create(
            user=self.user,
            name='Test Goal',
            target_amount=Decimal('5000.00'),
            current_amount=Decimal('1000.00'),
            target_date=target_date
        )
        
        self.assertEqual(goal.user, self.user)
        self.assertEqual(goal.name, 'Test Goal')
        self.assertEqual(goal.target_amount, Decimal('5000.00'))
        self.assertEqual(goal.current_amount, Decimal('1000.00'))
        self.assertEqual(goal.target_date, target_date)

    def test_financial_metric_creation(self):
        """Test financial metric creation and validation"""
        metric = FinancialMetric.objects.create(
            user=self.user,
            date=timezone.now().date(),
            total_income=Decimal('5000.00'),
            total_expenses=Decimal('3000.00'),
            savings_rate=Decimal('40.00')
        )
        
        self.assertEqual(metric.user, self.user)
        self.assertEqual(metric.total_income, Decimal('5000.00'))
        self.assertEqual(metric.total_expenses, Decimal('3000.00'))
        self.assertEqual(metric.savings_rate, Decimal('40.00'))