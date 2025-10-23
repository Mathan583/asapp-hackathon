from fastapi import FastAPI, Form
from app.chatbot import AirlineChatbot

app = FastAPI()
bot = AirlineChatbot()

@app.post("/chat")
async def chat(message: str = Form(...)):
    response = bot.get_response(message)
    return {"response": response}
