from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.environ.get('TOKEN')
BOT_USERNAME = os.environ.get('BOT_USERNAME')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
GOOGLE_API_KEY= os.environ.get('GOOGLE_API_KEY')

app = FastAPI()

# Define your bot commands and handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am a Python bot. Please type something so I can respond!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Echo: {update.message.text}")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Initialize the bot application
bot_app = Application.builder().token(TOKEN).build()

# Register command handlers
bot_app.add_handler(CommandHandler('start', start_command))
bot_app.add_handler(CommandHandler('help', help_command))
bot_app.add_handler(CommandHandler('custom', custom_command))

# Register message handler
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Register error handler
bot_app.add_error_handler(error)

@app.get("/")
async def root():
    return {"message": "Service is live! Visit the bot at https://t.me/researchA_bot"}

@app.head("/")
async def root_head():
    return {"message": "HEAD requests are allowed."}

@app.get("/webhook")
async def get_webhook():
    return {"message": "This is the webhook endpoint. Please use POST requests to send updates."}

@app.post('/webhook')
async def webhook_handler(request: Request):
    update = await request.json()
    update = Update.de_json(update, bot_app.bot)
    await bot_app.process_update(update)
    return 'OK'

@app.on_event("startup")
async def on_startup():
    # Initialize the bot application
    await bot_app.initialize()
    
    # Set the webhook for the bot
    await bot_app.bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot_app.shutdown()
