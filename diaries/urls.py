from django.urls import path
from . import views

urlpatterns = [
    # 월말 결산
    path('monthly/', views.PreviousMonthPlansView.as_view()),
    # 아이들만 사용할수 있는 챗봇
    path('chat/', views.ChatbotProcessView.as_view()),
    # 기입장 특정 삭제
    path('chat/<int:pk>/delete/', views.ChatbotProcessDelete.as_view()),
]