
import telebot
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WC_URL = os.getenv("WC_URL")
WC_KEY = os.getenv("WC_KEY")
WC_SECRET = os.getenv("WC_SECRET")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

bot = telebot.TeleBot(BOT_TOKEN)

def search_product(query):
    url = f"{WC_URL}/wp-json/wc/v3/products"
    params = {"search": query}
    auth = (WC_KEY, WC_SECRET)
    r = requests.get(url, params=params, auth=auth)
    return r.json()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! نام قطعه‌ای که دنبالشی رو بنویس تا قیمتش رو بهت بگم.")

@bot.message_handler(func=lambda message: True)
def handle_search(message):
    results = search_product(message.text)
    if results:
        for p in results[:1]:
            msg = f"🔧 نام: {p['name']}
💵 قیمت: {p['price']} تومان
📎 لینک: {p['permalink']}"
            bot.send_message(message.chat.id, msg)
    else:
        btn = telebot.types.InlineKeyboardMarkup()
        btn.add(telebot.types.InlineKeyboardButton("🧑‍💼 پشتیبان فروش", url=f"https://t.me/{ADMIN_USERNAME}"))
        bot.send_message(message.chat.id, "قطعه موردنظر پیدا نشد. لطفاً با پشتیبان در تماس باش.", reply_markup=btn)

bot.infinity_polling()
