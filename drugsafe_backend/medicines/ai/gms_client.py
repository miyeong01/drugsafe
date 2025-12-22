from django.conf import settings
from openai import AsyncOpenAI
import os, json, re

def get_client():
    return AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1"
    )

def safe_json_parse(text: str) -> dict:
    """
    GPT 출력에서 JSON 부분만 추출해서 파싱
    """
    try:
        # JSON 객체만 추출
        match = re.search(r'\{[\s\S]*\}', text)
        if not match:
            raise ValueError("JSON 형식 아님")

        return json.loads(match.group())

    except Exception:
        return {
            "intent": "unknown",
            "symptom": None,
            "form": None,
            "drugs": None
        }

async def parse_user_input(user_message: str) -> dict:
    # DB에 저장된 15가지 표준 증상 리스트
    symptom_list = "두통, 치통, 발열, 복통, 생리통, 위장약, 종합감기, 코감기, 기침, 재채기, 소화불량, 알레르기, 육체피로, 관절통, 근육통"

    prompt = f"""
너는 의약품 검색을 위한 자연어 처리기이자 JSON 변환기다.
사용자의 질문을 분석하여 의도(intent)와 상세 정보를 추출해.

[표준 증상 리스트]
{symptom_list}

[작업 규칙]
1. 사용자의 표현이 모호하더라도 반드시 위 [표준 증상 리스트] 중 가장 적절한 것으로 매핑해.
   - 예: "머리 아파", "머리 무거워" -> "두통"
   - 예: "콧물 나", "코 막혀" -> "코감기"
   - 예: "에취", "코 간지러워" -> "재채기"
   - 예: "열이 나", "몸이 뜨거워" -> "발열"
2. 만약 특정 약 이름(예: 타이레놀, 아스피린)이 언급되면 `drug_name`에 넣고, `intent`를 'drug_info'로 설정해.
3. 약 이름 없이 증상만 말하며 추천을 원하면 `intent`를 'recommend'로 설정해.

출력은 오직 JSON만 허용한다.

출력 형식:
{{
  "intent": "recommend | drug_info | unknown",
  "symptom": "위 표준 리스트 중 하나 또는 null",
  "drug_name": "추출된 약 이름 또는 null",
  "form": "정제, 액상, 시럽 등 또는 null",
  "sort": "rating | review | relevance | null"
}}

문장:
"{user_message}"
"""
    client = get_client()
    res = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300, # 필드가 늘어났으므로 약간 상향
    )

    raw = res.choices[0].message.content
    return safe_json_parse(raw)


async def explain(context: str, user_message: str) -> str:
    system_prompt = f"""
너는 친절하고 전문적인 의약품 상담사 'DrugSafe AI'야.

[응답 규칙]
1. 제공된 [DB 정보]를 바탕으로 정확하게 답변한다.
2. 약의 효능과 주의사항을 요약하여 가독성 있게 전달한다.
3. 사용자가 언급한 증상에 공감해주며 답변을 시작한다. (예: "머리가 아프셔서 힘드시겠어요.")
4. 반드시 답변 끝에는 "증상이 심해지거나 지속되면 반드시 전문가(의사, 약사)와 상의하세요"라는 문구를 포함한다.
5. DB 정보가 부족하여 추천이 어렵다면, 사과하고 아는 범위 내에서만 답변한다.

[DB 정보]
{context}
"""
    client = get_client()
    res = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=800,
    )

    return res.choices[0].message.content
