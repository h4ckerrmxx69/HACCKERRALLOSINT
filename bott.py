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

# --- ALL APIS IN ONE PLACE ---
APIS = {
    # H4CKERR MX SPECIALS
    "📸 Insta Lookup": "https://allnew.proportalxc.workers.dev/instagram?username={}",
    "🔍 GST Lookup": "https://paid.proportalxc.workers.dev/gst?gst={}",
    "📍 Pincode Search": "https://paid.proportalxc.workers.dev/pincode?pincode={}",
    "🌐 IP Detail": "https://paid.proportalxc.workers.dev/ip?ip={}",
    
    # NEW WORKER ENDPOINTS
    "💳 PAN Lookup": "https://api.b77bf911.workers.dev/pan?user={}",
    "🌾 Rashan Card": "https://api.b77bf911.workers.dev/rashan?aadhaar={}",
    "💸 UPI Lookup": "https://api.b77bf911.workers.dev/upi?user={}",
    "🏦 UPI V2": "https://api.b77bf911.workers.dev/upi2?user={}",
    "🚗 Vehicle V2": "https://api.b77bf911.workers.dev/v2?user={}",
    "📡 Telegram Info": "https://api.b77bf911.workers.dev/telegram?user={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?user={}",
    
    # FREE FIRE (NEW SERVER 203.57.85.58)
    "🎮 FF Player Info": "http://203.57.85.58:2005/player-info?uid={}",
    "🚫 FF Ban Check": "http://203.57.85.58:2005/bancheck?uid={}",
    "📊 FF Level Check": "http://203.57.85.58:2005/level?uid={}",
    "🌍 FF Region": "http://203.57.85.58:2005/region?uid={}",
    "🎁 FF Wishlist": "http://203.57.85.58:2005/wishlist?uid={}",
    "🔍 FF Name Search": "http://203.57.85.58:2005/search?name={}",
    "🎫 FF Token Decode": "http://203.57.85.58:2005/decode?token={}",
    
    # OSINT & UTILITY
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "📍 Num Trace": "https://ab-calltraceapi.vercel.app/info?number={}",
    "🇵🇰 Pak Phone": "https://abbas-apis.vercel.app/api/pakistan?number={}",
    "🆔 Aadhaar Lookup": "https://aadhar.ek4nsh.in/?name={}",
    "👤 Num Owner": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🚗 Vehicle Num": "https://new-vehicle-api-eosin.vercel.app/vehicle?rc={}",
    "📧 Email Lookup": "https://api.eva.pingutil.com/email?email={}",
    "🐙 GitHub Profile": "https://abbas-apis.vercel.app/api/github?username={}",
    "🔍 Domain/Whois": "https://api.hackertarget.com/whois/?q={}",
    "💳 BIN Lookup": "https://lookup.binlist.net/{}"
}

# --- EXAMPLES ---
EXAMPLES = {
    "📸 Insta Lookup": "Example: `physicswallah`",
    "🔍 GST Lookup": "Example: `07AAAAA0000A1Z5`",
    "💳 PAN Lookup": "Example: `ABCDE1234F`",
    "🌾 Rashan Card": "Example: `123456789012` (Aadhaar No)",
    "🎮 FF Player Info": "Example: `2919267964`",
    "📱 Phone Lookup": "Example: `91XXXXXXXXXX`"
}

user_state = {}
DEV_TAG = "\n\n━━━━━━━━━━━━━━━\n👤 **Developer:- @hackerrmx69**"

# Function to send large results without cutting
def send_long_message(chat_id, text):
    if len(text) <= 4096:
        bot.send_message(chat_id, text, parse_mode='Markdown')
    else:
        for i in range(0, len(text), 4000):
            bot.send_message(chat_id, text[i:i+4000])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(name) for name in APIS.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "💀 **H4CKERR MX Multi-Lookup V11.0**\nSaari APIs (25+) niche keyboard mein hain 👇", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in APIS.keys())
def handle_menu_click(message):
    user_state[message.chat.id] = message.text
    instruction = EXAMPLES.get(message.text, "Apni query enter karein:")
    bot.send_message(message.chat.id, f"🛠 **Tool:** {message.text}\n📝 **Instruction:** {instruction}", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def process_lookup(message):
    chat_id = message.chat.id
    selected_api = user_state[chat_id]
    query = message.text
    
    if query in APIS: # Safeguard for button clicks
        handle_menu_click(message)
        return

    # Admin Log
    try: bot.send_message(ADMIN_ID, f"📢 **Log:** {message.from_user.first_name}\n🛠 {selected_api}\n📝 `{query}`")
    except: pass

    wait = bot.send_message(chat_id, "⏳ Fetching Data...")
    del user_state[chat_id]

    try:
        url = APIS[selected_api].format(query)
        res = requests.get(url, headers=HEADERS, timeout=15)
        
        try:
            data = res.json()
            pretty = json.dumps(data, indent=2, ensure_ascii=False)
            bot.delete_message(chat_id, wait.message_id)
            send_long_message(chat_id, f"✅ **Result ({selected_api}):**\n```json\n{pretty}\n```\n{DEV_TAG}")
        except:
            bot.edit_message_text(f"⚠️ **Server Response:**\n`{res.text[:1000]}`{DEV_TAG}", chat_id, wait.message_id, parse_mode='Markdown')
    except:
        bot.edit_message_text(f"❌ Error: API Down ya Timeout ho gaya!{DEV_TAG}", chat_id, wait.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    print("H4CKERR MX V11.0 is LIVE with ALL APIs!")
    bot.remove_webhook()
    bot.infinity_polling()
    
