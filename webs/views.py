from django.shortcuts import render, get_object_or_404
from accounts.models import User


# index
def Index(request):
    return render(request, 'webs/index.html')

# 키즈 로그인 페이지
def Children_view(request):
    return render(request, 'webs/children.html')


# 부모 프로필
def Profile_view(request):
    return render(request, 'webs/profile.html')

# 키즈 계정 회원 가입
def Create_view(request):
    return render(request, 'webs/children_create.html')

# 키즈 프로필
def ChildrenProfile_view(request, pk):
    # 키즈 정보 가져오기
    child = get_object_or_404(User, pk=pk, parents=request.user)
    
    # 템플릿으로 child 객체 전달
    return render(request, 'webs/children_profile.html', {'child': child})