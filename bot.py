from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

TOKEN = "8283345987:AAGrFoP3tZHo1fRNvV5lFzToiaW7YO8PNzc"
CHANNEL_USERNAME = "@Hadyatulloh_YouTuber"

# USER STATUS
users = {}

# MENU
menu = [
    ["📞 Kontakt", "💼 Xizmatlar"],
    ["🌐 Tarmoqlar", "❓ Yordam"]
]
markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)

# LANGUAGE
language_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    ]
])

# SUBSCRIBE BUTTON
def subscribe_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Kanalga kirish", url="https://t.me/Hadyatulloh_YouTuber")],
        [InlineKeyboardButton("✅ Tasdiqlash", callback_data="check_sub")]
    ])

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Tilni tanlang:",
        reply_markup=language_keyboard
    )

# LANGUAGE SELECT
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    users[user_id] = {"lang": query.data, "subscribed": False}

    await query.message.reply_text(
        "📢 Kanalga obuna bo‘ling:",
        reply_markup=subscribe_button()
    )

# CHECK SUB
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if member.status in ["member", "administrator", "creator"]:
        users[user_id]["subscribed"] = True

        await query.message.reply_text(
            "✅ Tasdiqlandi!\n\nMenu:",
            reply_markup=markup
        )
    else:
        await query.message.reply_text("❌ Obuna bo‘ling!")

# MESSAGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # AGAR OBUNA BO'LMAGAN BO'LSA
    if user_id not in users or not users[user_id].get("subscribed"):
        await update.message.reply_text(
            "❗ Avval kanalga obuna bo‘ling",
            reply_markup=subscribe_button()
        )
        return

    # MENU
    if text == "📞 Kontakt":
        await update.message.reply_text("📞 @bahodirov_hadyatulloh")

    elif text == "💼 Xizmatlar":
        await update.message.reply_text(
            "💼 Xizmatlar:\n\n"
            "👉 Telegram bot yaratish\n"
            "👉 Website yaratish\n"
            "👉 Dasturlash yordam\n\n"
            "📢 https://t.me/Hadyatulloh_YouTuber"
        )

    elif text == "🌐 Tarmoqlar":
        await update.message.reply_text(
            "🌐 Tarmoqlar:\n\n"
            "📢 https://t.me/Hadyatulloh_YouTuber\n"
            "🎥 https://www.youtube.com/@Hadyatulloh_YouTuber\n"
            "📸 https://www.instagram.com/hadyatulloh.bahodirov"
        )

    elif text == "❓ Yordam":
        await update.message.reply_text("/start ni bosing")

    else:
        await update.message.reply_text("Iltimos tugmalardan foydalaning 👇")

# APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(language_handler, pattern="lang_"))
app.add_handler(CallbackQueryHandler(check_subscription, pattern="check_sub"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishlayapti 🚀")
app.run_polling()