# 🎁 모아모아 (아이들을 위한 용돈기입장)

모아모아는 아이(5세~13세)들에게 금융에대한 이해와 교육을 알려주기 위해 만든 서비스이며, AI와의 채팅을통해 용돈기입장 작성을 도와주고 월간 용돈기입장의 데이터를 통해서 부모님들에게 아이의 소비 습관을 보여주고 그 소비습관에 맞는 방향성을 제시해주는 서비스입니다. 

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

## 📋 API 사용법

| 기능                    | HTTP 메서드 | 엔드포인트                                   | 설명                                                    |
|-------------------------|-------------|---------------------------------------------|-------------------------------------------------------------|
| **부모 회원가입**       | POST        | `/api/v1/accounts/auth/kakao/callback/`       | 인덱스의 카카오 소셜 로그인을 통해 회원가입 진행 및 토큰 발급                 |
| **자녀 회원가입**        | POST       | `/api/v1/accounts/children/create/`            | 부모프로필 페이지에서 자녀 추가를 통해 회원가입 진행                        |
| **자녀 로그인**          | POST        | `/api/v1/accounts/login/`                     | 인덱스의 키즈 로그인을 통해서 아이디 및 비밀번호 입력후 쿠키 및 JWT토큰 발급  |
| **로그아웃**             | POST        | `/api/v1/accounts/logout/`                    | refresh_token 블랙리스트 추가 및 쿠키의 JWT토큰 삭제                        |           
| **refresh_token 발행**   | POST        | `/api/v1/accounts/token/refresh/`             | refresh_token을 통해 access_token 재발급                                    |
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
- **OpenAI**: AI 모델.
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
   - 프론트엔드에서 JSON 데이터를 차트로 표시할 때, 자동으로 갱신되지 않고 새로고침을 해야만 업데이트되는 현상이 있었습니다. 이 문제는 데이터가 차트에 바로 반영되지 않는 현상으로, 해결 방안을 모색 중입니다.

