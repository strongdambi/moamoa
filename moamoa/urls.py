from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # 기본 경로 설정: '/'로 접근 시 'webs' 앱의 index 페이지로 리다이렉트
    path('', lambda request: redirect('index')),  # 기본 URL을 webs 앱의 index로 리다이렉트


    # 프론트엔드 페이지
    path('webs/', include("webs.urls")), # 프론트엔드

    # API 엔드포인트
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include("accounts.urls")), # 회원
    path('api/v1/diary/', include("diaries.urls")),  # 용돈기입장
]
