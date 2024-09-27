from django.db import models
from django.conf import settings

class Plan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.PositiveIntegerField()
    food_expense = models.PositiveIntegerField()
    transportation_expense = models.PositiveIntegerField()
    savings = models.PositiveIntegerField()
    snack_expense = models.PositiveIntegerField()
    plan_details = models.TextField()
    allowance_plan = models.TextField()
    user = models.ForeignKey(to = settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="plans")
