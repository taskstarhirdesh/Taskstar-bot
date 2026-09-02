import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


CHANNEL_USERNAME = "@TaskStarRewards"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⭐ Welcome to TaskStar!\n\nUse /tasks to view available tasks."
    )


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Join TaskStar Rewards Channel",
                url="https://t.me/TaskStarRewards"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎯 Task #1\n\n📢 Join our TaskStar Rewards channel.",
        reply_markup=reply_markup
    )


def main():
    token = os.getenv("BOT_TOKEN", "").strip()

    if not token:
        print("BOT_TOKEN is not set!")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tasks", tasks))

    print("TaskStar Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
