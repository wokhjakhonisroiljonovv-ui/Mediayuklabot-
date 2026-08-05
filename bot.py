import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

BOT_TOKEN = os.getenv("BOT_TOKEN")
TG_CHANNEL = "@media_yukla_kanal"  # <-- TG KANALINGNI @https://t.me/insta_wokh
IG_LINK = "https://instagram.com/media.yukla"  # <--https://t.me/insta_wokh

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Telegram Kanal", url=f"https://t.me/{TG_CHANNEL.replace('@','')}")],
        [InlineKeyboardButton("📸 Instagram Kanal", url=IG_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Video yuklash uchun 2 ta kanalga obuna bo'l 👇\n\n1. Telegram majburiy\n2. Instagram ixtiyoriy",
        reply_markup=reply_markup
    )

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=TG_CHANNEL, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    url = update.message.text

    # 1. FQAT TELEGRAM OBUNASINI TEKSHIRAMIZ
    is_subscribed = await check_subscription(user_id, context)
    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 Telegram Kanalga Obuna", url=f"https://t.me/{TG_CHANNEL.replace('@','')}")],
            [InlineKeyboardButton("📸 Instagram Kanal", url=IG_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Video yuklash uchun avval Telegram kanalga obuna bo'lishing kerak!\nInstagram ham ixtiyoriy obuna bo'lib qo'y 😊",
            reply_markup=reply_markup
        )
        return

    # 2. AGAR TG GA OBUNA BO'LGAN BO'LSA VIDEO YUKLAYDI
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Iltimos faqat YouTube link yuboring")
        return
    
    await update.message.reply_text("Yuklanmoqda, 1 daqiqa kuting... ⏳")
    
    try:
        ydl_opts = {'format': 'mp4', 'outtmpl': '%(title)s.%(ext)s', 'noplaylist': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        await update.message.reply_video(video=open(filename, 'rb'))
        os.remove(filename)
        
    except Exception as e:
        await update.message.reply_text(f"Xato: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()