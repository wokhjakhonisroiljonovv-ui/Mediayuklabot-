import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from pytubefix import YouTube
from yt_dlp import YoutubeDL

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Menga YouTube link tashla, men video yuklab beraman 🎬")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Iltimos faqat YouTube link yuboring")
        return
    
    await update.message.reply_text("Yuklanmoqda, 1 daqiqa kuting... ⏳")
    
    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
        }
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
