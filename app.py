from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from supabase import create_client, Client
import os
import logging

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Telegram Handlers
async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm your D'Vote Assistant.")

async def handle_message(update: Update, context):
    text = update.message.text
    await update.message.reply_text(f"Got: {text}")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}

@app.on_event("startup")
async def startup():
    # Needed to initialize the telegram bot in async mode
    await telegram_app.initialize()

