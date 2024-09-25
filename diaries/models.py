from django.db import models
from django.conf import settings

class FinanceDiary(models.Model):
    CATEGORY_CHOICES = [
        # 수입 항목
        ('ALLOWANCE', '용돈'),  # 정기적으로 받는 용돈
        ('BONUS', '추가 용돈'),  # 생일, 명절, 기타에 받은 돈
        ('CHORES_EARNINGS', '용돈 벌이'),  # 심부름 등 집안일을 돕고 받은 보상금
        ('PRIZES', '상금/포상금'),  # 학교나 대회에서 받은 포상금
        
        # 지출 항목
        ('SNACK', '간식비'),  # 간식, 음료, 아이스크림 등
        ('TOYS', '게임/장난감비'),  # 장난감, 게임 등
        ('BOOKS', '책/학용품비'),  # 책, 필기구 등 학용품 등
        ('TRANSPORT', '교통비'),  # 버스, 지하철 등
        ('EXTRACURRICULAR', '학원비'),  # 방과후 수업 활동 등
        ('ENTERTAINMENT', '문화/오락비'),  # 영화, 콘서트, 놀이공원 등
        ('GIFT', '선물비'),  # 부모님, 친구 선물 비용 등
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="diaries")  # 작성한 사용자
    title = models.CharField(max_length=200)  # 용돈기입장 제목
    content = models.TextField()  # 용돈기입장 내용
    income = models.IntegerField()  # 수입 금액
    expenditure = models.IntegerField()  # 지출 금액
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # 수입/지출 항목
    today = models.DateField()  # 작성된 날짜
    created_at = models.DateTimeField(auto_now_add=True)  # 생성된 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정된 시간
