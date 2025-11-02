from django.contrib import admin
from .models import Category, Transaction, Budget, SavingsGoal, FinancialMetric

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('name', 'description')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'category', 'user', 'date')
    list_filter = ('transaction_type', 'user', 'category', 'date')
    search_fields = ('description',)
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'user', 'amount', 'start_date', 'end_date')
    list_filter = ('user', 'category', 'start_date', 'end_date')
    search_fields = ('category__name',)
    date_hierarchy = 'start_date'

@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'target_amount', 'current_amount', 'target_date')
    list_filter = ('user', 'target_date')
    search_fields = ('name',)
    date_hierarchy = 'target_date'

@admin.register(FinancialMetric)
class FinancialMetricAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total_income', 'total_expenses', 'savings_rate')
    list_filter = ('user', 'date')
    date_hierarchy = 'date'
