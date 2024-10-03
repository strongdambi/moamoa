from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings
from langchain_core.messages import AIMessage
from langchain_core.runnables.utils import ConfigurableFieldSpec
from django.utils import timezone
import pytz
from datetime import datetime, timedelta
import traceback
import redis

REDIS_URL = 'redis://localhost:6379/0'

llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", """
        Step 1
        - You are an AI assistant that helps children aged 5 to 13 record their pocket money entries.

        Step 2
        - When the child provides the details of their pocket money report, create a report based on the input and show it to them.
        - Today's date in Korea is {recent_day}. Always use this date unless the child specifically mentions a different date.

        Step 3
        - Use the following categories to classify the pocket money entry. Choose the most appropriate category key based on the input:
            - 용돈
            - 기타/수입
            - 음식
            - 음료/간식
            - 문구/완구
            - 교통
            - 문화/여가
            - 선물
            - 기부
            - 기타/지출

        Step 4
        - Please ask the child to confirm if the report is correct: "1. Yes" or "2. No, I want to rewrite it."

        Step 5
        - If the child selects "1", convert their input into the following JSON format:

        ```json
        {{
            'diary_detail': 'Briefly describe how much the child spent and where they spent it with formal language',
            'today': 'The date provided by the child or today’s date if no date was given',
            'category': 'The category key that best matches the child’s entry',
            'transaction_type': 'transaction_type',
            'amount': 0
        }}
        ```

        Step 6
        - Always conduct conversations in Korean, but keep the JSON keys in English.
    """),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

runnable = chat_prompt | llm | StrOutputParser()

# 한국 시간대 설정
KOREA_TZ = pytz.timezone(settings.TIME_ZONE)

# 현재 한국 시간을 가져오는 함수
def get_current_korea_time():
    return timezone.now().astimezone(KOREA_TZ)

# 현재 한국 날짜를 가져오는 함수
def get_current_korea_date():
    return get_current_korea_time().date()

class CustomRedisChatMessageHistory(RedisChatMessageHistory):
    def add_message(self, message):
        # 현재 한국 시간 가져오기
        korea_time = get_current_korea_time()
        # 타임 스탬프 추가
        message.additional_kwargs['time_stamp'] = korea_time.isoformat()
        return super().add_message(message)

# redis 저장 기간
three_months = 90 * 24 * 60 * 60
# Redis 방식 저장
def get_message_history(session_id: str) -> RedisChatMessageHistory:
    # 세션 id를 기반으로 RedisChatMessageHistory 객체를 반환
    return CustomRedisChatMessageHistory(session_id, url=REDIS_URL, ttl=three_months)


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


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
