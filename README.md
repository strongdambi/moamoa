# 🎁 모아모아 (아이들을 위한 용돈기입장)
- **모아모아 홈페이지 : https://moamoa.kids**
- **API 명세서 홈페이지 : https://documenter.getpostman.com/view/37988705/2sAXxTapsS**
- 모아모아는 아이(5세~13세)들에게 금융에대한 이해와 교육을 알려주기 위해 만든 서비스이며, AI와의 채팅을통해 용돈기입장 작성을 도와주고 월간 용돈기입장의 데이터를 통해서 부모님들에게 아이의 소비 습관을 보여주고 그 소비습관에 맞는 방향성을 제시해주는 서비스입니다. 

---
## 🧩 버전 업데이트
- **1.0.3 Version (2024-10-22)**
  - AI와의 채팅에서 기존 단일 내역만 저장할 수 있던 방식에서 용돈 지출내역 또는 수입내역을 다중으로 입력하여 저장할수 있게 수정하였습니다.
  - 자녀의 프로필 수정에서 비밀번호에 유효성 검사(비밀번호 길이, 문자+숫자 혼합, 똑같은 연속된 문자 4개이상 금지) 체크를 추가로 넣어주었습니다.
  - 자녀의 프로필 수정에서 자녀의 프로필 사진 버튼 CSS를 수정하고, 선택한 프로필 사진의 파일명이 나타나게 수정하였습니다.
---
- **1.0.2 Version (2024-10-17)**
  - 다른 사람의 채팅 내역과 용돈 기입장 페이지를 접근하지 못하도록 수정 하였습니다.
  - 하나의 문자로 이루어진 비밀번호 설정을 하지 못하도록 수정하였습니다.
  - AI와의 채팅에서 AI가 "용돈 기입장 작성을 저장할까요?"라고 묻는 질문에 대한 답장하는 방식을 전보다 폭넓은 긍정문과 부정문으로 입력하여 AI가 이해할수 있도록 수정하였습니다.
  - AI와의 채팅으로 용돈기입장을 작성할 때 최대 금액 제한을 두었습니다.
  - AI와의 채팅에서 유저의 채팅이 말풍선에 먼저 생성되게 수정하였습니다.
  - 부모 프로필에 진입했을때 부모의 프로필 사진이 길어지게 나오는 현상을 수정하였습니다.
  - 인덱스 페이지에 가이드라인을 알려주는 아이콘을 추가하였습니다.
  - 자녀 프로필 상에서 AI채팅으로 진입하는 아이콘을 수정하였습니다.
---
- **1.0.1 Version (2024-10-16)**
  - AI와의 채팅에서 AI가 "용돈 기입장 작성을 저장할까요"라고 묻는 질문에대한 답장하는 방식을 기존에 오로지 '1'과 '2'로만 입력하게 했던 부분을 '1', '2','네', '아니오','맞아요','틀려요','예', '아니요', '응', '아니'로 넓혔습니다.
  - AI와의 채팅에서 저장하는 부분에 '1'을 여러번 입력할시 중복으로 저장되는 문제를 해결하였습니다.
  - AI와의 채팅 페이지에서 용돈기입장 저장 이후 뒤로가기 버튼을 눌렀을시 자녀의 프로필 페이지에서 자동 업데이트 되게 수정하였습니다.
  - 배너에 로그아웃 버튼이 로그인 페이지에도 존재하여 버튼을 사라지게 수정하였습니다.
  - 페이지 뒤로가기 버튼을 배너에 추가하였습니다.
  - 프로필 수정에서 이름이 바뀌지 않는 버그를 수정하였습니다.
  - 부모 상세페이지의 자녀 월 결산 요약 부분에 AI의 로딩 지연이 있어서 로딩시간동안 progressbar을 보여주게 변경하였습니다.
  - 부모 상세페이지의 자녀 월 결산 요약의 데이터가 없으면 무한 로딩 되는 버그를 데이터가 없다는 안내로 수정하였습니다.
  - 부모 프로필 페이지에서 자녀 프로필의 사진이 구겨지는 현상을 수정하였습니다.
  - 부모 프로필 페이지에서 자녀 계정을 생성할 때 모든 유효성 검사가 '에러가 발생했습니다'라고 뜨는 alert부분을 각각의 유효성 검사로 alert 처리했습니다.
