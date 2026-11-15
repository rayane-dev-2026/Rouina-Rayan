# بوت خدمة زبائن للمتاجر - تلغرام
# التثبيت:  pip install python-telegram-bot==21.6
# التشغيل:  python bot.py

import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters,
)

# ====== إعدادات المتجر (غيّرها لكل زبون) ======
BOT_TOKEN = os.getenv("BOT_TOKEN", "ضع_التوكن_هنا")  # من @BotFather
STORE_NAME = "متجر نجمة"
WELCOME = f"أهلاً بك في {STORE_NAME} 🌟\nكيف أستطيع مساعدتك؟"
PRODUCTS = "🛍 منتجاتنا:\n- منتج 1 — 1000 دج\n- منتج 2 — 2500 دج\n- منتج 3 — 4000 دج"
HOURS = "🕘 أوقات العمل: من السبت إلى الخميس، 9:00 صباحًا – 7:00 مساءً"
ADDRESS = "📍 العنوان: ضع عنوان المتجر هنا"
CONTACT = "📞 للتواصل: 0555 00 00 00"
ORDER = "🛒 لطلب منتج أرسل: اسمك، رقم هاتفك، المنتج، وعنوان التوصيل، وسنؤكد طلبك قريبًا."
OWNER_CHAT_ID = None  # ضع رقم حسابك (من @userinfobot) لتصلك الطلبات
# ===============================================

SECTIONS = {
    "products": PRODUCTS,
    "hours": HOURS,
    "address": ADDRESS,
    "contact": CONTACT,
    "order": ORDER,
}

KEYWORDS = {
    "products": ["سعر", "اسعار", "أسعار", "منتج", "منتجات", "كم"],
    "hours": ["وقت", "ساعات", "مفتوح", "دوام"],
    "address": ["عنوان", "فين", "اين", "أين", "موقع"],
    "contact": ["هاتف", "رقم", "اتصال", "واتساب"],
    "order": ["طلب", "اشتري", "شراء", "توصيل"],
}


def menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍 المنتجات والأسعار", callback_data="products")],
        [InlineKeyboardButton("🛒 اطلب الآن", callback_data="order")],
        [InlineKeyboardButton("🕘 أوقات العمل", callback_data="hours"),
         InlineKeyboardButton("📍 العنوان", callback_data="address")],
        [InlineKeyboardButton("📞 تواصل معنا", callback_data="contact")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, reply_markup=menu())


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text(SECTIONS[q.data], reply_markup=menu())


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # أرسل نسخة من الرسالة لصاحب المتجر إن كانت تبدو كطلب
    if OWNER_CHAT_ID and any(k in text for k in KEYWORDS["order"]):
        user = update.effective_user
        await context.bot.send_message(
            OWNER_CHAT_ID,
            f"📩 رسالة جديدة من {user.full_name} (@{user.username}):\n{text}",
        )

    for key, words in KEYWORDS.items():
        if any(w in text for w in words):
            await update.message.reply_text(SECTIONS[key], reply_markup=menu())
            return

    await update.message.reply_text(
        "لم أفهم سؤالك تمامًا، اختر من القائمة 👇", reply_markup=menu()
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    print("البوت يعمل...")
    app.run_polling()


if __name__ == "__main__":
    main()
