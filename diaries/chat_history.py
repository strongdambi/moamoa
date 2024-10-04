from langchain_community.chat_message_histories import RedisChatMessageHistory
import pytz
from django.utils import timezone
from moamoa.config import TIME_ZONE, REDIS_URL

korea_tz = pytz.timezone(TIME_ZONE)
korea_time = timezone.now().astimezone(korea_tz)

class CustomRedisChatMessageHistory(RedisChatMessageHistory):
    def add_message(self, message):
        # 타임 스탬프 추가
        message.additional_kwargs['time_stamp'] = korea_time.isoformat()
        return super().add_message(message)

# redis 저장 기간
three_months = 90 * 24 * 60 * 60
# Redis 방식 저장
def get_message_history(session_id: str) -> RedisChatMessageHistory:
    # 세션 id를 기반으로 RedisChatMessageHistory 객체를 반환
    return CustomRedisChatMessageHistory(session_id, url=REDIS_URL, ttl=three_months)