import telebot
from datetime import datetime
import json

TOKEN = "8644495382:AAFKrhXiixBbhYdW4088BEoqbUxTFKNkdMU"

bot = telebot.TeleBot(TOKEN)

data = {
    "percent":25,
    "rate":35,
    "total_thb":0,
    "total_usdt":0
}

@bot.message_handler(commands=['fee'])
def fee(message):
    global data
    try:
        p = int(message.text.split()[1])
        data["percent"] = p
        bot.reply_to(message,f"ตั้งค่าหัก {p}%")
    except:
        bot.reply_to(message,"ใช้ /fee 25")

@bot.message_handler(commands=['rate'])
def rate(message):
    global data
    try:
        r = float(message.text.split()[1])
        data["rate"] = r
        bot.reply_to(message,f"เรท USDT = {r}")
    except:
        bot.reply_to(message,"ใช้ /rate 35")

@bot.message_handler(commands=['reset'])
def reset(message):
    data["total_thb"]=0
    data["total_usdt"]=0
    bot.reply_to(message,"รีเซ็ตยอดแล้ว")

@bot.message_handler(func=lambda m: True)
def calc(message):

    global data

    try:

        amount = float(message.text)

        fee = amount * data["percent"]/100
        remain = amount - fee
        usdt = remain / data["rate"]

        data["total_thb"] += remain
        data["total_usdt"] += usdt

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

bot.infinity_polling()
