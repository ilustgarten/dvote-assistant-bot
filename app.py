from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# app.py  (replace the whole handler block)
from fastapi import FastAPI, Request
from telegram import Bot

app = FastAPI()
bot = Bot(os.getenv("TG_TOKEN"))

@app.post("/webhook")
async def telegram_webhook(req: Request):
    update = await req.json()

    message = update.get("message") or update.get("edited_message")
    if not message or "text" not in message:
        return {"ok": True}

    chat_id = str(message["chat"]["id"])  # cast to string for safety
    text = message["text"]

    # Store the message as a new "task" in the DB
    supabase.table("task").insert({
        "chat_id": chat_id,
        "text": text,
        "status": "pending"
    }).execute()

    await bot.send_message(chat_id, f"📝 Task saved: {text}")
    return {"ok": True}
