import time
import re
import cloudscraper
from bs4 import BeautifulSoup
from telegram import Bot

# ==========================
# CONFIG
# ==========================

EMAIL = "muqueetyt@gmail.com"
PASSWORD = "Usatiktok1$"

BOT_TOKEN = "8733336332:AAFlW2wMsYJPhhl08b7_Hzb6ZP4TUIAqGCk"
GROUP_ID = "-1003622434067"

LOGIN_URL = "https://ivasms.com/login"
SMS_URL = "https://www.ivasms.com/portal/live/my_sms"

CHECK_DELAY = 5

bot = Bot(token=BOT_TOKEN)

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "android",
        "mobile": True
    }
)

sent_messages = set()

# ==========================
# LOGIN SYSTEM
# ==========================

def login():
    print("🔐 Logging in...")

    scraper.get(LOGIN_URL)

    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }

    r = scraper.post(LOGIN_URL, data=payload)

    if "dashboard" in r.text.lower():
        print("✅ Login Successful")
        return True

    print("❌ Login Failed")
    return False


# ==========================
# OTP EXTRACTOR
# ==========================

def find_otps(text):

    otps = re.findall(r"\b\d{4,8}\b", text)
    return list(set(otps))


# ==========================
# MESSAGE FORMATTER
# ==========================

def format_message(sender, otp):

    return f"""
✨ <b>NEW OTP RECEIVED</b>

📱 <b>Sender:</b> {sender}
🔐 <b>OTP Code:</b> <code>{otp}</code>

⚡ Auto Forwarded
🌐 IVASMS Panel
"""


# ==========================
# SMS CHECKER
# ==========================

def check_sms():

    global sent_messages

    r = scraper.get(SMS_URL)

    # session expired
    if "login" in r.url.lower():
        print("♻ Session expired → Relogin")
        login()
        return

    soup = BeautifulSoup(r.text, "lxml")

    page_text = soup.get_text()

    otps = find_otps(page_text)

    for otp in otps:

        if otp in sent_messages:
            continue

        sent_messages.add(otp)

        message = format_message("Unknown", otp)

        bot.send_message(
            chat_id=GROUP_ID,
            text=message,
            parse_mode="HTML"
        )

        print("✅ OTP Forwarded:", otp)


# ==========================
# MAIN LOOP
# ==========================

login()

while True:
    try:
        check_sms()
        time.sleep(CHECK_DELAY)

    except Exception as e:
        print("⚠ ERROR:", e)
        time.sleep(15)
