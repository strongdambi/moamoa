from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include("accounts.urls")),  # 회원
    path('api/v1/diary/', include("diaries.urls")),  # 용돈기입장
]
