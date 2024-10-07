# langchain 라이브러리
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
# 장고 라이브러리
from django.conf import settings
# 시간 관련 라이브러리
from datetime import timedelta, date
from .chat_history import get_current_korea_date
# 정규표현식
import re
# 캡슐 라이브러리
from .prompts import chat_prompt
from .chat_history import get_message_history
# 비동기 처리 라이브러리
import aiohttp


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


# Views.py와 함수 연결
def chat_with_bot(user_input, user_id):
    try:
        session_id = f"user_{user_id}"
        current_date = get_current_korea_date()
        input_with_date = f"오늘의 날짜는 {current_date}입니다. {user_input}"
        response = with_message_history.invoke(
            {"recent_day": current_date, "input": input_with_date},
            config={"configurable": {"session_id": session_id}}
        )
        return response
    except Exception as e:
        print(f"챗봇 오류: {str(e)}")
        return "죄송합니다. 채팅 서비스에 일시적인 문제가 발생했습니다."


# 우리들의 소악마들을 위한 결계
def is_allowance_related(input_text):
    # 예/아니오 선택이 있을 경우
    if input_text in ['1', '2']:
        return True
    
    # 금액 패턴 (숫자+원 또는 한글로 만원, 천원 등)
    if re.search(r"\d+(원|만원|천원|백원)|[일이삼사오육칠팔구십]만원|[일이삼사오육칠팔구십]천원|[일이삼사오육칠팔구십]백원", input_text):
        return True

    return False  # 금액이나 예/아니오가 아니면 용돈기입장과 관련 없는 것으로 처리

# 생년월일을 이용한 나이 계산 함수
def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
