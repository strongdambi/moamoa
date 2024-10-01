from django.shortcuts import render


# index
def index(request):
    return render(request, 'webs/index.html')

# 키즈 로그인 페이지
def children_view(request):
    return render(request, 'webs/children.html')