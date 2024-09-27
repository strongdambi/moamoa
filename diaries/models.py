from django.db import models
from django.conf import settings


class FinanceDiary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="diaries")  # 작성한 사용자
    content = models.TextField()  # 용돈기입장 내용
    imcome = models.PositiveIntegerField()  # 수입
    spending = models.PositiveIntegerField()  # 지출
    category = models.CharField(max_length=100)  # 카테고리 (AI가 추론한 값을 저장)
    today = models.DateField()  # 사용자 지정 날짜/시간
    created_at = models.DateTimeField(auto_now_add=True)  # 생성된 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정된 시간


class Summary(models.Model):
    parents = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="summary")
    weekly = models.TextField()  # 아이
    monthly = models.TextField()  # 부모님


class Plan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.PositiveIntegerField()
    food_expense = models.PositiveIntegerField()
    transportation_expense = models.PositiveIntegerField()
    savings = models.PositiveIntegerField()
    snack_expense = models.PositiveIntegerField()
    plan_details = models.TextField()  # 간략
    allowance_plan = models.TextField()  # 상세
    user = models.ForeignKey(to = settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="plans")


'''
프롬프트로 용돈계획서 시나리오
시나리오를 바탕으로 일관된 결과가 나오는지 체크
일관된 결과를 우리 입맛에 맞출 수 있는지 체크
결과를 가지고 모델 작성

효율적인 방법
한도 - 부모님 정함
정해진 한도 내에서 계획을 작성하는데
AI가 도와줌
'''
