from django.shortcuts import render


# index
def index(request):
    return render(request, 'webs/index.html')

# 키즈 로그인 페이지
def children_view(request):
    return render(request, 'webs/children.html')


# 부모 프로필
def profile_view(request):
    return render(request, 'webs/profile.html')

# 키즈 계정 회원 가입
def create_view(request):
    return render(request, 'webs/children_create.html')