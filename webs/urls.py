from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 홈
    path('children/', views.children_view, name='children'), # 키즈 로그인 페이지
    path('profile/', views.profile_view, name='profile'), # 부모 프로필
]