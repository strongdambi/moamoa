# from django.db import models

class Plan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.PositiveIntegerField()
    food_expense = models.PositiveIntegerField()
    transportation_expense = models.PositiveIntegerField()
    savings = models.PositiveIntegerField()
    snack_expense = models.PositiveIntegerField()
    plan_details = models.TextField()