---
- **1.0.0 Version (2024-10-15)** 
   - **모아모아 1.0.0 Version 서비스 배포 시작**
   - 부모의 계정과 그 하위 계정인 자녀 계정이 서로 상호작용하여 자녀의 지출 습관과 분석을 AI를 통해 확인 할 수 있습니다.
   - 자녀는 AI와의 채팅을 통해 매우 쉽게 용돈기입장을 작성하여 용돈을 관리할 수 있습니다.


---

## 🌟 주요 기능

- **회원가입 및 로그인**: 주 계정(부모님 계정)과 하위 계정(자녀 계정)을 나누어 부모님이 메인 페이지에서 카카오 소셜 로그인을 하여 자녀의 회원가입을 진행. 만들어진 자녀 계정은 메인 홈페이지의 자녀 로그인을 통해서 자녀 페이지로 진입 가능.
- **용돈기입장 작성**: AI와의 대화를 통해 직접 AI가 용돈 기입장의 내용(사용한 날짜, 입출, 항목, 금액, 지출요약)을 정리하여 데이터베이스에 저장
- **월간 소비습관 분석**: 월말 마다 AI가 자녀의 해당 월의 용돈 기입장을 가져와서 소비습관, 사용한 소비의 카테고리 분류 그리고 개선 방향성을 부모에게 요약하여 제공

---

## 🔍 프로젝트 핵심 기술 및 버전
- Programming Language : **Python 3.10**
- Web Framework : **Django 4.2**
- API Toolkit : **DjangoRestFramework 3.15.2**
- Database : **SQLite, MariaDB**
- Version Control : **Git, Github**
- LLM : **Open AI, LangChain**

## 🛠️ 설치 방법

### 1️⃣ 저장소 클론

```bash
git clone [https://github.com/strongdambi/moamoa.git
```

### 2️⃣ 가상 환경 설정 및 패키지 설치

