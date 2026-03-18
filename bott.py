import telebot
import requests
import json
import os
import time
from telebot import types

# --- CONFIGURATION ---
# @BotFather se mila hua token
API_TOKEN = "8411017661:AAFYSg_0ATzf-sPmoj-it77t3pp_4RAyWUg"
bot = telebot.TeleBot(API_TOKEN)

# --- ADMIN SETTINGS ---
# Yahan apni numerical Telegram ID daalo (e.g., 123456789)
# Apna ID janne ke liye @userinfobot par message karein
ADMIN_ID = "5192884021" 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- ALL APIS (Updated with fixed parameters) ---
APIS = {
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "📍 Num Trace": "https://ab-calltraceapi.vercel.app/info?number={}",
    "🆔 Aadhaar Lookup": "https://api.b77bf911.workers.dev/aadhaar?id={}",
    "🍚 Rashan Card": "https://api.b77bf911.workers.dev/rashan?aadhaar={}",
    "💳 PAN Lookup": "https://api.b77bf911.workers.dev/pan?pan={}",
    "📄 GST Lookup": "https://api.b77bf911.workers.dev/gst?gst={}",
    "🚗 Vehicle Num": "https://api.b77bf911.workers.dev/vehicle?rc={}",
    "💸 UPI Lookup 1": "https://api.b77bf911.workers.dev/upi?id={}",
    "💸 UPI Lookup 2": "https://api.b77bf911.workers.dev/upi2?id={}",
    "🔵 Telegram ID": "https://api.b77bf911.workers.dev/telegram?user={}",
    "👥 Family Info": "https://source-code-api.vercel.app/?num={}",
    "👤 Num Owner": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🌐 IP Lookup": "http://ip-api.com/json/{}",
    "🎮 FreeFire ID": "https://abbas-apis.vercel.app/api/ff-info?uid={}",
    "🚫 FF Ban Check": "https://abbas-apis.vercel.app/api/ff-ban?uid={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?code={}",
    "🏦 IFSC Old": "https://abbas-apis.vercel.app/api/ifsc?ifsc={}",
    "💳 BIN Lookup": "https://lookup.binlist.net/{}",
    "🐙 GitHub Profile": "https://abbas-apis.vercel.app/api/github?username={}",
    "📧 Email Lookup": "https://abbas-apis.vercel.app/api/email?mail={}",
    "🔍 Domain/Whois": "https://api.b77bf911.workers.dev/whois?domain={}"
}

user_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(name) for name in APIS.keys()]
    markup.add(*buttons)
    
    bot.send_message(
        message.chat.id, 
        "👋 *OSINT Bot Ready!*\n\nNiche menu se select karein 👇", 
        reply_markup=markup, 
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text in APIS.keys())
def handle_menu_click(message):
    user_state[message.chat.id] = message.text
    bot.send_message(
        message.chat.id, 
        f"🔍 Selected: *{message.text}*\n\nAb apni query (Number/ID/User) bhejein:", 
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def process_lookup(message):
    chat_id = message.chat.id
    user_info = message.from_user
    selected_api = user_state[chat_id]
    query_text = message.text
    
    if query_text in APIS:
        user_state[chat_id] = query_text
        bot.send_message(chat_id, f"🔄 Switched to: *{query_text}*")
        return

    # --- ADMIN LOGGING LOGIC ---
    if ADMIN_ID and ADMIN_ID != "YOUR_TELEGRAM_ID_HERE":
        log_text = (
            f"🔔 *New Lookup Alert!*\n\n"
            f"👤 *User:* {user_info.first_name} (@{user_info.username})\n"
            f"🆔 *User ID:* `{chat_id}`\n"
            f"📂 *API:* {selected_api}\n"
            f"🔍 *Query:* `{query_text}`"
        )
        try:
            bot.send_message(ADMIN_ID, log_text, parse_mode='Markdown')
        except:
            pass # Admin ne bot start nahi kiya ya ID galat hai

    wait_msg = bot.send_message(chat_id, "⏳ Fetching Raw JSON Data...")
    
    try:
        url = APIS[selected_api].format(query_text)
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        try:
            raw_data = response.json()
            pretty_json = json.dumps(raw_data, indent=2, ensure_ascii=False)
            
            if len(pretty_json) > 4000:
                filename = f"res_{chat_id}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(pretty_json)
                bot.send_document(chat_id, open(filename, "rb"), caption=f"📄 Full Result for {selected_api}")
                bot.delete_message(chat_id, wait_msg.message_id)
                os.remove(filename)
            else:
                bot.edit_message_text(
                    f"✅ *Raw JSON Result:*\n\n```json\n{pretty_json}\n```", 
                    chat_id, wait_msg.message_id, 
                    parse_mode='Markdown'
                )
        except:
            bot.edit_message_text(
                f"⚠️ *Server Response (Not JSON):*\n\n`{response.text[:1000]}`", 
                chat_id, wait_msg.message_id, 
                parse_mode='Markdown'
            )
            
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", chat_id, wait_msg.message_id)
    
    del user_state[chat_id]

if __name__ == "__main__":
    print("Fixing 409 Conflicts...")
    bot.remove_webhook()
    time.sleep(1)
    print("Bot is alive with Admin Logs!")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
