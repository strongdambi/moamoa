var kakaoLoginButton = document.querySelector('.kakao-login');
if (kakaoLoginButton) {
    kakaoLoginButton.addEventListener('click', function () {
        location.href = 'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=c39ec02ba741d3bb7d91cc57847a9566&redirect_uri=http://localhost:8000/api/v1/accounts/auth/kakao/callback/';
    });
}

var kidsLoginButton = document.querySelector('.kids-login');
if (kidsLoginButton) {
    kidsLoginButton.addEventListener('click', function () {
        location.href = '/webs/children/';
    });
}

var addAccountButton = document.querySelector('.add-account');
if (addAccountButton) {
    addAccountButton.addEventListener('click', function () {
        location.href = '/webs/create/';
    });
}

// document.querySelector('.kids-login').addEventListener('click', function () {
//     alert(31)
//     location.href = './';
// });