import telebot
import requests
import json
import os
import time
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = "8411017661:AAFYSg_0ATzf-sPmoj-it77t3pp_4RAyWUg"
ADMIN_ID = 5192884021  # <--- Apni Numerical ID yahan daalein
bot = telebot.TeleBot(API_TOKEN)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- ALL APIS (OSINT + FF) ---
APIS = {
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "📍 Num Trace": "https://ab-calltraceapi.vercel.app/info?number={}",
    "🇵🇰 Pak Phone": "https://abbas-apis.vercel.app/api/pakistan?number={}",
    "🆔 Aadhaar Lookup": "https://aadhar.ek4nsh.in/?name={}",
    "👥 Family Info": "https://source-code-api.vercel.app/?num={}",
    "👤 Num Owner": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🚗 Vehicle Num": "https://new-vehicle-api-eosin.vercel.app/vehicle?rc={}",
    "🌐 IP Lookup": "http://ip-api.com/json/{}",
    "📧 Email Lookup": "https://api.eva.pingutil.com/email?email={}",
    "🎮 FF Player Info": "http://168.119.49.69:1132/player-info?uid={}",
    "🚫 FF Ban Check": "http://168.119.49.69:1132/bancheck?uid={}",
    "📊 FF Level Check": "http://168.119.49.69:1132/level?uid={}",
    "🌍 FF Region": "http://168.119.49.69:1132/region?uid={}",
    "🎁 FF Wishlist": "http://168.119.49.69:1132/wishlist?uid={}",
    "🔍 FF Name Search": "http://168.119.49.69:1132/search?name={}",
    "🎫 FF Token Decode": "http://168.119.49.69:1132/decode?token={}",
    "📅 FF Events": "http://168.119.49.69:1132/events?region={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?code={}",
    "💳 BIN Lookup": "https://lookup.binlist.net/{}",
    "🐙 GitHub Profile": "https://abbas-apis.vercel.app/api/github?username={}",
    "🔍 Domain/Whois": "https://api.b77bf911.workers.dev/whois?domain={}"
}

# --- EXAMPLES FOR EVERY TOOL ---
EXAMPLES = {
    "📱 Phone Lookup": "Example: `91XXXXXXXXXX`",
    "📍 Num Trace": "Example: `92XXXXXXXXXX` (With Country Code)",
    "🇵🇰 Pak Phone": "Example: `03XXXXXXXXX` (Pakistan Number)",
    "🆔 Aadhaar Lookup": "Example: `Full Name` (e.g., Rajesh Kumar)",
    "👥 Family Info": "Example: `91XXXXXXXXXX` (Target Number)",
    "👤 Num Owner": "Example: `91XXXXXXXXXX` (Truecaller Search)",
    "🚗 Vehicle Num": "Example: `DL10CE1234` (Vehicle Number)",
    "🌐 IP Lookup": "Example: `8.8.8.8` (IP Address)",
    "📧 Email Lookup": "Example: `test@gmail.com` (Email Address)",
    "🎮 FF Player Info": "Example: `2919267964` (Numeric UID)",
    "🚫 FF Ban Check": "Example: `2919267964` (Numeric UID)",
    "📊 FF Level Check": "Example: `2919267964` (Numeric UID)",
    "🌍 FF Region": "Example: `2919267964` (Numeric UID)",
    "🎁 FF Wishlist": "Example: `2919267964` (Numeric UID)",
    "🔍 FF Name Search": "Example: `yash` (Player Name)",
    "🎫 FF Token Decode": "Example: `eyJhbGci...` (JWT Token)",
    "📅 FF Events": "Example: `europe` or `indonesia` (Region)",
    "🏦 IFSC Lookup": "Example: `SBIN0001234` (IFSC Code)",
    "💳 BIN Lookup": "Example: `457173` (First 6 Digits)",
    "🐙 GitHub Profile": "Example: `torvalds` (Username)",
    "🔍 Domain/Whois": "Example: `google.com` (Domain)"
}

user_state = {}
DEV_TAG = "\n\n━━━━━━━━━━━━━━━\n👤 **Developer:- @hackerrmx69**"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(name) for name in APIS.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "🚀 **Multi-Lookup Bot Ready!**\n\nService select karein aur command follow karein 👇", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in APIS.keys())
def handle_menu_click(message):
    service = message.text
    user_state[message.chat.id] = service
    guide = EXAMPLES.get(service, "Apni query yahan type karein:")
    bot.send_message(message.chat.id, f"🛠 **Tool:** {service}\n📝 **Instruction:** {guide}", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def process_lookup(message):
    chat_id = message.chat.id
    user_info = message.from_user
    selected_api = user_state[chat_id]
    query_text = message.text
    
    if query_text in APIS:
        handle_menu_click(message)
        return

    # Logging to Admin
    try:
        log = f"📢 **User:** {user_info.first_name} (@{user_info.username})\n🛠 **Tool:** {selected_api}\n📝 **Query:** `{query_text}`"
        bot.send_message(ADMIN_ID, log, parse_mode='Markdown')
    except: pass

    wait_msg = bot.send_message(chat_id, "⏳ Data fetch ho raha hai...")
    del user_state[chat_id]

    try:
        url = APIS[selected_api].format(query_text)
        response = requests.get(url, headers=HEADERS, timeout=12)
        
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
            bot.edit_message_text(f"⚠️ **Response:** `{response.text[:1000]}`{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')
            
    except:
        bot.edit_message_text(f"❌ Error: API Timeout ya down hai!{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
