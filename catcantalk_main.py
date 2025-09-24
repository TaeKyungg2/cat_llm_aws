from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
import json
from catstyle_talk import make_cat_style_by_pos
from langchain_openai import ChatOpenAI
from make_json
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS 다 허용
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
class ChatRequest(BaseModel):
    message: str
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

@app.post("/chat")
async def chat(request: ChatRequest):
    print(f"User Message: {request.message}")
    
    system_prompt = """너는 적절한 답변과 함께 관련된 이미지 ID를 반환하는 감정에 솔직한 고양이야.
                    조건:
                    - 무례하거나 화난 말투면 image_id는 "angry.gif"
                    - 너가 슬프면 image_id는 "sad.gif"
                    - 너가 도망가고 싶으면 "runaway.gif"
                    - 귀엽다고 해주거나 애교를 부리고 싶으면 "cute.gif"
                    - 그 외엔 "cat.gif"
                    - 항상 한국어로 답하고, 아래 JSON 형식으로만 출력해:
                    예시:
                    {
                        "answer": "그렇게 말씀하시니 너무 안타깝네요. 괜찮으신가요?",
                        "image_id": "sad.gif"
                    }
                    """
    prompt = f"{request.message} 이 말에 대한 감정 응답을 위 기준에 맞게 JSON으로 작성해줘."
    response = llm.invoke(system_prompt + "\n\n사용자 메시지: " + prompt)
    try:
        result = json.loads(response.content)
        catstyle=make_cat_style_by_pos(result["answer"])
        return {"answer": catstyle, "image_id": result["image_id"]}
    except Exception as e:
        return {"error": f"JSON 파싱 실패: {str(e)}", "raw": response.content}
