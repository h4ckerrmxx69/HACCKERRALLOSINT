import telebot
import requests
import json
import os
import time
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = "8411017661:AAFYSg_0ATzf-sPmoj-it77t3pp_4RAyWUg"
ADMIN_ID = 5192884021  # <--- Apni ID check kar lena
bot = telebot.TeleBot(API_TOKEN)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- ALL APIS (FF APIs with &key=@yashapis FIXED) ---
APIS = {
    # FREE FIRE (NEW SERVER + AUTH KEY)
    "🎮 FF Player Info": "http://203.57.85.58:2005/player-info?uid={}&key=@yashapis",
    "🚫 FF Ban Check": "http://203.57.85.58:2005/bancheck?uid={}&key=@yashapis",
    "📊 FF Level Check": "http://203.57.85.58:2005/level?uid={}&key=@yashapis",
    "🌍 FF Region": "http://203.57.85.58:2005/region?uid={}&key=@yashapis",
    "🎁 FF Wishlist": "http://203.57.85.58:2005/wishlist?uid={}&key=@yashapis",
    "🔍 FF Name Search": "http://203.57.85.58:2005/search?name={}&key=@yashapis",
    "🎫 FF Token Decode": "http://203.57.85.58:2005/decode?token={}&key=@yashapis",
    "📅 FF Events": "http://203.57.85.58:2005/events?region={}&key=@yashapis",

    # H4CKERR MX SPECIALS
    "📸 Insta Lookup": "https://allnew.proportalxc.workers.dev/instagram?username={}",
    "🔍 GST Lookup": "https://paid.proportalxc.workers.dev/gst?gst={}",
    "📍 Pincode Search": "https://paid.proportalxc.workers.dev/pincode?pincode={}",
    "🌐 IP Detail": "https://paid.proportalxc.workers.dev/ip?ip={}",
    
    # WORKER ENDPOINTS
    "🚗 Vehicle V2": "https://api.b77bf911.workers.dev/v2?query={}",
    "💳 PAN Lookup": "https://api.b77bf911.workers.dev/pan?user={}",
    "🌾 Rashan Card": "https://api.b77bf911.workers.dev/rashan?aadhaar={}",
    "💸 UPI Lookup": "https://api.b77bf911.workers.dev/upi?user={}",
    "📡 Telegram Info": "https://api.b77bf911.workers.dev/telegram?user={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?user={}",
    
    # OSINT
    "📱 Phone Lookup": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "📍 Num Trace": "https://ab-calltraceapi.vercel.app/info?number={}",
    "🇵🇰 Pak Phone": "https://abbas-apis.vercel.app/api/pakistan?number={}",
    "🆔 Aadhaar Lookup": "https://aadhar.ek4nsh.in/?name={}",
    "👤 Num Owner": "https://information-web-by-rose.vercel.app/api/search?mode=mobile&query={}",
    "🚗 Vehicle Num": "https://new-vehicle-api-eosin.vercel.app/vehicle?rc={}",
    "📧 Email Lookup": "https://api.eva.pingutil.com/email?email={}",
    "🔍 Domain/Whois": "https://api.hackertarget.com/whois/?q={}",
    "💳 BIN Lookup": "https://lookup.binlist.net/{}"
}

# --- ALL EXAMPLES ---
EXAMPLES = {
    "🎮 FF Player Info": "Example: `2919267964` (UID)",
    "🚫 FF Ban Check": "Example: `2919267964` (UID)",
    "📊 FF Level Check": "Example: `2919267964` (UID)",
    "🎫 FF Token Decode": "Example: `eyJhbGci...` (Full Token)",
    "🚗 Vehicle V2": "Example: `DL10CE1234` (RC No)",
    "🌾 Rashan Card": "Example: `123456789012` (Aadhar ID)",
    "📸 Insta Lookup": "Example: `physicswallah` (Username)",
    "🆔 Aadhaar Lookup": "Example: `Rajesh Kumar` (Name)"
}

user_state = {}
DEV_TAG = "\n\n━━━━━━━━━━━━━━━\n👤 **Developer:- @hackerrmx69**"

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
    bot.send_message(message.chat.id, "💀 **H4CKERR MX V14.0 - FF Keys Set!**\nAb saari APIs ekdum mast chalengi 👇", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in APIS.keys())
def handle_menu_click(message):
    user_state[message.chat.id] = message.text
    instruction = EXAMPLES.get(message.text, "Apni query enter karein:")
    bot.send_message(message.chat.id, f"🛠 **Tool:** {message.text}\n📝 **Instruction:** {instruction}", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def process_lookup(message):
    chat_id = message.chat.id
    user_info = message.from_user
    selected_api = user_state[chat_id]
    query = message.text
    
    if query in APIS:
        handle_menu_click(message)
        return

    # Admin Log
    try:
        log_text = (
            "📢 **Log**\n"
            f"👤 **User:** {user_info.first_name}\n"
            f"🛠 **Tool:** {selected_api}\n"
            f"📝 **Query:** `{query}`"
        )
        bot.send_message(ADMIN_ID, log_text, parse_mode='Markdown')
    except: pass

    wait = bot.send_message(chat_id, "⏳ Fetching Data from Server...")
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
        bot.edit_message_text(f"❌ Error: Server Down hai ya Authorization (Key) issue hai!{DEV_TAG}", chat_id, wait.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
