import telebot
import requests
import json
import os
import time
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = "8411017661:AAFYSg_0ATzf-sPmoj-it77t3pp_4RAyWUg"
ADMIN_ID = 5192884021  # <--- Yahan apni Numerical ID daalein
bot = telebot.TeleBot(API_TOKEN)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# --- ALL APIS (Parameter Fixes Included) ---
APIS = {
    "📸 Insta Lookup": "https://allnew.proportalxc.workers.dev/instagram?username={}",
    "🔍 GST Lookup": "https://paid.proportalxc.workers.dev/gst?gst={}",
    "📍 Pincode Search": "https://paid.proportalxc.workers.dev/pincode?pincode={}",
    "🌐 IP Detail": "https://paid.proportalxc.workers.dev/ip?ip={}",
    "💳 PAN Lookup": "https://api.b77bf911.workers.dev/pan?user={}",
    "🌾 Rashan Card": "https://api.b77bf911.workers.dev/rashan?aadhaar={}", # FIXED
    "💸 UPI Lookup": "https://api.b77bf911.workers.dev/upi?user={}",
    "🏦 UPI V2": "https://api.b77bf911.workers.dev/upi2?user={}",
    "🚗 Vehicle V2": "https://api.b77bf911.workers.dev/v2?user={}",
    "📡 Telegram Info": "https://api.b77bf911.workers.dev/telegram?user={}",
    "🏦 IFSC Lookup": "https://api.b77bf911.workers.dev/ifsc?user={}",
    "🎮 FF Player Info": "http://203.57.85.58:2005/player-info?uid={}",
    "🚫 FF Ban Check": "http://203.57.85.58:2005/bancheck?uid={}",
    "📊 FF Level Check": "http://203.57.85.58:2005/level?uid={}",
    "🌍 FF Region": "http://203.57.85.58:2005/region?uid={}",
    "🔍 FF Name Search": "http://203.57.85.58:2005/search?name={}",
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
    "🌾 Rashan Card": "Example: `123456789012` (Aadhaar Number)",
    "📸 Insta Lookup": "Example: `physicswallah` (Username)",
    "💳 PAN Lookup": "Example: `ABCDE1234F` (PAN Card)",
    "💸 UPI Lookup": "Example: `paytm@upi` (UPI ID)",
    "🎮 FF Player Info": "Example: `2919267964` (UID)",
    "🆔 Aadhaar Lookup": "Example: `Rajesh Kumar` (Name)"
}

user_state = {}
DEV_TAG = "\n\n━━━━━━━━━━━━━━━\n👤 **Developer:- @hackerrmx69**"

# --- HELPER FUNCTIONS ---
def send_long_message(chat_id, text):
    if len(text) <= 4096:
        bot.send_message(chat_id, text, parse_mode='Markdown')
    else:
        for i in range(0, len(text), 4000):
            bot.send_message(chat_id, text[i:i+4000])

# --- COMMANDS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(name) for name in APIS.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "💀 **H4CKERR MX Multi-Lookup V9.0**\nAll Parameters Fixed! Select a tool 👇", reply_markup=markup, parse_mode='Markdown')

# Admin Broadcast Command: /bc Your Message
@bot.message_handler(commands=['bc'])
def broadcast(message):
    if message.from_user.id == ADMIN_ID:
        msg_text = message.text.replace('/bc ', '')
        if msg_text == '/bc':
            bot.reply_to(message, "Usage: `/bc Your Message`")
            return
        # Note: Dynamic user tracking needs a database, this is for basic admin use
        bot.send_message(message.chat.id, f"📢 Broadcast Sent: {msg_text}")
    else:
        bot.reply_to(message, "❌ Access Denied!")

# --- MESSAGE HANDLERS ---
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
    query_text = message.text
    
    if query_text in APIS:
        handle_menu_click(message)
        return

    try:
        log = f"📢 **Log**\n👤 **User:** {user_info.first_name}\n🛠 **Tool:** {selected_api}\n📝 **Query:** `{query_text}`"
        bot.send_message(ADMIN_ID, log)
    except: pass

    wait_msg = bot.send_message(chat_id, "⏳ Fetching Data...")
    del user_state[chat_id]

    try:
        url = APIS[selected_api].format(query_text)
        response = requests.get(url, headers=HEADERS, timeout=20)
        
        try:
            raw_data = response.json()
            pretty_json = json.dumps(raw_data, indent=2, ensure_ascii=False)
            header = f"✅ **Result ({selected_api}):**\n"
            full_response = f"{header}```json\n{pretty_json}\n```\n{DEV_TAG}"
            bot.delete_message(chat_id, wait_msg.message_id)
            send_long_message(chat_id, full_response)
        except:
            bot.edit_message_text(f"⚠️ **Response:**\n`{response.text[:1000]}`\n{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')
            
    except:
        bot.edit_message_text(f"❌ Error: API Connection Failed!{DEV_TAG}", chat_id, wait_msg.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    print("H4CKERR MX V9.0 is LIVE!")
    bot.remove_webhook()
    bot.infinity_polling()
    
