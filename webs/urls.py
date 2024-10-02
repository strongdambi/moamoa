from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'), # 홈
    path('children/', views.Children_view, name='children'), # 키즈 로그인 페이지
    path('profile/', views.Profile_view, name='profile'), # 부모 프로필
    path('create/', views.Create_view, name='create'), # 키즈 계정 회원가입
    path('children/<int:pk>/', views.ChildrenProfile_view, name='children_profile') # 키즈 프로필
]