from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from django.utils import timezone
from ..models import Category, Transaction, Budget, SavingsGoal
from datetime import timedelta
import json

class APITestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description',
            user=self.user
        )

    def test_category_list_create(self):
        """Test category listing and creation"""
        # Test listing
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Test creation
        new_category_data = {
            'name': 'New Category',
            'description': 'New Description'
        }
        response = self.client.post('/api/categories/', new_category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_transaction_operations(self):
        """Test transaction CRUD operations"""
        # Create transaction
        transaction_data = {
            'category': self.category.id,
            'amount': '100.50',
            'transaction_type': 'EXPENSE',
            'description': 'Test Transaction',
            'date': timezone.now().date().isoformat()
        }
        
        response = self.client.post('/api/transactions/', transaction_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction_id = response.data['id']
        
        # Read transaction
        response = self.client.get(f'/api/transactions/{transaction_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['amount']), Decimal('100.50'))
        
        # Update transaction
        update_data = {
            'amount': '150.75'
        }
        response = self.client.patch(
            f'/api/transactions/{transaction_id}/',
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['amount']), Decimal('150.75'))
        
        # Delete transaction
        response = self.client.delete(f'/api/transactions/{transaction_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_budget_operations(self):
        """Test budget creation and retrieval"""
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        
        budget_data = {
            'category': self.category.id,
            'amount': '1000.00',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        
        response = self.client.post('/api/budgets/', budget_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test budget list
        response = self.client.get('/api/budgets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_savings_goal_operations(self):
        """Test savings goal creation and updates"""
        target_date = timezone.now().date() + timedelta(days=365)
        
        goal_data = {
            'name': 'Test Goal',
            'target_amount': '5000.00',
            'current_amount': '1000.00',
            'target_date': target_date.isoformat()
        }
        
        response = self.client.post('/api/savings-goals/', goal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        goal_id = response.data['id']
        
        # Update progress
        update_data = {
            'current_amount': '2000.00'
        }
        response = self.client.patch(
            f'/api/savings-goals/{goal_id}/',
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['current_amount']), Decimal('2000.00'))

    def test_unauthorized_access(self):
        """Test API access without authentication"""
        # Create new client without authentication
        client = APIClient()
        
        # Try to access protected endpoints
        endpoints = [
            '/api/categories/',
            '/api/transactions/',
            '/api/budgets/',
            '/api/savings-goals/'
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED
            )