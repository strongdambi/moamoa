document.querySelector('.kakao-login').addEventListener('click', function () {
    location.href = 'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=c39ec02ba741d3bb7d91cc57847a9566&redirect_uri=http://localhost:8000/api/v1/accounts/auth/kakao/callback/';
});

document.querySelector('.kids-login').addEventListener('click', function () {
    location.href = '/login/';
});

document.querySelector('.add-account').addEventListener('click', function () {
    location.href = '/webs/children_create/';  // children_create 페이지로 이동
});

// document.querySelector('.kids-login').addEventListener('click', function () {
//     alert(31)
//     location.href = './';
// });
