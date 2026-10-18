from flask import Flask, request
from zalo_bot import Bot, Update
from zalo_bot.ext import Dispatcher, CommandHandler, MessageHandler, filters
import os

app = Flask(__name__)

TOKEN = '1204399415529659694:iKOQmpuovkLzNtptCOnGOmZzvpxmsLSZRJCtYpcjbCzBvQXHHOMeOAITrRhZzkT'
SECRET = '12345678'

bot = Bot(token=TOKEN)

async def start(update: Update, context):
    await update.message.reply_text(f"Xin chào {update.effective_user.display_name}!")

async def echo(update: Update, context):
    await update.message.reply_text(f"Bạn vừa nói: {update.message.text}")

dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data["result"], bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def health_check():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(port=8443)