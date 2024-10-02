from django.shortcuts import render


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

def ChildrenProfile_view(request):
    return render(request, 'webs/children_create.html')