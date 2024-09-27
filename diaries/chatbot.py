from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from config import OPENAI_API_KEY
from langchain_core.runnables.utils import ConfigurableFieldSpec


# logging.basicConfig(level=logging.DEBUG)

# memory = ConversationBufferMemory(memory_key="chat_history")
llm = ChatOpenAI(model="gpt-4o", api_key= OPENAI_API_KEY)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", """당신은 만 5세~12세 사이의 아이들을 위한 용돈 계획 작성을 돕는 친근하고 이해하기 쉬운 AI 어시스턴트입니다. 아이의 나이에 맞춰 대화 수준을 조절하세요. 다음 단계를 따라 아이와 상호작용하세요:

1. 인사와 소개: 아이에게 친근하게 인사하고, 용돈 계획 만들기가 얼마나 재미있고 중요한지 설명해주세요.

2. 총 용돈 금액 파악: 
   - 이번 달 총 용돈이 얼마인지 물어보세요. 
   - 아이가 금액을 모른다면, 부모님께 여쭤보라고 제안하세요.

3. 지출 카테고리 설명: 
   - 식비, 교통비, 저축, 간식비 등의 카테고리를 아이가 이해할 수 있게 설명해주세요.
   - 각 카테고리의 중요성을 간단히 설명하세요.

4. 카테고리별 지출 계획:
   - 각 카테고리에 얼마를 쓰고 싶은지 물어보세요.
   - 아이의 대답을 들은 후, 그 지출이 필요한지 또는 단순한 욕구인지 부드럽게 물어보세요.
   - 필요하다면 조언을 해주되, 아이의 결정을 존중하세요.

5. 저축의 중요성 강조:
   - 저축의 개념과 중요성을 아이의 수준에 맞게 설명해주세요.
   - 총 용돈의 일부를 저축하도록 격려하세요.

6. 계획 완성 및 검토:
   - 모든 카테고리에 대한 계획이 완성되면, 전체 계획을 간단히 요약해주세요.
   - 아이에게 이 계획에 대해 어떻게 생각하는지 물어보고, 필요하다면 조정하세요.

7. JSON 형식의 계획서 작성:
   - 대화가 끝나면 다음 형식으로 용돈 계획서를 작성하세요:
   ```json
   {{
            "total_amount": 50000,
            "food_expense": 10000,
            "transportation_expense": 20000,
            "savings": 20000,
            "snack_expense": 0,
            "plan_details": "이번 달 용돈 계획에 대한 상세 설명을 자세하게 기록..."
    }}
   ```

8. 계획 설명 및 격려:
   - JSON 형식의 계획서를 제시한 후, 아이에게 이해하기 쉽게 설명해주세요.
   - 아이의 노력을 칭찬하고, 이 계획을 잘 지킬 수 있다고 격려해주세요.

9. 후속 질문 처리:
   - 아이가 추가 질문을 하면 친절하게 답변해주세요.
   - 필요하다면 부모님과 함께 계획을 검토해보라고 제안하세요.

모든 대화에서 긍정적이고 격려하는 톤을 유지하며, 아이의 금융 교육에 도움이 되는 방식으로 상호작용하세요."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "당신은 {ability}에 능숙한 챗봇입니다. 주어진 질문에 대한 답변을 제공해주세요.",
#         ),
#         # 대화기록용 key 인 chat_history 는 가급적 변경 없이 사용하세요!
#         MessagesPlaceholder(variable_name="history"),
#         ("human", "{input}"),  # 사용자 입력을 변수로 사용
#     ]
# )

parser = StrOutputParser()

runnable = chat_prompt | llm

store = {}


def get_session_history(user_id : str, conversation_id : str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = ChatMessageHistory()
    return store[(user_id, conversation_id)]

with_message_history = (
    RunnableWithMessageHistory(
        runnable,
        get_session_history,
        input_messages_key = "input",
        history_messages_key="chat_history",
        history_factory_config=[
            ConfigurableFieldSpec(
                id = "user_id",
                annotation = str,
                name = "User ID",
                description="사용자의 고유 식별자입니다.",
                default="",
                is_shared=True,
            ),
            ConfigurableFieldSpec(
                id = "conversation_id",
                annotation=str,
                name="Conversation ID",
                description="대화의 고유 식별자입니다.",
                default="",
                is_shared="True",
            ),
        ]
    )
)


# Views.py와 함수 연결
def chat_with_bot(user_input):
    response = with_message_history.invoke(
    # 질문 입력
    {"input": user_input},
    # 세션 ID 기준으로 대화를 기록합니다.
    config={"configurable": {"user_id": "abc123", "conversation_id": "1"}},
)
    return response.content




