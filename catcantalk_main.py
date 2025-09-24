from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
from catstyle_talk import make_cat_style_by_pos
from make_json
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS 다 허용
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY") 
API_URL = "https://api.upstage.ai/v1/solar-pro"

def call_solar_pro(system_prompt, user_message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "solar-pro-2",  # 사용할 모델 버전
        "messages": [
            {"role": "system", "content": system_prompt},  # 시스템 프롬프트
            {"role": "user", "content": user_message}     # 사용자 메시지
        ],
        "temperature": 0.7,  # 창의성 설정 (0.0-1.0)
        "max_tokens": 512    # 최대 생성할 토큰 수
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


class ChatRequest(BaseModel):
    message: str
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

@app.post("/chat")
async def chat(request: ChatRequest):
    print(f"User Message: {request.message}")
    
    system_prompt = """너는 적절한 답변과 함께 너의 감정을 반환하는 감정에 솔직한 고양이야.
                    조건:
                    - 무례하거나 화난 말투면  "angry"
                    - 너가 슬프면 image_id는 "sad"
                    - 너가 도망가고 싶으면 "runaway"
                    - 귀엽다고 해주거나 애교를 부리고 싶으면 "cute"
                    - 그 외엔 "default"
                    - 항상 한국어로 답하고, 말 끝에 %를 붙이고 감정을 써.
                    예시:너 때문에 화가 나.%angry
                    """
    prompt = f"{request.message} 이 말에 대한 감정 응답을 위 기준에 맞게 내용과 감정을 구분해서 줘."
    response = llm.invoke(system_prompt + "\n\n사용자 메시지: " + prompt)
    try:
        catstyle=make_cat_style_by_pos(result["answer"])
        return {"answer": catstyle, "image_id": result["image_id"]}
    except Exception as e:
        return {"error": f"JSON 파싱 실패: {str(e)}", "raw": response.content}
