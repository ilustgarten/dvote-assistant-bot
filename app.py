import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from telegram import Bot
from supabase import create_client, Client

# Load environment variables
load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize clients
bot = Bot(TG_TOKEN)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "up"}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    update = await req.json()

    # Extract message (text only)
    message = update.get("message") or update.get("edited_message")
    if not message or "text" not in message:
        return {"ok": True}  # ignore non-text messages

    chat_id = str(message["chat"]["id"])
    text = message["text"]

    # Save task to Supabase
    supabase.table("task").insert({
        "chat_id": chat_id,
        "text": text,
        "status": "pending"
    }).execute()

    # Send confirmation
    await bot.send_message(chat_id, f"📝 Task saved: {text}")
    return {"ok": True}
