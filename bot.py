#!/usr/bin/env python3

import telebot
import os, sys
import gy21, gy68, gy302

if "API_TOKEN" not in os.environ:
    raise AssertionError("Please configure API_TOKEN as environment variables")

API_TOKEN = os.environ["API_TOKEN"]
USER = [215381056, 361484960]

bot = telebot.TeleBot(API_TOKEN)
gy21_sensor = gy21.Gy21()
gy68_sensor = gy68.Gy68()
gy302_sensor = gy302.Gy302()


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hi, I'm Vetall's bot")


def process_message(message):
    gy21_data = gy21_sensor.get_tmpr_and_hmdt()
    gy68_data = gy68_sensor.get_temperature()
    gy302_data = gy302_sensor.get_luminance()
    msg = "t1 = {0:.1f}{1}C\nh = {2:.1f}%\nt2 = {3:.1f}{1}C\nl = {4:.0f}lx"\
    .format(gy21_data[0], '\u00b0', gy21_data[1], gy68_data, gy302_data)

    bot.send_message(message.chat.id, msg)

def print_message(message, text):
        bot.send_message(message.chat.id, text)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.chat.id in USER:
        process_message(message)
    else:
        print_message(message, "access denied")


bot.polling()
