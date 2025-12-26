from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from research_agent.core import Agent

load_dotenv()

app = FastAPI(title="Research agent API")

SYSTEM_PROMPT = """
You are a helpful Research Assistant. 
Always verify with a web search. Be concise.
"""
agent = Agent(system_prompt=SYSTEM_PROMPT)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def health_check():
    """Simple health check to see if everything is running"""
    return {"status": "ok", "message": "Research agent is ready"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Send the message to the agent and get a response
    """

    try:
        user_message = request.message

        agent_response = agent.run(user_message)

        return ChatResponse(response=agent_response or "")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

