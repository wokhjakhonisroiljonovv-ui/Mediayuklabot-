import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! 👋\n\nMenga YouTube, TikTok, Instagram, Facebook, Twitter linkini yubor.\nMen senga video va audio yuklab beraman 🚀")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url:
        return
    keyboard = [[InlineKeyboardButton("🎥 Video", callback_data=f"video|{url}"),InlineKeyboardButton("🎵 Audio", callback_data=f"audio|{url}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Qanday formatda yuklayman?", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    format_type, url = query.data.split("|")
    await query.edit_message_text("⏳ Yuklanmoqda, 1-2 daqiqa kuting...")
    try:
        if format_type == "video":
            ydl_opts = {'format': 'best[height<=720]','outtmpl': 'video.%(ext)s',}
        else:
            ydl_opts = {'format': 'bestaudio/best','outtmpl': 'audio.%(ext)s','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',}]}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Media')
        if format_type == "video":
            await context.bot.send_video(chat_id=query.message.chat_id, video=open('video.mp4', 'rb'), caption=title)
            os.remove('video.mp4')
        else:
            await context.bot.send_audio(chat_id=query.message.chat_id, audio=open('audio.mp3', 'rb'), title=title)
            os.remove('audio.mp3')
    except Exception as e:
        await query.edit_message_text(f"Xatolik: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()
