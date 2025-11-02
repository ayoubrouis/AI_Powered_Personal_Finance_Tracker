from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Category, Transaction, Budget, SavingsGoal
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Initialize sample data for testing'

    def handle(self, *args, **kwargs):
        # Create test user
        user, created = User.objects.get_or_create(
            username='testuser',
            email='test@example.com'
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user'))

        # Create categories
        categories = [
            'Groceries',
            'Rent',
            'Utilities',
            'Transportation',
            'Entertainment',
            'Healthcare',
            'Shopping',
            'Dining Out',
            'Savings',
            'Investment'
        ]

        created_categories = []
        for cat_name in categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                user=user,
                defaults={'description': f'Expenses related to {cat_name.lower()}'}
            )
            created_categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))

        # Create transactions
        start_date = timezone.now() - timedelta(days=90)
        for i in range(100):
            date = start_date + timedelta(days=random.randint(0, 90))
            category = random.choice(created_categories)
            transaction_type = random.choice(['INCOME', 'EXPENSE'])
            amount = Decimal(str(round(random.uniform(10, 1000), 2)))

            Transaction.objects.create(
                user=user,
                category=category,
                amount=amount,
                transaction_type=transaction_type,
                description=f'Sample {transaction_type.lower()} for {category.name}',
                date=date
            )

        self.stdout.write(self.style.SUCCESS('Created sample transactions'))

        # Create budgets
        for category in created_categories:
            if category.name not in ['Savings', 'Investment']:
                Budget.objects.create(
                    user=user,
                    category=category,
                    amount=Decimal(str(round(random.uniform(500, 2000), 2))),
                    start_date=timezone.now().date().replace(day=1),
                    end_date=(timezone.now().date().replace(day=1) + timedelta(days=30))
                )

        self.stdout.write(self.style.SUCCESS('Created sample budgets'))

        # Create savings goals
        goals = [
            'Emergency Fund',
            'New Car',
            'Vacation',
            'Down Payment'
        ]

        for goal_name in goals:
            target_amount = Decimal(str(round(random.uniform(5000, 20000), 2)))
            current_amount = Decimal(str(round(random.uniform(0, float(target_amount)), 2)))
            
            SavingsGoal.objects.create(
                user=user,
                name=goal_name,
                target_amount=target_amount,
                current_amount=current_amount,
                target_date=timezone.now().date() + timedelta(days=random.randint(180, 365))
            )

        self.stdout.write(self.style.SUCCESS('Created sample savings goals'))
        self.stdout.write(self.style.SUCCESS('Sample data initialization completed'))