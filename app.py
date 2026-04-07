import requests
from bs4 import BeautifulSoup
import time
import re

EMAIL = "muqueetyt@gmail.com"
PASSWORD = "Usatiktok1$"

BOT_TOKEN = "8733336332:AAFlW2wMsYJPhhl08b7_Hzb6ZP4TUIAqGCk"
CHAT_ID = "-1003622434067"

LOGIN_URL = "https://ivasms.com/login"
SMS_URL = "https://ivasms.com/portal/test_sms_history"

session = requests.Session()
sent_messages = set()


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def login():
    data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    session.post(LOGIN_URL, data=data)
    print("Logged in")


def extract_otp(text):
    otp = re.findall(r"\b\d{4,6}\b", text)
    return otp[0] if otp else None


def check_sms():
    r = session.get(SMS_URL)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.find_all("tr")

    for row in rows:
        text = row.text.strip()

        # avoid duplicate forwarding
        if text in sent_messages:
            continue

        otp = extract_otp(text)

        if otp:
            sent_messages.add(text)

            send_telegram(
                f"📩 NEW OTP RECEIVED\n\n{text}"
            )


login()

while True:
    try:
        check_sms()
        time.sleep(20)

    except Exception as e:
        print("Error:", e)
        login()
        time.sleep(10)
