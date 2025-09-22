import os, logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
import openai

BOT_TOKEN = os.getenv("BOT_TOKEN", "8349267043:AAG1buzO50UhIWdi3qxT8iUNM51LagC-dRQ")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-abcdef1234567890abcdef1234567890abcdef12")
openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ask_openai(prompt: str) -> str:
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content": prompt}],
            max_tokens=400
        )
        return resp['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.exception("OpenAI error")
        return "Maaf, tidak dapat menghubungi layanan jawaban sekarang."

def on_message(update: Update, context: CallbackContext):
    text = update.message.text or ""
    reply = ask_openai(text[:1000])
    update.message.reply_text(reply)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot cerdas siap menjawab. (Perhatian: pakai OpenAI API — berbayar)")

def main():
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN hilang")
    if not OPENAI_API_KEY:
        raise SystemExit("OPENAI_API_KEY hilang")
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), on_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
