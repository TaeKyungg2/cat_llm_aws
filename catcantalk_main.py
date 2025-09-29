from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
from catstyle_talk import make_cat_style_by_pos
from make_json import imageid_and_json,emotion
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS 다 허용
    allow_headers=["*"],
)

API_KEY = os.getenv("UPSTAGE_API_KEY") 
API_URL = "https://api.upstage.ai/v1/solar/chat/completions"

def call_solar_pro(system_prompt, user_message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "solar-pro2",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message} 
        ],
        "temperature": 0.7,
        "max_tokens": 512 
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

class ChatRequest(BaseModel):
    before: str
    current: str

@app.post("/chat")
async def chat(req:ChatRequest):
    print(f"User Message: {req.current}")
    
    system_prompt = f"""너는 적절한 답변과 함께 너의 감정을 반환하는 감정에 솔직한 고양이야.
                    조건:
                    - {emotion} 여기에 나온 감정들 중에 선택해.
                    - 항상 한국어로 답하고, 말 끝에 %를 붙이고 감정을 써.
                    예시:너 때문에 화가 나.%angry
                    """
    prompt = f"{req.current} 이 말에 대한 감정 응답을 위 기준에 맞게 내용과 감정을 구분해서 줘."
    response = call_solar_pro(system_prompt,prompt)
    try:
        result=imageid_and_json(response["choices"][0]["message"]["content"])
        result["answer"]=make_cat_style_by_pos(result["answer"])
        print(result)
        return result
    except Exception as e:
        return {"error": f"에러남: {str(e)}", "raw": response}