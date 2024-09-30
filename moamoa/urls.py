from django.contrib import admin
from django.urls import path, include
from webs import views

urlpatterns = [
    # 프론트엔드 페이지
    path('', views.index, name='index'), #홈

    # API 엔드포인트
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include("accounts.urls")), # 회원
    path('api/v1/diary/', include("diaries.urls")),  # 용돈기입장
]
