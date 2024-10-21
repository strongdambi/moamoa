import re
import json
import redis
# 장고 라이브러리
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import DateField
from django.db.models.functions import TruncMonth
# drf 라이브러리
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# 캡슐 라이브러리
from accounts.models import User
from .models import FinanceDiary, User, MonthlySummary
from .chat_history import get_message_history
from .utils import chat_with_bot, calculate_age, update_remaining_balance, is_allowance_related
# 직렬화 라이브러리
from .serializers import FinanceDiarySerializer, MonthlySummarySerializer
# langchain 관련 라이브러리
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
# openai 관련 라이브러리
from openai import OpenAI
# 시간 라이브러리
from datetime import datetime


class CheckTokenView(APIView):
    def get(self, request):
        if not request.auth:
            return Response({}, status=401)
        return Response({}, status=200)

# 아이들 작성한 기입장 삭제
class ChatbotProcessDelete(APIView):
    def delete(self, request, pk):
        child = request.user
        
        # pk 값과 child 필드를 기준으로 FinanceDiary 항목 찾기
        diary_entry = get_object_or_404(
            FinanceDiary, pk=pk, child=child.pk)
        
        # 수입 지출 판단
        # 수입이면 다시 마이너스
        if diary_entry.transaction_type == '수입':
            child.total -= diary_entry.amount
        # 지출이면 다시 플러스
        elif diary_entry.transaction_type == '지출':
            child.total += diary_entry.amount    
        
        # 항목 삭제
        diary_entry.delete()
        
        # 잔액 업데이트
        update_remaining_balance(child)

        return Response({"message": "성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 아이 월별 용돈기입장 리스트(영훈)
class MonthlyDiaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, child_pk, year, month):

        try:
            child = User.objects.get(pk=child_pk)
        except User.DoesNotExist:
            return Response({"message": "다른 유저는 볼 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        queryset = child.diaries.filter(
            today__year=year,
            today__month=month
        ).order_by('-created_at', '-id')

        serializer = FinanceDiarySerializer(queryset, many=True)
        return Response(
            {
                "diary": serializer.data,
                "remaining_amount": queryset.last().remaining if queryset.exists() else 0,  # 가장 최근의 남은 금액 반환
            },
        )


# 키즈 프로필 콤보박스 월을 동적으로 표시하기 위함
class AvailableMonthsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, child_pk):
        # 특정 자녀의 용돈기입장 기록을 조회
        finance_entries = FinanceDiary.objects.filter(
            child_id=child_pk).dates('today', 'month')

        # 용돈기입장 기록이 있는 달만 추출
        available_months = [entry.strftime("%Y-%m")
                            for entry in finance_entries]

        return Response({
            "available_months": available_months
        })


# 채팅 메시지 기록을 가져오는 뷰
class ChatMessageHistory(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request, child_pk):
        if request.user.pk != child_pk:
                    return Response({"error": "자신의 정보만 조회할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        try:
            child = User.objects.get(pk=child_pk)
        except User.DoesNotExist:
            return Response({"message": "다른 유저는 볼 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 자녀와의 채팅 세션 처리 (child.id 사용)
        session_id = f"user_{child.id}"
        chat_histories = get_message_history(session_id).messages
        message_history = []

        # 채팅 기록을 변환하여 저장
        for chat_history in chat_histories:
            message = {
                # redis에 저장되어있는 timestamp
                "timestamp": chat_history.additional_kwargs.get('time_stamp'),
                "content": chat_history.content  # 채팅 내역
            }
            # 사람이 입력한 대화 내용
            if isinstance(chat_history, HumanMessage):
                message['type'] = "USER"
                message['username'] = child.first_name
                message['user_profile_image'] = request.build_absolute_uri(
                        child.images.url)
                message_history.append(message)
                
            # AI가 입력한 대화 내용
            elif isinstance(chat_history, AIMessage):
                message['type'] = "AI"
                message['ai_name'] = '모아모아'
                message['ai_profile_image'] = request.build_absolute_uri(
                        '/media/default_profile.png')
                message_history.append(message)
        return Response({"response": message_history})


# 아이들 작성한 기입장 처리
class ChatbotProcessView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request):
        user_input = request.data.get('message')
        child_pk = request.data.get('child_pk')  # body에서 child_pk를 추출
        user = request.user

        try:
            child = User.objects.get(pk=child_pk)
        except User.DoesNotExist:
            return Response({"message": "다른 유저는 이 기능을 사용할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 다중 항목 입력 방지: 금액 패턴이 2개 이상이면 오류 반환
        # amount_count = len(re.findall(r'\d+(원|만원|천원|백원)', user_input))
        # if amount_count > 1:
        #     return Response({
        #         "message": "한 번에 하나씩만 말씀해 주세요! 예를 들어 '장난감 사는데 5000원 썼어요'처럼 말해 주시면 제가 더 쉽게 기록할 수 있어요!"
        #     }, status=400)
            
        # if not is_allowance_related(user_input):
        #     response_message = "<strong>용돈기입장과 관련된 정보를 입력해 주세요!<br> 지출 또는 용돈 날짜와 금액 그리고 어떻게 사용했는지 꼭 입력하셔야되요! <br> 입력하지 않으면 모아모아는 알아듣지를 못한답니다</strong>🥺"
        #     session_id = f"user_{child.id}"
        #     chat_histories = get_message_history(session_id)
        #     chat_histories.add_user_message(user_input)
        #     chat_histories.add_ai_message(response_message)

        #     return Response({})

        # OpenAI 프롬프트를 통해 채팅 응답을 받음
        response = chat_with_bot(user_input, child_pk)
        print(response)

        # 1 또는 2 입력에 대한 처리
        if "json" in response.lower():
            try:
                # JSON 파싱
                json_part = response.split("```json")[-1].split("```")[0].strip().replace("'", '"')

                # 단일 JSON 객체만 처리 (배열이 아닌 경우 오류 처리)
                plan_json = json.loads(json_part)
                
                saved_diaries = []
                # 여러개 항목일때
                if isinstance(plan_json, list):
                    for item in plan_json:
                        today_str = item.get('today')
                        if today_str:
                            today_date = datetime.strptime(today_str, '%Y-%m-%d').date()  # 문자열을 날짜로 변환
                        else:
                            today_date = timezone.now().date()

                        finance_diary = FinanceDiary(
                            diary_detail=item.get('diary_detail'),
                            today=today_date,
                            category=item.get('category'),
                            transaction_type=item.get('transaction_type'),
                            amount=item.get('amount'),
                            remaining=child.total,  # 추가 전에 잔액 설정
                            child=child,
                            parent=user.parents
                        )
                        finance_diary.save()
                        saved_diaries.append(finance_diary)
                    # return Response({
                    #     "message": "한 번에 여러 항목을 입력할 수 없습니다. 한 번에 하나씩만 입력해 주세요."
                    # }, status=400)
                else:
                    # 오늘 날짜 확인 및 문자열 -> 날짜 변환
                    today_str = plan_json.get('today')
                    if today_str:
                        today_date = datetime.strptime(today_str, '%Y-%m-%d').date()  # 문자열을 날짜로 변환
                    else:
                        today_date = timezone.now().date()

                    # 정상적인 단일 항목 처리
                    finance_diary = FinanceDiary(
                        diary_detail=plan_json.get('diary_detail'),
                        today=today_date,
                        category=plan_json.get('category'),
                        transaction_type=plan_json.get('transaction_type'),
                        amount=plan_json.get('amount'),
                        remaining=child.total,  # 추가 전에 잔액 설정
                        child=child,
                        parent=user.parents
                    )
                    finance_diary.save()
                    saved_diaries.append(finance_diary)

                # 새로운 항목이 저장된 후 잔액 업데이트
                update_remaining_balance(child)

                # 저장된 계획서를 시리얼라이즈
                serializer = FinanceDiarySerializer(saved_diaries, many=True)
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

        return Response({"response": response})


client = OpenAI(api_key=settings.OPENAI_API_KEY)


class MonthlySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, child_id):

        year = request.data.get('year')
        month = request.data.get('month')

        # 유효성 검사
        if not year or not month:
            return Response({"error": "연도와 월이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 부모님(로그인한 사용자) 정보 추출
        parent = request.user

        # 자녀 정보를 데이터베이스에서 가져옴
        try:
            child = get_object_or_404(User, pk=child_id, parents=parent)
        except User.DoesNotExist:
            return Response({"error": "해당하는 자녀를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 현재 날짜 구하기
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        # 요청 받은 year, month를 비교
        year = int(year)
        month = int(month)

        if year == current_year and month == current_month:

            # 현재 년도와 월인 경우 데이터를 계속 업데이트
            summary_content = self.create_summary_content(child, year, month)

            # 현재 년도와 월인 경우 데이터를 계속 업데이트
            MonthlySummary.objects.update_or_create(
                child=child,
                parent=parent,
                year=year,
                month=month,
                defaults={"content": summary_content}  # 여기서 JSON 데이터를 content로 저장
            )

            return Response(self.create_summary_content(child, year, month), status=status.HTTP_200_OK)

        else:

            # 해당 연도와 월에 맞는 계획서를 조회
            summary = MonthlySummary.objects.filter(child=child, parent=parent, year=year, month=month).first()

            if summary:
                # 계획서가 존재하는 경우, 기존 계획서를 반환
                serializer = MonthlySummarySerializer(summary)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                # 데이터가 없을 경우 새 계획서 생성]
                summary_content = self.create_summary_content(child, year, month)

                if not summary_content["message"]:
                    MonthlySummary.objects.get_or_create(
                        child=child,
                        parent=parent,
                        year=year,
                        month=month,
                        defaults={"content": summary_content}  # 여기서 JSON 데이터를 content로 저장
                    )

                return Response(summary_content, status=status.HTTP_200_OK)

    def create_summary_content(self, child, year, month):
        # 자녀 이름과 나이 계산
        child_name = child.first_name
        child_age = calculate_age(child.birthday) if child.birthday else "Unknown"

        # 자녀의 이번 달 용돈기입장 데이터 가져오기
        current_year = year
        current_month = month

        # 데이터 필터링: 해당 월의 수입/지출 데이터만 가져오기
        diaries = FinanceDiary.objects.filter(child=child, today__year=current_year, today__month=current_month)
        if not diaries.exists():
            return {"username": child_name, "age": child_age,
                    "message": f"{child_name}님의 {current_year}년 {current_month}월 용돈기입장 기록이 없습니다."}

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
                    f"Each record has a transaction_type field, which indicates whether the transaction is an '수입' (income) or '지출' (expense). "
                    f"Ensure that only records with transaction_type set to '지출' are considered in the expense calculation. "
                    f"Respond entirely in Korean. "
                    f"Here are the records categorized by transaction type and amount:\n"
                    f"{[f'{diary.diary_detail} ({diary.transaction_type}): {diary.amount} KRW' for diary in diaries]}\n\n"
                    f"Please provide the following information in JSON format, using the provided data:\n"
                    f"1. 총_수입 (Total income): {total_income}\n"
                    f"2. 총_지출 (Total expenditure): {total_expenditure}\n"
                    f"3. 남은_금액 (Remaining amount): {total_income - total_expenditure}\n"
                    f"4. 카테고리별_지출 (Expenditure by category): {category_expenditure}\n"
                    f"5. 가장_많이_지출한_카테고리 (Category with the highest expenditure)\n"
                    f"6. 지출_패턴_평가 (Don't say kid's name. Say just kid and Evaluation of the spending pattern and Friendly advice for improvement to parent, within 400 characters)\n"
                )
            }
        ]

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

        # JSON 문자열 추출 및 파싱
        json_str = chat_response.strip().strip('`').strip()
        if json_str.startswith('json'):
            json_str = json_str[4:].strip()
        summary_data = json.loads(json_str)

        # 요약 정보를 JSON으로 저장
        return {
            "username": child_name,
            "age": child_age,
            "summary": summary_data  # 파싱된 JSON 데이터 저장
        }