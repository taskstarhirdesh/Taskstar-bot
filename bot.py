import os
import json
import firebase_admin

from firebase_admin import credentials, db
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters
)

CHANNEL_USERNAME = "@TaskStarRewards"
VIDEO_PRICE = 250


# FIREBASE

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


# START

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🎬 Unlock Video - 250 Stars",
                callback_data="buy_video"
            )
        ]
    ]

    await update.message.reply_text(
        "Welcome to TaskStar!\n\n"
        "Use /tasks to view available tasks.\n\n"
        "Unlock the video for 250 Telegram Stars.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# TASKS

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "Join TaskStar Rewards Channel",
                url="https://t.me/TaskStarRewards"
            )
        ],
        [
            InlineKeyboardButton(
                "Check Task",
                callback_data="check_task_1"
            )
        ]
    ]

    await update.message.reply_text(
        "Task #1\n\n"
        "Join our TaskStar Rewards channel.\n\n"
        "After joining, click Check Task.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# CHECK TASK

async def check_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = str(query.from_user.id)

    await query.answer()

    task_ref = db.reference(
        f"TaskStar/users/{user_id}/task_1"
    )

    if task_ref.get():

        await query.message.reply_text(
            "You already completed this task."
        )

        return

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
                "Task Completed!\n\n"
                "Your completion has been saved."
            )

        else:

            await query.message.reply_text(
                "Please join the channel first."
            )

    except Exception as e:

        print(e)

        await query.message.reply_text(
            "Please join the channel first."
        )


# BUY VIDEO

async def buy_video(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = str(query.from_user.id)

    await query.answer()

    purchase_ref = db.reference(
        f"TaskStar/users/{user_id}/video_unlocked"
    )

    if purchase_ref.get():

        await query.message.reply_text(
            "You already unlocked this video!"
        )

        return

    prices = [
        LabeledPrice(
            "Video Unlock",
            VIDEO_PRICE
        )
    ]

    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title="Unlock Video",
        description="Unlock this video for 250 Telegram Stars.",
        payload="video_unlock_250",
        currency="XTR",
        prices=prices
    )


# PRE CHECKOUT

async def pre_checkout(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.pre_checkout_query

    if query.invoice_payload == "video_unlock_250":

        await query.answer(ok=True)

    else:

        await query.answer(
            ok=False,
            error_message="Payment error."
        )


# SUCCESSFUL PAYMENT

async def successful_payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    payment = update.message.successful_payment
    user_id = str(update.effective_user.id)

    if (
        payment.currency == "XTR"
        and payment.total_amount == VIDEO_PRICE
    ):

        purchase_ref = db.reference(
            f"TaskStar/users/{user_id}/video_unlocked"
        )

        purchase_ref.set(True)

        await update.message.reply_text(
            "Payment Successful!\n\n"
            "Your video has been unlocked."
        )


# MAIN

def main():

    token = os.getenv("BOT_TOKEN", "").strip()

    if not token:

        print("BOT_TOKEN is not set!")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("tasks", tasks))

    app.add_handler(
        CallbackQueryHandler(
            check_task,
            pattern="check_task_1"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            buy_video,
            pattern="buy_video"
        )
    )

    app.add_handler(
        PreCheckoutQueryHandler(pre_checkout)
    )

    app.add_handler(
        MessageHandler(
            filters.SUCCESSFUL_PAYMENT,
            successful_payment
        )
    )

    print("TaskStar Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
