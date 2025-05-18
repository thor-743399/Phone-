
import logging
import phonenumbers
from phonenumbers import carrier, geocoder
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(level=logging.INFO)

# ✅ Only authorized Telegram user IDs
ADMIN_IDS = [2128531830]  # Narendra

# 🔐 Your bot token
BOT_TOKEN = "7216203077:AAFzoENt4Pg3_jqY01TD7oW4u-5yJ7Ii-9Q"

# Phone info function
def get_phone_info(phonenumber: str) -> str:
    try:
        if not phonenumber.isdigit():
            return "❗ Enter digits only (without '+' or spaces)."
        parsed_number = phonenumbers.parse("+" + phonenumber)
        provider = carrier.name_for_number(parsed_number, 'en')
        location = geocoder.description_for_number(parsed_number, 'en')
        return (
            f"📞 Number: {parsed_number.national_number}\n"
            f"🌍 Location: {location}\n"
            f"📡 Carrier: {provider}"
        )
    except phonenumbers.NumberParseException as e:
        return f"❌ Error: {e}"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access Denied.\nOnly authorized users can use this bot.")
        return
    await update.message.reply_text("👋 Welcome Narendra! Send a phone number (without `+`) to get details.")

# Handle any message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access Denied.\nYou are not authorized to use this bot.")
        return

    phone = update.message.text.strip()
    info = get_phone_info(phone)
    await update.message.reply_text(info)

# Main runner
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot is running (Admin access only).")
    app.run_polling()

if __name__ == '__main__':
    main()
