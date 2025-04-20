# app.py  (replace the whole handler block)
from fastapi import FastAPI, Request
from telegram import Bot

app = FastAPI()
bot = Bot(os.getenv("TG_TOKEN"))

@app.post("/webhook")
async def telegram_webhook(req: Request):
    update = await req.json()

    # Accept either message or edited_message; ignore others
    message = update.get("message") or update.get("edited_message")
    if not message or "text" not in message:
        return {"ok": True}        # skip non‑text updates

    chat_id = message["chat"]["id"]
    text    = message["text"]

    await bot.send_message(chat_id, f"✅ Got: {text}")
    return {"ok": True}
