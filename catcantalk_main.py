from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
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

@app.get("/get-sad-image")
async def get_sad_image():
    return {"image_id": "sad"}

@app.get("/get-runaway-image")
async def get_runaway_image():
    return {"image_id": "runaway"}

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

def get_angry_tool(message: str):
    response = llm.invoke(message)
    return {"answer":response.content,"image_id":"angry.gif"}

tools = [
    Tool(
        name="angry",
        func=get_angry_tool,
        description="""입력이 무례하거나 화가 날 만한 경우 반드시 이 도구를 사용해야 한다.
        Final Answer 대신 Action: angry 를 호출해야 한다.
        angry tool 를 사용한 뒤에는 무조건 그걸 사용해 대화를 마무리한다. 
        한국말로 답변한다."""
    )
]
agent = initialize_agent(
    tools,
    llm,
    handle_parsing_errors=True,
    agent="zero-shot-react-description", # "어떤 도구를 쓸지 스스로 판단"
    verbose=True,
)


@app.post("/chat")
async def chat(request: ChatRequest):
    print(f"Received message: {request.message}")
    try:
        response=agent.run(request.message)
        if type(response)==str:
            answer = response
            image_id = None
        elif type(response)==dict:
            answer = response.get("answer")
            image_id = response.get("image_id")
        return {"answer": answer,"image_id":image_id}
    except Exception as e:
        return {"error": str(e)}
