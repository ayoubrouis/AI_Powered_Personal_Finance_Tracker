from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, TransactionViewSet, BudgetViewSet,
    SavingsGoalViewSet, FinancialMetricViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'savings-goals', SavingsGoalViewSet, basename='savings-goal')
router.register(r'financial-metrics', FinancialMetricViewSet, basename='financial-metric')

urlpatterns = [
    path('', include(router.urls)),
]