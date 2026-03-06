import telebot
from datetime import datetime
import json

TOKEN = "8644495382:AAFKrhXiixBbhYdW4088BEoqbUxTFKNkdMU"

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    except:
        return {
            "percent":25,
            "rate":35,
            "total_thb":0,
            "total_usdt":0
        }

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f)

data = load_data()

def is_admin(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    admins = bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in admins]

    return user_id in admin_ids


# ตั้งค่าเปอร์เซ็นต์
@bot.message_handler(commands=['fee'])
def set_fee(message):

    if not is_admin(message):
        return

    try:
        percent = int(message.text.split()[1])
        data["percent"] = percent
        save_data(data)

        bot.reply_to(message,f"ตั้งค่าหัก {percent}% แล้ว")

    except:
        bot.reply_to(message,"ใช้คำสั่ง /fee 25")


# ตั้งค่าเรท USDT
@bot.message_handler(commands=['rate'])
def set_rate(message):

    if not is_admin(message):
        return

    try:
        rate = float(message.text.split()[1])
        data["rate"] = rate
        save_data(data)

        bot.reply_to(message,f"ตั้งค่าเรท USDT = {rate}")

    except:
        bot.reply_to(message,"ใช้คำสั่ง /rate 35")


# ดูสถานะ
@bot.message_handler(commands=['status'])
def status(message):

    if not is_admin(message):
        return

    bot.reply_to(message,
f"""
⚙️ค่าปัจจุบัน

ค่าธรรมเนียม = {data['percent']}%
เรท USDT = {data['rate']}

ยอดสะสม THB = {data['total_thb']:.2f}
ยอดสะสม USDT = {data['total_usdt']:.2f}
""")


# รีเซ็ตยอด
@bot.message_handler(commands=['reset'])
def reset(message):

    if not is_admin(message):
        return

    data["total_thb"] = 0
    data["total_usdt"] = 0
    save_data(data)

    bot.reply_to(message,"รีเซ็ตยอดแล้ว")


# คำนวณเงิน
@bot.message_handler(func=lambda m: True)
def calculate(message):

    if not is_admin(message):
        return

    try:

        amount = float(message.text)

        fee = amount * data["percent"] / 100
        remain = amount - fee
        usdt = remain / data["rate"]

        data["total_thb"] += remain
        data["total_usdt"] += usdt

        save_data(data)

        now = datetime.now().strftime("%d/%m/%Y เวลา %H:%M")

        text = f"""
วันที่ {now}

🏦บิลล่าสุด THB = {amount:.2f}

♻️ลบ{data['percent']}% = -{fee:.2f}
♻️เหลือยอด = +{remain:.2f}

🏦คำนวน USDT = {usdt:.2f}

💲ยอดสะสมรวมทั้งหมดวันนี้ THB = +{data['total_thb']:.2f}
💲ยอดสะสมรวมทั้งหมดวันนี้ USDT = +{data['total_usdt']:.2f}
"""

        bot.reply_to(message,text)

    except:
        pass


print("BOT STARTED")

bot.infinity_polling()
