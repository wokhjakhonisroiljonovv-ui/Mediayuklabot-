import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

BOT_TOKEN = os.getenv("BOT_TOKEN")

# === SENING KANALLARING ===
TG_KANAL = "@insta_wokh"  
IG_SSILKA = "https://www.instagram.com/insta.shakkh"  
# ==========================

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=TG_KANAL, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def send_subscription_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Telegram Kanalga Obuna", url="https://t.me/insta_wokh")],
        [InlineKeyboardButton("📸 Instagram Kanalga Obuna", url=IG_SSILKA)],
        [InlineKeyboardButton("✅ Obuna Bo'ldim, Tekshir", callback_data="check_sub")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    matn = f"""⛔ Video yuklash uchun obuna shart!

1. 📢 Telegram kanalga MAJBURIY obuna
2. 📸 Instagram kanalga ixtiyoriy obuna

Obuna bo'lib pastdagi tugmani bos 👇"""
    
    await update.message.reply_text(matn, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Menga YouTube link yuboring 🎬\n\nEslatma: Video yuklashdan oldin kanallarga obuna bo'lish kerak")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
   