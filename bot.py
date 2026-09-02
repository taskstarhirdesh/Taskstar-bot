import os
import json
import firebase_admin

from firebase_admin import credentials, db

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


# ---------------- FIREBASE ----------------

firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")

if not firebase_json:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT is not set!")

firebase_data = json.loads(firebase_json)

cred = credentials.Certificate(firebase_data)

firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://taskstar-b6d2e-default-rtdb.asia-southeast1.firebasedatabase.app/"
    }
)


# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "⭐ Welcome to TaskStar!\n\n"
        "Use /tasks to view available tasks."
    )


# ---------------- TASKS ----------------

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


# ---------------- CHECK TASK ----------------

async def check_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    user_id = str(query.from_user.id)

    await query.answer()


    # Check Firebase first

    task_ref = db.reference(
        f"TaskStar/users/{user_id}/task_1"
    )

    completed = task_ref.get()


    if completed:

        await query.message.reply_text(
            "⚠️ You already completed this task."
        )

        return


    # Check Telegram channel

    try:

        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=int(user_id)
        )

        if member.status in [
            "member",
            "administrator",
            "creator"
        ]:

            task_ref.set(True)

            await query.message.reply_text(
                "🎉 Task Completed!\n\n"
                "Your completion has been saved. ✅"
            )

        else:

            await query.message.reply_text(
                "❌ Please join the channel first."
            )


    except Exception:

        await query.message.reply_text(
            "❌ Please join the channel first."
        )


# ---------------- MAIN ----------------

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
