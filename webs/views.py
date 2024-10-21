from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user
from accounts.models import User


#10.24 삭제 시작
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, login

from . import config
@api_view(['GET'])
def TestLogin(request, pk):

    allowed_users = config.ALLOWED_USERS

    # 사용자가 허용된 사용자 목록에 있는지 확인
    if pk not in allowed_users:
        return Response({'detail': '허용되지 않은 사용자입니다.'}, status=status.HTTP_403_FORBIDDEN)

    # 사용자 ID로 해당 유저를 조회합니다.
    User = get_user_model()
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'detail': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 사용자를 로그인 시킵니다.
    login(request, user)

    # JWT 토큰을 발급합니다.
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # 프론트엔드로 리다이렉트할 URL (프로필 페이지로 리다이렉트)
    frontend_url = settings.FRONTEND_URL + '/profile/'  # 설정된 프론트엔드 도메인 사용

    # 리다이렉트 시, JWT 토큰을 쿠키에 설정 (HTTP-Only 쿠키로 저장)
    response = redirect(frontend_url)

    # 쿠키에 JWT 토큰 설정 (HTTPOnly=True로 보안을 강화)
    response.set_cookie('access_token', access_token, httponly=True, samesite='Lax', secure=False)
    response.set_cookie('refresh_token', refresh_token, httponly=True, samesite='Lax', secure=True)

    return response

#10.24 삭제 끝

# index
def Index(request):
    return render(request, 'webs/index.html')

# 키즈 로그인 페이지
def Children_view(request):
    return render(request, 'webs/children.html')


# 부모 프로필
def Profile_view(request):
    return render(request, 'webs/profile.html')

def Create_view(request):
    # GET 요청일 때만 로그인 여부를 확인합니다.
    if request.method == 'GET':
        # 사용자가 로그인하지 않은 경우
        if not request.user.is_authenticated:
            # 로그인 페이지로 리다이렉트
            return redirect('/')
    
    # 로그인된 사용자는 페이지를 볼 수 있습니다.
    return render(request, 'webs/children_create.html')

# 키즈 프로필
def ChildrenProfile_view(request, child_pk):
    # 키즈 정보 가져오기
    child = get_object_or_404(User, pk=child_pk)
    # 템플릿으로 child 객체 전달
    return render(request, 'webs/children_profile.html', {
        'child': child,
        })

# AI 채팅
def Chatbot_view(request, child_pk):
    user = get_object_or_404(User, pk=child_pk)
    user_image = request.build_absolute_uri(
                        user.images.url)
    
    context = {
        'user': user,
        'user_image': user_image,
        'child_pk': child_pk,
    }
    return render(request, 'webs/chatbot.html', context)

# 부모 프로필
def ProfileDetail_view(request, pk):
    return render(request, 'webs/profile_detail.html')

# Access-error 페이지
def access_error_view(request):
    # 현재 세션에 로그인된 사용자를 가져옴
    logged_in_user = get_user(request)
    return render(request, 'webs/access_error.html', {'logged_in_user': logged_in_user})  # 에러 페이지 렌더링

