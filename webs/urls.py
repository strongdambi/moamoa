from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'), # 홈
    path('login/', views.Children_view, name='children'), # 키즈 로그인 페이지
    path('profile/', views.Profile_view, name='profile'), # 부모 프로필
    path('profile/<int:pk>/', views.ProfileDetail_view, name='profile_detail'), # 부모 프로필 상세조회
    path('signin/', views.Create_view, name='signin'), # 키즈 계정 회원가입
    path('child_profile/<int:child_pk>/', views.ChildrenProfile_view, name='child_profile'),  # 키즈 프로필
    path('chatbot/<int:child_pk>/', views.Chatbot_view, name='chatbot'), # 용돈기입장 챗봇
]