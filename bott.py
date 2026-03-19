import telebot
import requests
import json
import os
import time
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = "8411017661:AAFYSg_0ATzf-sPmoj-it77t3pp_4RAyWUg"
ADMIN_ID = 5192884021  # <--- Apni numerical ID yahan daal
bot = telebot.TeleBot(API_TOKEN)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- ALL APIS (OSINT + NEW FF SERVER) ---
APIS = {
    # --- OSINT LOOKUPS ---
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "📍 Num Trace": "https://ab-calltraceapi.vercel.app/info?number={}",
    "🇵🇰 Pak Phone": "https://abbas-apis.vercel.app/api/pakistan?number={}",
    "🆔 Aadhaar Lookup": "https://aadhar.ek4nsh.in/?name={}",
    "👥 Family Info": "https://source-code-api.vercel.app/?num={}",
    "👤 Num Owner": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🚗 Vehicle Num": "https://new-vehicle-api-eosin.vercel.app/vehicle?rc={}",
    "🌐 IP Lookup": "http://ip-api.com/json/{}",
    "📧 Email Lookup": "https://api.eva.pingutil.com/email?email={}",
    "🐙 GitHub Profile": "https://abbas-apis.vercel.app/api/github?username={}",
    "🔍 Domain/Whois": "https://api.b77bf911.workers.dev/whois?domain={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?code={}",
    "💳 BIN Lookup": "https://lookup.binlist.net/{}",

    # --- NEW FREE FIRE APIS (Server: 203.57.85.58:2005) ---
    "🎮 FF Player Info": "http://203.57.85.58:2005/player-info?uid={}",
    "🚫 FF Ban Check": "http://203.57.85.58:2005/bancheck?uid={}",
    "📊 FF Level Check": "http://203.57.85.58:2005/level?uid={}",
    "🌍 FF Region": "http://203.57.85.58:2005/region?uid={}",
    "🎁 FF Wishlist": "http://203.57.85.58:2005/wishlist?uid={}",
    "🔍 FF Name Search": "http://203.57.85.58:2005/search?name={}",
    "🎫 FF Token Decode": "http://203.57.85.58:2005/decode?token={}",
    "📅 FF Events": "http://203.57.85.58:2005/events?region={}"
}

# --- EXAMPLES FOR ALL TOOLS ---
EXAMPLES = {
    "📱 Phone Lookup": "Format: `91XXXXXXXXXX` (India No)",
    "📍 Num Trace": "Format: `92XXXXXXXXXX` (With CC)",
    "🇵🇰 Pak Phone": "Format: `03XXXXXXXXX` (Pak No)",
    "🆔 Aadhaar Lookup": "Format: `Rajesh Kumar` (Full Name)",
    "👥 Family Info": "Format: `91XXXXXXXXXX` (Mobile No)",
    "👤 Num Owner": "Format: `91XXXXXXXXXX` (Name/Owner)",
    "🚗 Vehicle Num": "Format: `DL10CE1234` (RC No)",
    "🌐 IP Lookup": "Format: `8.8.8.8` (IP Address)",
    "📧 Email Lookup": "Format: `user@gmail.com` (Email)",
    "🐙 GitHub Profile": "Format: `hacker` (Username)",
    "🔍 Domain/Whois": "Format: `google.com` (Domain)",
    "🏦 IFSC Lookup": "Format: `SBIN0001234` (IFSC)",
    "💳 BIN Lookup": "Format: `457173` (First 6 Digits)",
    "🎮 FF Player Info": "Format: `2919267964` (Numeric UID)",
    "🚫 FF Ban Check": "Format: `2919267964` (Numeric UID)",
    "📊 FF Level Check": "Format: `2919267964` (Numeric UID)",
    "🌍 FF Region": "Format: `2919267964` (Numeric UID)",
    "🎁 FF Wishlist": "Format: `2919267964` (Numeric UID)",
    "🔍 FF Name Search": "Format: `yash` (In-game Name)",
    "🎫 FF Token Decode": "Format: `eyJhbGci...` (JWT Token)",
    "📅 FF Events": "Format: `indonesia` (Region Name)"
}

user_state = {}
DEV_TAG = "\n\n━━━━━━━━━━━━━━━\n👤 **Developer:- @hackerrmx69**"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(name) for name in APIS.keys()]
    markup.add(*buttons)
    bot.send_message(
        message.chat.id, 
        "🔥 **Ultimate Multi-Lookup Bot Ready!**\n\nSaari APIs (OSINT + FF New Server) set hain.\nKoi bhi button select karein 👇", 
        reply_markup=markup, 
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text in APIS.keys())
def handle_menu_click(message):
    service = message.text
    user_state[message.chat.id] = service
    instruction = EXAMPLES.get(service, "Apni query niche bhejein:")
    bot.send_message(
        message.chat.id, 
        f"🛠 **Selected:** {service}\n📝 **Instruction:** {instruction}", 
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def process_lookup(message):
    chat_id = message.chat.id
    user_info = message.from_user
    selected_api = user_state[chat_id]
    query_text = message.text
    
    if query_text in APIS: # Menu change safeguard
        handle_menu_click(message)
        return

    # Admin Logging
    try:
        log = f"📢 **New Query**\n👤 **User:** {user_info.first_name} (@{user_info.username})\n🛠 **Tool:** {selected_api}\n📝 **Query:** `{query_text}`"
        bot.send_message(ADMIN_ID, log, parse_mode='Markdown')
    except: pass

    wait_msg = bot.send_message(chat_id, "⏳ Fetching Data from Server...")
    del user_state[chat_id]

    try:
        url = APIS[selected_api].format(query_text)
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        try:
            raw_data = response.json()
            pretty_json = json.dumps(raw_data, indent=2, ensure_ascii=False)
            
            if len(pretty_json) > 3800:
                filename = f"res_{chat_id}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(pretty_json)
                bot.send_document(chat_id, open(filename, "rb"), caption=f"📄 Result: {selected_api}{DEV_TAG}", parse_mode='Markdown')
                bot.delete_message(chat_id, wait_msg.message_id)
                os.remove(filename)
            else:
                bot.edit_message_text(f"✅ **Result:**\n```json\n{pretty_json}\n```\n{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')
        except:
            bot.edit_message_text(f"⚠️ **Server Response:**\n`{response.text[:1000]}`{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')
            
    except:
        bot.edit_message_text(f"❌ Error: API Server down hai ya query galat hai!{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot is Alive!")
    bot.infinity_polling()
