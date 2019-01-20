#!/usr/bin/env python3

import os
import time
import picamera
import telebot

import gy21
import gy68
import gy302

if "API_TOKEN" not in os.environ:
    raise AssertionError("Please configure API_TOKEN as environment variables")

API_TOKEN = os.environ["API_TOKEN"]
USER = [215381056, 361484960]

bot = telebot.TeleBot(API_TOKEN)
gy21_sensor = gy21.Gy21()
gy68_sensor = gy68.Gy68()
gy302_sensor = gy302.Gy302()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    "Handle '/start' and '/help'"
    bot.reply_to(message, "Hi, I'm Vetall's bot")


def process_message(message):
    "Processing text messages"
    gy21_data = gy21_sensor.get_tmpr_and_hmdt()
    gy68_data = gy68_sensor.get_temperature()
    gy302_data = gy302_sensor.get_luminance()
    msg = "t1 = {0:.1f}{1}C\nt2 = {2:.1f}{1}C\nh  = {3:.1f}%\nl   = {4:.0f}lx"\
    .format(gy21_data[0], '\u00b0', gy68_data, gy21_data[1], gy302_data)

    bot.send_message(message.chat.id, msg)

def print_message(message, text):
    "Printeng text messages"
    bot.send_message(message.chat.id, text)


def process_photo(message):
    "Make and send photo"
    with picamera.PiCamera(resolution = (1024, 768)) as camera:
        camera.rotation = 180
        camera.start_preview()
        time.sleep(2)
        camera.capture('/home/pi/Documents/photo.jpg')
        camera.stop_preview()
    bot.send_photo(message.chat.id, open('/home/pi/Documents/photo.jpg', 'rb'))


@bot.message_handler(commands=['photo'])
def make_photo(message):
    "Handle '/photo' command"
    if message.chat.id in USER:
        process_photo(message)
    else:
        print_message(message, "access denied")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    '''Handle all other messages with content_type 'text' \
    (content_types defaults to ['text'])'''
    if message.chat.id in USER:
        process_message(message)
    else:
        print_message(message, "access denied")


bot.polling()
