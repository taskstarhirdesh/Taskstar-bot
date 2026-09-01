import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⭐ Welcome to TaskStar!\n\nUse /tasks to view available tasks."
    )


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 Available tasks will appear here soon."
    )




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
