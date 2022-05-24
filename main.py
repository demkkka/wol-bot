import paramiko
from time import sleep
from ping3 import ping
from telebot import telebot, types
from wakeonlan import send_magic_packet
from config import botToken, telegramUsername, winPcMac, winPcUsername, winPcIp, winPcPassword, sshPort

bot = telebot.TeleBot(botToken)

def actions_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    turnOnPcButton = types.KeyboardButton(text="turn on")
    turnOffPcButton = types.KeyboardButton(text="turn off")
    statusButton = types.KeyboardButton(text="status")
    keyboard.add(statusButton, turnOnPcButton, turnOffPcButton)
    return keyboard

def statusOfPc(host):
    resp = ping(host)
    if resp is None:
        return 'computer is off'
    else:
        return 'computer is on'

def turnOnPc(macAddress):
    send_magic_packet(macAddress)
    
def turnOffWinPc():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=winPcIp, username=winPcUsername, password=winPcPassword, port=sshPort)
    client.exec_command('shutdown /s /f /t 0')
    client.close()
    
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.username == telegramUsername:
        bot.reply_to(message, f'hi, '+message.from_user.first_name)
    else:
        bot.reply_to(message, f' my parents don\'t allow me to talk to strangers, we won\'t have a dialogue :<')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.from_user.username == telegramUsername:
        if message.text.lower() == 'turn on':
            turnOnPc(winPcMac)
            bot.send_message(message.from_user.id, 'magic packet sent to '+winPcMac, reply_markup=actions_keyboard())
            sleep(25)
            bot.send_message(message.from_user.id, statusOfPc(winPcIp), reply_markup=actions_keyboard())
        elif message.text.lower() == 'turn off':
            bot.send_message(message.from_user.id, 'computer is shuting down...', reply_markup=actions_keyboard())
            turnOffWinPc()
            sleep(21)
            bot.send_message(message.from_user.id, statusOfPc(winPcIp), reply_markup=actions_keyboard())
        elif message.text.lower() == 'status':
            bot.send_message(message.from_user.id, 'checking...', reply_markup=actions_keyboard())
            bot.send_message(message.from_user.id, statusOfPc(winPcIp), reply_markup=actions_keyboard())
        else:
            bot.send_message(message.from_user.id, 'I don\'t understand what this means')
    else:
        bot.reply_to(message, f'You\'re not my parent')

def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()