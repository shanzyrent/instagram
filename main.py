from telegram import Update, Document
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from instagrapi import Client
import os
from config import BOT_TOKEN, TARGET_USERNAME

async def handle_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document and update.message.document.file_name.endswith(".txt"):
        file = await update.message.document.get_file()
        file_path = await file.download_to_drive()

        with open(file_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            combo = line.strip()
            if ":" in combo:
                username, password = combo.split(":", 1)
                cl = Client()
                try:
                    cl.login(username, password)
                    user_id = cl.user_id_from_username(TARGET_USERNAME)
                    cl.user_follow(user_id)
                    await update.message.reply_text(f"✅ {username}: Takip atıldı → {TARGET_USERNAME}")
                    cl.logout()
                except Exception as e:
                    await update.message.reply_text(f"❌ {username}: Hata – {str(e)}")
            else:
                await update.message.reply_text(f"⚠️ Geçersiz satır: {combo}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, handle_txt))
print("🚀 Bot çalışıyor...")
app.run_polling()