```bash
python -m venv venv
source venv/bin/activate  # Mac
source venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3️⃣ 데이터베이스 마이그레이션

```bash
python manage.py migrate
python manage.py makemigrations
```

### 4️⃣ 슈퍼유저 생성 (관리자 계정)

```bash
python manage.py createsuperuser
```

### 5️⃣ 개발 서버 실행

```bash
python manage.py runserver
```

---

## 🖇️ 와이어 프레임

![image (1)](https://github.com/user-attachments/assets/855a476c-5724-4f73-b3c6-aa6841316a16)

---

## 📋 API 명세서

| 기능                    | HTTP 메서드 | 엔드포인트                                   | 설명                                                    |
|-------------------------|-------------|---------------------------------------------|-------------------------------------------------------------|
| **부모 회원가입**       | POST        | `/api/v1/accounts/auth/kakao/callback/`       | 인덱스의 카카오 소셜 로그인을 통해 회원가입 진행 및 토큰 발급                 |
| **자녀 회원가입**        | POST       | `/api/v1/accounts/children/create/`            | 부모프로필 페이지에서 자녀 추가를 통해 회원가입 진행                        |
| **자녀 로그인**          | POST        | `/api/v1/accounts/login/`                     | 인덱스의 키즈 로그인을 통해서 아이디 및 비밀번호 입력후 쿠키 및 JWT토큰 발급  |
| **로그아웃**             | POST        | `/api/v1/accounts/logout/`                    | refresh_token 블랙리스트 추가 및 쿠키의 JWT토큰 삭제                        |           
| **refresh_token 발행**   | POST        | `/api/v1/accounts/token/refresh/`             | refresh_token을 통해 access_token 재발급                                    |
| **AUTH 여부 확인**      | GET         | `/api/v1/accounts/check_token/`                | 유저의 AUTH를 체크                                                          |
| **부모 프로필**          | GET         | `/api/v1/accounts/`                           | 부모 프로필 및 부모의 자녀들 조회                                            |
| **자녀 정보 조회**       | GET         | `/api/v1/accounts/children/<int:pk>/`           | 자녀의 생일, 이름, 아이디 프로필이미지 조회                                |
| **자녀 정보 수정**       | PUT         | `/api/v1/accounts/children/<int:pk>/`         | 자녀의 생일, 이름, 아이디, 비밀번호, 프로필 수정                             |
| **자녀 정보 삭제**       | DELETE      | `/api/v1/accounts/children/<int:pk>/`         | 자녀의 정보 및 데이터를 삭제                                                |
| **자녀 월말 결산 작성**  | POST        | `/api/v1/diary/monthly/<int:child_id>/`     | 자녀의 월간 용돈기입장 데이터를 토대로 AI가 결산 작성                        |
| **용돈기입장 작성**      | POST        | `/api/v1/diary/chat/`                       | AI와의 대화를 통해 수집한 json데이터를 저장                                 |
| **AI챗봇 채팅 기록**     | GET         | `/api/v1/diary/chat/messages/<int:child_pk>/`  | AI와 자녀가 대화한 내용을 전달                                             |
| **기입장 특정 삭제**     | DELETE      | `/api/v1/diary/chat/<int:diary_pk>/delete/`  | 자녀의 특정 용돈기입장 내용 삭제                                           |
| **월별 용돈 기입장 조회**| GET         | `/api/v1/diary/<int:child_pk>/<int:year>/<int:month>/`| 년월을 기준으로 작성한 용돈기입장 조회                            |
| **용돈기입장 데이터가있는 월 조회**| GET | `/api/v1/diary/<int:child_pk>/available-months/`| 용돈 기입장 데이터가 있는 월 조회                                    |



---

## 🖼️ ERD (Entity Relationship Diagram)

### ERD 이미지
![moamoa_erd](https://github.com/user-attachments/assets/cb77ebea-f4d5-4078-9326-380445a616d3)


---

## 🛠️ 데이터베이스 관리

이 프로젝트는 **SQLite3**을 기본 데이터베이스로 사용합니다.
(추후**MySQL**로 전환 예정)

---

## 🌍 시스템 아키텍처

### 백엔드 구성

- **Django REST Framework**: API 설계를 위한 프레임워크.
- **KAKAO API**: 카카오 소셜 로그인을 위한 API.
- **SQLite3**: 데이터베이스 관리.
- **Redis**: AI 채팅 내역 저장 관리.
- **Langchain**: AI 서비스 사용을 위한 라이브러리.
- **OpenAI**: GPT 4o-mini
- **JWT**: 토큰 방식의 사용자 인증 시스템.

---


## 🔐 보안

- **HTTPS 사용**: 모든 API 요청은 HTTPS를 통해 암호화되어 전송됩니다.
- **JWT 인증**: 사용자는 JWT 토큰을 통해 인증되며, 권한 관리가 이루어집니다.
- **비밀번호 암호화**: 사용자의 비밀번호는 해시화되어 안전하게 저장됩니다.
- **HTTP ONLY**: JavaScript를 통한 쿠키에 접근을 방지하여 쿠키 값에 접근을 막아줍니다.

---

## :eyes: 트러블슈팅
1. **날짜 인식 문제**
   - 사용자들이 입력한 '오늘', '어제'와 같은 상대적 날짜 표현이 하루 전으로 기록되는 문제가 발생했습니다.
     이는 타임존 설정과 날짜 파싱 로직에 문제가 있었으며, 이를 수정하여 현재는 정상적으로 작동합니다.
2. **성능 문제**
   - 초기에는 데이터가 쌓일수록 시스템의 응답 속도가 느려지는 성능 저하 문제가 발생했습니다. 이를 해결하기 위해 비동기 처리를 고려했으나, 데이터 구조를 최적화하는 방식으로 성능을 개선하고 문제를 해결했습니다.
3. **프롬프트 작성 문제**
   - AI 챗봇의 프롬프트 작성 중, 날짜나 금액과 같은 사용자 입력이 제대로 처리되지 않거나, 의도한 대로 응답이 나오지 않는 문제가 있었습니다. 이는 프롬프트 구조가 지나치게 복잡하거나, AI 모델이 요구사항을 정확히 파악하지 못한 데서 비롯되었습니다.
   - 문제 해결을 위해 프롬프트를 간결하고 명확하게 수정하여, 날짜와 금액 처리가 올바르게 이루어지도록 하였으며, AI의 응답을 더 직관적으로 유도할 수 있었습니다
4. **차트 새로고침 문제**
   - 프론트엔드에서 JSON 데이터를 차트로 표시할 때, 자동으로 갱신되지 않고 새로고침을 해야만 업데이트되는 현상이 있었습니다.
   - 차트를 새로 그리기 전에 기존 차트 요소를 JSON 초기화 하여 d3.js를 활용하여, 차트를 다시 그릴 때 기존의 SVG 요소를 제거한 뒤 새로운 데이터를 기반으로 차트를 렌더링 하여 실시간으로 데이터가 반영될 수 있게 변경하였습니다.
5. **월간 결산에서 실시간 현황으로 변경하는 문제**
   - LLM에서 바로 가져오는 Json 부분과 디비에서 Json 가져오는 부분을 실시간 데이터를 처리할 수 있도록 필터링 범위를 유연하게 설정 하며  날짜 범위를 월간에서 일간 혹은 실시간으로 조정해야 하였으며 스크립트 부분에서도 LLM에서 가져오는 Json 데이터 값과 디비에서 가져오는 json 데이터 값을 처리하여 반영하도록 하였으며 LLM부분에서는 로딩이 길어 감시 기다려주세요 라는 메시지 표시 하도록 처리 하였습니다.
6. **Django DRF 토큰 기반 인증에서 세션 관리 이슈 해결**
   - 다른 사용자의 URL에 접근이 가능한 문제를 파악했습니다.
   - 확인해본 결과, Django DRF로 백엔드를, 같은 프로젝트의 WEB 앱으로 프론트엔드를 구성하여, 프론트엔드에서 request.user 값이 None으로 반환되었습니다. 토큰 기반 로그인을 사용하면서 세션 정보가 없었기 때문입니다. 따라서 세션이 생성되지 않아 로그인된 사용자의 ID를 얻지 못해 /child_profile/<child_id>/로 리다이렉션할 수 없었습니다.
   - from django.contrib.auth import login을 DRF 로그인 코드에 추가하여 세션을 생성했고, 프론트엔드에서 get_user()를 사용해 세션 기반 사용자 정보를 가져와 리다이렉션이 가능해졌습니다.
7. **AI와의 채팅에서 유저 입력 말풍선과 AI 응답 말풍선이 동시에 나타나는 문제**
   - AI와의 채팅 기능에서 유저가 대화 전송 버튼을 누르면 유저의 말풍선이 먼저 보이지 않고 AI의 응답을 기다렸다가 동시에 보여주는 문제가 있었습니다.
   - 코드를 확인해본 결과 랭체인을 사용하여 유저에 입력에 대한 체인을 호출할 때 유저의 입려과 AI의 응답이 동시에 이루어지는 것을 확인했습니다. html 상에서도 버튼을 눌러 fetch를 실행할 때 입력 값을 전달하고 바로 AI의 응답과 같이 redis에 저장되어 전체 대화 내용을 불러오는 로직이여서 나타나는 문제였습니다.
   -  유저의 말풍선이 전송버튼을 클릭 후 바로 보여주기 위해서 fetch로 post를 실행하기 전에 버튼을 눌러 가져온 유저의 메시지 내용을 유저의 말풍선에 먼저 화면에 추가하는 기능을 넣어주었습니다.

