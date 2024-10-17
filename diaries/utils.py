# langchain 라이브러리
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
# 장고 라이브러리
from django.conf import settings
# 시간 관련 라이브러리
from datetime import timedelta, date
from .chat_history import get_current_korea_date
# 캡슐 라이브러리
from .prompts import chat_prompt
from .chat_history import get_message_history
from .models import FinanceDiary
# 정규표현식 라이브러리
import re

llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)

runnable = chat_prompt | llm | StrOutputParser()

with_message_history = RunnableWithMessageHistory(
    runnable,
    get_message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# 사용자 입력값을 토대로 날짜 계산
def convert_relative_dates(user_input):
    today = get_current_korea_date()
    if "오늘" in user_input:
        return today
    elif "어제" in user_input:
        return today - timedelta(days=1)
    elif "그저께" in user_input:
        return today - timedelta(days=2)
    else:
        return None
# 프롬프트 전달 데이터
prompt_data = {
    "limit" : "<strong>사용하기에는 너무 많은 금액이에요!<br> 100만원 밑으로 입력해보는게 어때요?</strong>🤗",
    "chat_format" : """입력하신 내용을 바탕으로 기록을 정리해 보았습니다.
1. <strong>날짜</strong>: 2024-10-15
2. <strong>금액</strong>: 5000원
3. <strong>사용 내역</strong>: 탕후루를 샀음
4. <strong>분류</strong>: 음식
5. <strong>거래 유형</strong>: 지출
위 내용이 맞는지 확인해 주세요!
<br>1. 맞아요! <br> 2. 아니요, 다시 수정할래요!""",
    "notice" : "<strong>용돈기입장과 관련된 정보를 입력해 주세요!<br> 지출 또는 용돈 날짜와 금액 그리고 어떻게 사용했는지 꼭 입력하셔야되요! <br> 입력하지 않으면 모아모아는 알아듣지를 못한답니다</strong>🥺",
}

# Views.py와 함수 연결
def chat_with_bot(user_input, user_id):
    try:
        session_id = f"user_{user_id}"
        current_date = get_current_korea_date()
        response = with_message_history.invoke(
            {"limit":prompt_data.get("limit"), "chat_format":prompt_data.get("chat_format"),"answer_check": prompt_data.get("answer_check"), "notice": prompt_data.get("notice"), "recent_day": current_date, "input": user_input},
            config={"configurable": {"session_id": session_id}}
        )

        # 수입/지출 관련 모든 영단어를 한글로 변환
        if isinstance(response, str):
            response = (
                response.replace("income", "수입")
                        .replace("earnings", "수입")
                        .replace("revenue", "수입")
                        .replace("profit", "수입")
                        .replace("expense", "지출")
                        .replace("expenditure", "지출")
                        .replace("spending", "지출")
                        .replace("cost", "지출")
            )
        return response
    except Exception as e:
        print(f"챗봇 오류: {str(e)}")
        return "죄송합니다. 채팅 서비스에 일시적인 문제가 발생했습니다."


# 우리들의 소악마들을 위한 결계
def is_allowance_related(input_text):
    # 예/아니오 선택이 있을 경우
    if input_text in ['1', '2','네','아니오','맞아요','틀려요', '예', '아니요', '응', '아니']:
        return True
    
    # 금액 패턴 (숫자+원 또는 한글로 만원, 천원 등)
    if re.search(r"\d+(원|만원|천원|백원)|[일이삼사오육칠팔구십]만원|[일이삼사오육칠팔구십]천원|[일이삼사오육칠팔구십]백원|만원|천원|백원", input_text):
        return True

    return False  # 금액이나 예/아니오가 아니면 용돈기입장과 관련 없는 것으로 처리

# 생년월일을 이용한 나이 계산 함수
def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


# 잔액 업데이트 함수 정의
def update_remaining_balance(child):
    # 해당 child의 모든 finance_diary 기록을 today 날짜 기준으로 정렬해서 불러옵니다.
    finance_entries = FinanceDiary.objects.filter(child=child).order_by('today')
    
    total_balance = 0
    for entry in finance_entries:
        if entry.transaction_type == "수입":
            total_balance += entry.amount
        elif entry.transaction_type == "지출":
            total_balance -= entry.amount
        
        # 각 항목의 remaining을 업데이트
        entry.remaining = total_balance
        entry.save()

    # child.total 업데이트
    child.total = total_balance
    child.save()
