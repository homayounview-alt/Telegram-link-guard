import os
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.environ["BOT_TOKEN"]

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message or not message.from_user:
        return

    # به پیام‌های مدیران گروه کاری نداشته باش
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        message.from_user.id
    )

    if member.status in ("administrator", "creator"):
        return

    # شناسایی لینک‌های متنی و لینک‌های مخفی
    has_link = bool(
        re.search(r"(https?://|www\.|t\.me/|telegram\.me/)", message.text or "", re.I)
        or re.search(r"(https?://|www\.|t\.me/|telegram\.me/)", message.caption or "", re.I)
        or any(
            entity.type in ("url", "text_link")
            for entity in (message.entities or []) + (message.caption_entities or [])
        )
    )

    if has_link:
        try:
            await message.delete()
        except Exception as e:
            print(f"Could not delete message: {e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.ChatType.GROUPS & ~filters.StatusUpdate.ALL,
        delete_links
    )
)

app.run_polling()
