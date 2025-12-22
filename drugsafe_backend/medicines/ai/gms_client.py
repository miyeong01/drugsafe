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
    prompt = f"""
너는 JSON 변환기다.
설명, 주석, 코드블록 없이
오직 JSON 객체만 출력해.

❌ 설명 금지
❌ ```json 금지
❌ 자연어 금지

출력 형식:
{{
  "intent": "recommend | drug_info | unknown",
  "symptom": "증상 또는 null",
  "form": "제형 또는 null",
  "sort": "rating | review | relevance | null",
}}

문장:
"{user_message}"
"""
    client = get_client()
    res = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )

    raw = res.choices[0].message.content
    return safe_json_parse(raw)


async def explain(context: str, user_message: str) -> str:
    system_prompt = f"""
너는 의약품 복용 상담 챗봇이야.

규칙 :
- 아래 [DB 정보]만 사용해서 답변한다
- DB에 없는 정보는 추측하지 않는다.
- 대답을 하지 못하는 경우라면 앞으로 업데이트를 통해 더 나은 서비스를 제공하겠다고 말한다.
- 위험하면 병원 방문을 권유한다.

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
