from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings
from langchain_core.runnables.utils import ConfigurableFieldSpec
from django.utils import timezone
import traceback
import redis

REDIS_URL = 'redis://localhost:6379/0'


llm = ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", """
        Step 1
        - You're an AI assistant that makes pocket money for children aged 5 to 13
        Step 2
        - When you receive the contents of the pocket money report from the kid, make a pocket money report form based on the contents and show it to the child
        - Today is {recent_day}
        - Please check again to see if the user's answer is correct. No. 1 is "Yes," and No. 2 is "No, I want to rewrite it."
        Step 3
        - If it's number 1, convert it to json, and if it's number 2, kindly tell the user to rewrite it
        Step 4
        - As a result, if the user says number 1 when asked, please convert it to the following json format
        
        ```json
        {{
            'diary_detail':'Briefly include how much kid spend and where kid spend it', 
            'today':You can put the date of your child's allowance in like yyyy-mm-dd. If you didn't mention the date of use, please put it in today's date, 
            'category':'category',
            'transaction_type':'transaction_type',
            'amount': 0
        }}
        ```
        Please proceed with all conversations in Korean and add the json value in Korean format
    """),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

runnable = chat_prompt | llm | StrOutputParser()


# InMemory 방식 저장
# store={}
# def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
#     if (user_id, conversation_id) not in store:
#         store[(user_id, conversation_id)] = ChatMessageHistory()
#     return store[(user_id, conversation_id)]

# with_message_history = (
#     RunnableWithMessageHistory(
#         runnable,
#         get_session_history, # 세션 기록
#         input_messages_key="input",  # 입력 메시지의 키
#         history_messages_key="chat_history",  # 기록 메시지의 키
#         history_factory_config=[
#             ConfigurableFieldSpec(
#                 id="user_id",
#                 annotation=str,
#                 name="User ID",
#                 description="사용자의 고유 식별자입니다.",
#                 default="",
#                 is_shared=True,
#             ),
#             ConfigurableFieldSpec(
#                 id="conversation_id",
#                 annotation=str,
#                 name="Conversation ID",
#                 description="대화의 고유 식별자입니다.",
#                 default="",
#                 is_shared="True",
#             ),
#         ]
#     )
# )

# Redis 방식 저장
def get_message_history(session_id: str) -> RedisChatMessageHistory:
    # 세션 id를 기반으로 RedisChatMessageHistory 객체를 반환
    return RedisChatMessageHistory(session_id, url=REDIS_URL)


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


# Views.py와 함수 연결
def chat_with_bot(user_input, user_id):
    try:
        session_id = f"user_{user_id}"
        response = with_message_history.invoke(
            # 질문 입력
            {"recent_day": timezone.now().date(), "input": user_input},
            # 세션 ID 기준으로 대화를 기록
            config={"configurable": {"session_id": session_id}}
            # 유저PK와 방 아이디 값 부여
            # config={"configurable": {"user_id": user_id,
            #                         "conversation_id": user_username}},
        )
        return response
    except Exception as e:
        print(f"챗봇 오류: {str(e)}")
        return "죄송합니다. 채팅 서비스에 일시적인 문제가 발생했습니다."
