import telebot
import requests
import json
import os
import time
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = "8411017661:AAFYSg_0ATzf-sPmoj-it77t3pp_4RAyWUg"
ADMIN_ID = 5192884021  # <--- Apni Numerical ID yahan zaroor check kar lena
bot = telebot.TeleBot(API_TOKEN)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- ALL 28+ APIS (EVERY SINGLE ONE FIXED) ---
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

    # WORKER ENDPOINTS (FIXED PARAMETERS)
    "🚗 Vehicle V2": "https://api.b77bf911.workers.dev/v2?query={}",
    "💳 PAN Lookup": "https://api.b77bf911.workers.dev/pan?user={}",
    "🌾 Rashan Card": "https://api.b77bf911.workers.dev/rashan?aadhaar={}",
    "💸 UPI Lookup": "https://api.b77bf911.workers.dev/upi?user={}",
    "🏦 UPI V2": "https://api.b77bf911.workers.dev/upi2?user={}",
    "📡 Telegram Info": "https://api.b77bf911.workers.dev/telegram?user={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?user={}",
    
    # H4CKERR MX SPECIALS
    "📸 Insta Lookup": "https://allnew.proportalxc.workers.dev/instagram?username={}",
    "🔍 GST Lookup": "https://paid.proportalxc.workers.dev/gst?gst={}",
    "📍 Pincode Search": "https://paid.proportalxc.workers.dev/pincode?pincode={}",
    "🌐 IP Detail": "https://paid.proportalxc.workers.dev/ip?ip={}",
    
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

# --- ALL EXAMPLES (NO EXCEPTION) ---
EXAMPLES = {
    "🎮 FF Player Info": "Example: `2919267964` (Numeric UID)",
    "🚫 FF Ban Check": "Example: `2919267964` (Numeric UID)",
    "📊 FF Level Check": "Example: `2919267964` (Numeric UID)",
    "🌍 FF Region": "Example: `2919267964` (Numeric UID)",
    "🎁 FF Wishlist": "Example: `2919267964` (Numeric UID)",
    "🔍 FF Name Search": "Example: `yash` (In-game Name)",
    "🎫 FF Token Decode": "Example: `eyJhbGci...` (JWT Token)",
    "📅 FF Events": "Example: `indonesia` (Region Name)",
    "🚗 Vehicle V2": "Example: `DL10CE1234` (RC Number)",
    "💳 PAN Lookup": "Example: `ABCDE1234F` (PAN Number)",
    "🌾 Rashan Card": "Example: `123456789012` (Aadhaar Number)",
    "💸 UPI Lookup": "Example: `paytm@upi` (UPI ID)",
    "🏦 UPI V2": "Example: `paytm@upi` (UPI ID)",
    "📡 Telegram Info": "Example: `12345678` (User ID)",
    "🏦 IFSC Lookup": "Example: `SBIN0001234` (IFSC Code)",
    "📸 Insta Lookup": "Example: `physicswallah` (Username)",
    "🔍 GST Lookup": "Example: `07AAAAA0000A1Z5` (GSTIN)",
    "📍 Pincode Search": "Example: `110001` (Pin Code)",
    "🌐 IP Detail": "Example: `8.8.8.8` (IP Address)",
    "📱 Phone Lookup": "Example: `91XXXXXXXXXX` (With Country Code)",
    "📍 Num Trace": "Example: `91XXXXXXXXXX` (Mobile Number)",
    "🇵🇰 Pak Phone": "Example: `03XXXXXXXXX` (Pakistan Number)",
    "🆔 Aadhaar Lookup": "Example: `Rajesh Kumar` (Full Name)",
    "👤 Num Owner": "Example: `91XXXXXXXXXX` (Mobile Number)",
    "🚗 Vehicle Num": "Example: `DL10CE1234` (RC Number)",
    "📧 Email Lookup": "Example: `test@gmail.com` (Email ID)",
    "🐙 GitHub Profile": "Example: `torvalds` (Username)",
    "🔍 Domain/Whois": "Example: `google.com` (Domain Name)",
    "💳 BIN Lookup": "Example: `457173` (First 6 Digits)"
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
    bot.send_message(message.chat.id, "💀 **H4CKERR MX V15.0 - ALL FIXED**\nSaare tools aur examples set hain! 👇", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in APIS.keys())
def handle_menu_click(message):
    service = message.text
    user_state[message.chat.id] = service
    instruction = EXAMPLES.get(service, "Apni query niche enter karein:")
    bot.send_message(message.chat.id, f"🛠 **Tool:** {service}\n📝 **Instruction:** {instruction}", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.chat.id in user_state)
def process_lookup(message):
    chat_id = message.chat.id
    user_info = message.from_user
    selected_api = user_state[chat_id]
    query = message.text
    
    if query in APIS:
        handle_menu_click(message)
        return

    # --- ADMIN LOG FORMAT ---
    try:
        log_text = (
            "📢 **Log**\n"
            f"👤 **User:** {user_info.first_name}\n"
            f"🛠 **Tool:** {selected_api}\n"
            f"📝 **Query:** `{query}`"
        )
        bot.send_message(ADMIN_ID, log_text, parse_mode='Markdown')
    except: pass

    wait = bot.send_message(chat_id, "⏳ Data fetch ho raha hai...")
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
        bot.edit_message_text(f"❌ Error: API Down hai ya Timeout ho gaya!{DEV_TAG}", chat_id, wait.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    print("H4CKERR MX V15.0 is LIVE!")
    bot.remove_webhook()
    bot.infinity_polling()
