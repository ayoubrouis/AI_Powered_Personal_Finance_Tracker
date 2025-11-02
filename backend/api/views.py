from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from django.utils import timezone
from .models import Category, Transaction, Budget, SavingsGoal, FinancialMetric
from .serializers import (
    CategorySerializer, TransactionSerializer, BudgetSerializer,
    SavingsGoalSerializer, FinancialMetricSerializer, UserSerializer
)
from datetime import datetime, timedelta
from decimal import Decimal

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        month = request.query_params.get('month', timezone.now().month)
        year = request.query_params.get('year', timezone.now().year)

        transactions = self.get_queryset().filter(
            date__month=month,
            date__year=year
        )

        summary = {
            'total_income': transactions.filter(
                transaction_type='INCOME'
            ).aggregate(total=Sum('amount'))['total'] or 0,
            'total_expenses': transactions.filter(
                transaction_type='EXPENSE'
            ).aggregate(total=Sum('amount'))['total'] or 0,
            'by_category': []
        }

        for category in Category.objects.filter(user=request.user):
            category_expenses = transactions.filter(
                category=category,
                transaction_type='EXPENSE'
            ).aggregate(total=Sum('amount'))['total'] or 0
            if category_expenses > 0:
                summary['by_category'].append({
                    'category': category.name,
                    'amount': category_expenses
                })

        return Response(summary)

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category__name']
    ordering_fields = ['start_date', 'end_date', 'amount']

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_expenses_for_budget(self, budget):
        return Transaction.objects.filter(
            user=self.request.user,
            category=budget.category,
            transaction_type='EXPENSE',
            date__gte=budget.start_date,
            date__lte=budget.end_date
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        spent = self.get_expenses_for_budget(instance)
        data = self.get_serializer(instance).data
        data['spent_amount'] = spent
        data['remaining_amount'] = instance.amount - spent
        return Response(data)

class SavingsGoalViewSet(viewsets.ModelViewSet):
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['target_date', 'target_amount']

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        if instance.target_amount > 0:
            progress = (instance.current_amount / instance.target_amount) * 100
            data['progress_percentage'] = round(progress, 2)
        return Response(data)

class FinancialMetricViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialMetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date']

    def get_queryset(self):
        return FinancialMetric.objects.filter(user=self.request.user)
