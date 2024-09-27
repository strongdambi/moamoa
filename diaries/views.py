import os
import json

from django.conf import settings
from django.shortcuts import get_object_or_404
from openai import OpenAI
from .models import FinanceDiary, User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from .models import Plan  # Plan 모델 임포트
from datetime import datetime

client = OpenAI(api_key=settings.OPENAI_API_KEY)

#아이들 작성한 기입장 삭제
class ChatbotProcessDelete(APIView):
    def delete(self, request, pk):

        # pk 값과 child 필드를 기준으로 FinanceDiary 항목
        diary_entry = get_object_or_404(FinanceDiary, pk=pk, child=request.user)

        # 현재 사용자가 diary_entry의 child와 동일한지 확인
        if diary_entry.child != request.user:
            return Response({"error": "이 항목을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        diary_entry.delete()

        return Response({"message": "성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

# 아이들만 작용하는 챗봇
class ChatbotProcessView(APIView):

    def post(self, request):
        msg = request.data.get("msg", None)

        # 사용자가 메시지를 입력하지 않았을 경우
        if not msg:
            return Response({"error": "채팅이 입력 되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 자녀만 접근 가능 설정
        if request.user.parents_id is None:
            return Response({"error": "이 기능은 어린이만 사용할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        conversation_history = [
            {"role": "system", "content": "You're an assistant that tracks daily expenses and responds in JSON format. Also you can help users when they ask you to change or delete their previous request. {'title':'title','category':'category','transaction_type':'transaction_type','amount':'amount'"},
            {"role": "user", "content": msg}  # POST 요청으로 받은 'msg' 값을 적용
        ]

        try:
            response = client.chat.completions.create( model="gpt-3.5-turbo", messages=conversation_history )
            reply = response.choices[0].message.content

            try:

                # OpenAI에서 받은 응답을 JSON으로 변환
                clean_reply = json.loads(reply)  # 문자열 형태의 JSON을 Python 객체로 변환 (\n 들어가있음)

                # 어시스트에서 보내준 json 정보 추출
                category = clean_reply.get('category')
                transaction_type = clean_reply.get('transaction_type')
                amount = clean_reply.get('amount')
                today = clean_reply.get('date', None)

                # 날짜가 제공되지 않았다면 오늘 날짜로 설정
                if today is None:
                    today = datetime.now().strftime("%Y-%m-%d")

                # 부모님의 ID를 가져옴
                parent_id = request.user.parents_id

                if parent_id is None:
                    return Response({"error": "이 사용자의 부모 정보를 찾을 수 없습니다."},
                                    status=status.HTTP_400_BAD_REQUEST)

                # 부모님의 User 인스턴스를 가져옴
                try:
                    parent_user = User.objects.get(pk=parent_id)
                except User.DoesNotExist:
                    return Response({"error": "부모 사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

                # FinanceDiary 모델에 맞게 추가
                FinanceDiary.objects.create(child=request.user, parent=parent_user, title=msg, category=category,
                                            transaction_type=transaction_type, amount=amount,
                                            today=datetime.strptime(today, "%Y-%m-%d"))

            except json.JSONDecodeError:
                # OpenAI 응답을 파싱하지 못했을 때
                return Response({"error": "OpenAI의 응답을 구문 분석하지 못했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # 성공적으로 처리된 경우 OpenAI의 응답을 반환
            return Response({"result": reply}, status=status.HTTP_200_OK)

        except Exception as e:

            # 기타 예외 처리
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PreviousMonthPlansView(APIView):
    file_path = os.path.join(settings.BASE_DIR, 'output.txt')

    def get(self, request):
        try:
            # 부모가 있는 자녀들을 필터링하여 가져옴
            children_with_parents = User.objects.filter(parents__isnull=False)

            # 자녀 ID, 이름, 부모 ID를 output.txt 파일에 기록
            with open(self.file_path, 'w', encoding='utf-8') as file:
                for child in children_with_parents:
                    file.write(f"{child.id}|{child.first_name}|{child.parents.id}\n")

            # 기록한 파일을 읽어 첫 번째 라인의 자녀 정보 가져오기
            with open(self.file_path, 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()
                parts = first_line.split('|')

                # 자녀 이름과 ID 추출
                username = parts[1]
                child_id = parts[0]

                messages = []
                messages_system = {"role": "system","content": f"Create a fictional set of pocket money ledger data on this month, summarize it, evaluate it, and give advice on how to improve. Also, provide a score based on general standards. The tone should be kind and friendly, as if explaining to a child aged 5 to 13. Answer in Korean. Call user as {username}."}
                messages_user = { "role": "user", "content": "해줘"}
                messages.append(messages_system)
                messages.append(messages_user)

                try:

                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=messages,
                        max_tokens=2444,
                        temperature=0.7,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )

                    chat_response = response.choices[0].message.content

                    # 자녀와 부모 정보 가져오기
                    child = User.objects.get(pk=child_id)
                    parent = child.parents

                    # 현재 연도와 월 가져오기
                    now = timezone.now()
                    year = now.year
                    month = now.month

                    # 자녀와 부모에 해당하는 이달의 계획서가 있는지 확인
                    plan = Plan.objects.filter(child=child, parent=parent, year=year, month=month).first()

                    if plan:
                        # 계획서가 있으면 내용을 업데이트
                        plan.content = chat_response
                        plan.save()
                        message = "계획서가 업데이트되었습니다."
                    else:
                        # 계획서가 없는 경우 새로 생성
                        Plan.objects.create(child=child, parent=parent, year=year, month=month, content=chat_response)
                        message = "계획서가 생성되었습니다."

                    # 성공 메시지와 함께 응답 반환
                    return Response({"message": message, "Response": chat_response}, status=200)

                except Exception as e:
                    # OpenAI API 호출 또는 처리 중 오류 발생 시
                    return Response({"error": str(e)}, status=500)

        except Exception as e:
            # 전반적인 처리 중 발생하는 오류 처리
            return Response({"error": str(e)}, status=500)