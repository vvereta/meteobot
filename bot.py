#!/usr/bin/env python3

import telebot
import os, sys
import gy21

if "API_TOKEN" not in os.environ:
    raise AssertionError("Please configure API_TOKEN as environment variables")

API_TOKEN = os.environ["API_TOKEN"]
USER = [215381056, 361484960]

bot = telebot.TeleBot(API_TOKEN)
gy21_sensor = gy21.Gy21()


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hi, I'm Vetall's bot")


def process_message(message):
    gy21_data = gy21_sensor.get_tmpr_and_hmdt()
    msg = "t = {0:.2f}{1}C\nh = {2:.2f}%"\
    .format(gy21_data[0], '\u00b0', gy21_data[1])

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
