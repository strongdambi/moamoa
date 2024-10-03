import re
import json
from django.db.models import Sum
from datetime import date
from django.conf import settings
from django.shortcuts import get_object_or_404
from openai import OpenAI
from .models import FinanceDiary, User, MonthlySummary
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from .chatbot import chat_with_bot, get_message_history
from .serializers import FinanceDiarySerializer
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from rest_framework.permissions import IsAuthenticated



# 아이들 작성한 기입장 삭제
class ChatbotProcessDelete(APIView):
    def delete(self, request, pk):
        # pk 값과 child 필드를 기준으로 FinanceDiary 항목
        diary_entry = get_object_or_404(
            FinanceDiary, pk=pk, child=request.user)
        # 현재 사용자가 diary_entry의 child와 동일한지 확인
        if diary_entry.child != request.user:
            return Response({"error": "이 항목을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        diary_entry.delete()
        return Response({"message": "성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 아이 월별 옹돈기입장 리스트
class MonthlyDiaryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, child_pk, year, month):
        user = request.user
        if user.pk != child_pk:
            return Response({"message": "다른 유저는 볼 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        # 해당 연월 용돈 기입장 내역 가져오기
        queryset = user.diaries.filter(
            today__year = year,
            today__month = month
        ).order_by('-today', '-id')
        serializer = FinanceDiarySerializer(queryset, many=True)
        return Response(
            {
            "diary": serializer.data
            },
        )
    


# 채팅 버튼 눌렀을때 화면에 보여주는 대화 목록
class ChatMessageHistory(APIView):
    def get(self, request, child_pk):
        user = request.user
        if user.id != child_pk:
            return Response("대화내역을 볼 권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
        
        session_id=f"user_{user.id}"
        chat_histories = get_message_history(session_id).messages
        message_history = []
        for chat_history in chat_histories:
            # 기본 설정된 message 키값 세팅
            message = {
                "timestamp": chat_history.additional_kwargs.get('time_stamp'), # redis에 저장되어있는 timestamp
                "content": chat_history.content  # 채팅 내역
            }
            # 사람이 입력한 대화 내용
            if isinstance(chat_history, HumanMessage):
                message['type'] = "USER"
                message['username'] = user.first_name
                message_history.append(message)
            # ai가 입력한 대화 내용
            elif isinstance(chat_history, AIMessage):
                # json 데이터 형식의 대화는 제외
                if 'json' not in chat_history.content:
                    message['type'] = "AI"
                    message['ai_name'] = '모아모아'
                    message_history.append(message)
                    

        return Response({"response": message_history})
        
                
    
# 아이들만 작용하는 챗봇
class ChatbotProcessView(APIView):
    def post(self, request):
        user_input = request.data.get('message')
        user = request.user
        parent_id = user.parents

        # 용돈기입 관련 메시지가 아닌 경우
        if not self.is_allowance_related(user_input):
            return Response({
                "message": "용돈기입장과 관련된 정보를 입력해 주세요. 예시: '친구랑 간식으로 3000원 썼어.'"
            })

        # 다중 항목 입력 방지: 금액 패턴이 2개 이상이면 오류 반환
        amount_count = len(re.findall(r'\d+(원|만원|천원|백원)', user_input))
        if amount_count > 1:
            return Response({
                "message": "한 번에 하나씩만 말씀해 주세요! 예를 들어 '장난감 사는데 5000원 썼어요'처럼 말해 주시면 제가 더 쉽게 기록할 수 있어요!"
            }, status=400)

        # OpenAI 프롬프트를 통해 채팅 응답을 받음
        response = chat_with_bot(user_input, user.id)

        # 1 또는 2 입력에 대한 처리
        if user_input in ['1', '2']:
            if user_input == '1' and "json" in response.lower():
                try:
                    # JSON 파싱
                    json_part = response.split("```json")[-1].split("```")[0].replace("'", '"')

                    # 단일 JSON 객체만 처리 (배열이 아닌 경우 오류 처리)
                    plan_json = json.loads(json_part)
                    if isinstance(plan_json, list):
                        return Response({
                            "message": "한 번에 여러 항목을 입력할 수 없습니다. 한 번에 하나씩만 입력해 주세요."
                        }, status=400)

                    # 정상적인 단일 항목 처리
                    finance_diary = FinanceDiary(
                        diary_detail=plan_json.get('diary_detail'),
                        today=plan_json.get('today') or timezone.now().date(),
                        category=plan_json.get('category'),  # OpenAI 응답에서 카테고리 가져오기
                        transaction_type=plan_json.get('transaction_type'),
                        amount=plan_json.get('amount'),
                        child=user,  # child 필드를 명시적으로 추가
                        parent=parent_id
                    )
                    finance_diary.save()

                    # 저장된 계획서를 시리얼라이즈
                    serializer = FinanceDiarySerializer(finance_diary)
                    return Response({
                        "message": "용돈기입장이 성공적으로 저장되었습니다.",
                        "plan": serializer.data  # 단일 계획서만 직렬화
                    })

                except json.JSONDecodeError as e:
                    return Response({
                        "message": "JSON 파싱 오류가 발생했습니다.",
                        "error": str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    return Response({
                        "message": "처리 중 오류가 발생했습니다.",
                        "error": str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            elif user_input == '2':
                return Response({
                    "message": "입력한 내용을 다시 한 번 확인해 주시고, 용돈기입장을 다시 작성해 주세요!"
                })
        return Response({"response": response})


# 우리들의 소악마들을 위한 결계
    def is_allowance_related(self, input_text):
        # 예/아니오 선택이 있을 경우
        if input_text in ['1', '2']:
            return True
        
        # 금액 패턴 (숫자+원 또는 한글로 만원, 천원 등)
        if re.search(r"\d+(원|만원|천원|백원)|[일이삼사오육칠팔구십]만원|[일이삼사오육칠팔구십]천원|[일이삼사오육칠팔구십]백원", input_text):
            return True

        return False  # 금액이나 예/아니오가 아니면 용돈기입장과 관련 없는 것으로 처리


client = OpenAI(api_key=settings.OPENAI_API_KEY)

# 생년월일을 이용한 나이 계산 함수
def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


class MonthlySummaryView(APIView):
    def get(self, request, child_id):
        try:
            # 해당 child_id로 자녀 조회
            try:
                child = User.objects.get(id=child_id, parents__isnull=False)
            except User.DoesNotExist:
                return Response({"error": "해당 자녀를 찾을 수 없습니다."}, status=404)

            # 자녀 이름과 나이 계산
            child_name = child.first_name
            child_age = calculate_age(child.birthday) if child.birthday else "Unknown"

            # 자녀의 이번 달 용돈기입장 데이터 가져오기
            now = timezone.now()
            current_year = now.year
            current_month = now.month

            # 데이터 필터링: 이번 달의 수입/지출 데이터만 가져오기
            diaries = FinanceDiary.objects.filter(child=child, today__year=current_year, today__month=current_month)

            if not diaries.exists():
                return Response({
                    "username": child_name,
                    "age": child_age,
                    "message": f"{child_name}님의 이번 달 용돈기입장 기록이 없습니다."
                }, status=200)

            # 총 수입 계산 (transaction_type이 '수입'인 항목만)
            total_income = diaries.filter(transaction_type='수입').aggregate(Sum('amount'))['amount__sum'] or 0

            # 총 지출 계산 (transaction_type이 '지출'인 항목만)
            total_expenditure = diaries.filter(transaction_type='지출').aggregate(Sum('amount'))['amount__sum'] or 0

            # 카테고리별 지출 계산 (지출 항목만 대상으로)
            category_expenditure = {}
            for diary in diaries.filter(transaction_type='지출'):
                category = diary.category
                if category not in category_expenditure:
                    category_expenditure[category] = 0
                category_expenditure[category] += diary.amount

            # OpenAI에게 메시지 보내서 자동으로 요약, 평가, 계산
            messages = [
                {
                    "role": "system",
                    "content": (
                        f"You are a financial advisor for children. You are given pocket money records for {child_name}, a {child_age}-year-old child. "
                        f"Each record has a `transaction_type` field, which indicates whether the transaction is an '수입' (income) or '지출' (expense). "
                        f"Ensure that only records with `transaction_type` set to '지출' are considered in the expense calculation. "
                        f"Respond entirely in Korean. "
                        f"Here are the records categorized by transaction type and amount:\n"
                        f"{[f'{diary.diary_detail} ({diary.transaction_type}): {diary.amount} KRW' for diary in diaries]}\n\n"
                        f"Please provide the following information in JSON format, using the provided data:\n"
                        f"1. 총_수입 (Total income): {total_income}\n"
                        f"2. 총_지출 (Total expenditure): {total_expenditure}\n"
                        f"3. 남은_금액 (Remaining amount): {total_income - total_expenditure}\n"
                        f"4. 카테고리별_지출 (Expenditure by category): {category_expenditure}\n"
                        f"5. 가장_많이_지출한_카테고리 (Category with the highest expenditure)\n"
                        f"6. 지출_패턴_평가 (Evaluation of the spending pattern, within 100 characters)\n"
                        f"7. 개선을_위한_조언 (Friendly advice for improvement, within 100 characters). "
                    )
                }
            ]

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=2444,
                    temperature=0.7,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )

                # OpenAI 응답 처리
                chat_response = response.choices[0].message.content

                # 요약 정보를 JSON으로 저장
                summary_content = {
                    "username": child_name,
                    "age": child_age,
                    "summary": chat_response  # OpenAI로부터 받은 응답 전체를 저장
                }

                # 데이터베이스에 저장
                parent = child.parents
                summary, created = MonthlySummary.objects.get_or_create(
                    child=child,
                    parent=parent,
                    year=current_year,
                    month=current_month,
                    defaults={"content": summary_content}
                )
                if not created:
                    summary.content = summary_content
                    summary.save()

                return Response(summary_content, status=200)

            except Exception as e:
                return Response({"error": f"OpenAI API 호출 중 오류 발생: {str(e)}"}, status=500)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        