import os, logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from telegram import Bot

load_dotenv()                              # pulls TG_TOKEN from .env
TG_TOKEN = os.getenv("TG_TOKEN")
bot       = Bot(TG_TOKEN)

app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    chat_id = data["message"]["chat"]["id"]
    text    = data["message"].get("text", "")
    # Echo for now
    await bot.send_message(chat_id, f"✅ Got: {text}")
    return {"ok": True}

@app.get("/")                              # simple health check
async def root():
    return {"status": "up"}
