from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Plan
from .serializers import PlanSerializer
from .chatbot import chat_with_bot
import json

class ChatbotView(APIView):
    def post(self, request): 
        user_input = request.data.get('message')
        response = chat_with_bot(user_input)
        
        # response에 json단어가 있으면
        if "json" in response:
            try:
                # JSON 형식의 용돈 계획서 추출
                plan_json = json.loads(response.split("```json")[-1].split("```")[0])
                
                # AllowancePlan 객체 생성 및 저장
                allowance_plan = Plan(
                    total_amount=plan_json['total_amount'],
                    food_expense=plan_json['food_expense'],
                    transportation_expense=plan_json['transportation_expense'],
                    savings=plan_json['savings'],
                    snack_expense=plan_json['snack_expense'],
                    plan_details=plan_json['plan_details']
                )
                allowance_plan.save()
                
                # 저장된 계획서를 시리얼라이즈
                serializer = PlanSerializer(allowance_plan)
                return Response({
                    "message": "용돈 계획서가 성공적으로 저장되었습니다.",
                    "plan": serializer.data,
                    "response": response
                })
            except json.JSONDecodeError:
                return Response({
                    "message": "용돈 계획서 형식이 올바르지 않습니다.",
                    "response": response
                })
        
        return Response({"response": response})