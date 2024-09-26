from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("", views.AccountsView.as_view()), #학부모 조회
    path('auth/kakao/callback/', views.KakaoCallbackView.as_view()), #카카오톡 부모 회원가입
    path("login/", views.LoginView.as_view()),  # 아이들 로그인
    path("logout/", views.LogoutView.as_view()),  # 아이들 로그아웃
    path("token/refresh/", TokenRefreshView.as_view()), # refresh_token 발행
    path('children/create/', views.ChildrenPRCreate.as_view()), # 아이들 회원가입
    path('children/<int:pk>/', views.ChildrenPRView.as_view()), # 아이들 조회, 수정, 삭제

]

