import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)


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
        ],
        [
            InlineKeyboardButton(
                "✅ Check Task",
                callback_data="check_task_1"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎯 Task #1\n\n"
        "📢 Join our TaskStar Rewards channel.\n\n"
        "After joining, click ✅ Check Task.",
        reply_markup=reply_markup
    )


async def check_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        if member.status in [
            "member",
            "administrator",
            "creator"
        ]:

            await query.message.reply_text(
                "🎉 Task Completed!\n\n"
                "You successfully joined the TaskStar Rewards channel. ✅"
            )

        else:

            await query.message.reply_text(
                "❌ Please join the channel first."
            )

    except Exception:

        await query.message.reply_text(
            "❌ Please join the channel first."
        )


def main():

    token = os.getenv("BOT_TOKEN", "").strip()

    if not token:
        print("BOT_TOKEN is not set!")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("tasks", tasks)
    )

    app.add_handler(
        CallbackQueryHandler(
            check_task,
            pattern="check_task_1"
        )
    )

    print("TaskStar Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
