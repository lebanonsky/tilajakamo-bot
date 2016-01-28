#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from random import getrandbits

import re

from telegram import Updater, Update, InlineQueryResultArticle, ParseMode, ReplyKeyboardMarkup, ForceReply
import logging
import json
import time

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

tilajakamo_data = json.load(open('./tilajakamo.json'))

msg = ''

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text=tilajakamo_data['apua'])

def okei(bot, update):
    bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text=tilajakamo_data['okei!'])
    #bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text=update.message)

def share(bot, update):
    try:
        key = update.message.text.split()[1]
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää juttu komennon perään!")

    if key in tilajakamo_data:
        bot.sendMessage(update.message.chat_id, 
            text=tilajakamo_data[key], 
            disable_web_page_preview=False
            )
    else:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Ei ole!")

def join(bot, update):
    try:
        key = update.message.text.split()[1]
        if key in tilajakamo_data:
            bot.sendMessage(update.message.chat_id, 
                text=tilajakamo_data[key], 
                disable_web_page_preview=False
                )
    except:
        list = "Tapahtumat %s\nTalkoot %s\nSaneeraus %s\nOstomyyntivaihto %s\nTiedotteet %s" %(tilajakamo_data['tapahtumakanava'],tilajakamo_data['talkookanava'],tilajakamo_data['saneerauskanava'],tilajakamo_data['ostomyyntivaihto'], tilajakamo_data['tiedotteet'])
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text=list)

def test(bot, update):
    to_chat_id = tilajakamo_data['channel']['testi']
    chat = bot.getUpdates()[-1].message.chat_id
    logger.warn(chat)
    global msg
    logger.warn('moimoi %s', update.message ) 
    if 'new_chat_participant' in update.message:
        bot.sendMessage(update.message.chat_id, text="moi")

    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text = "Okei, lisää juttu komennon perään!")
        return
    # custom_keyboard = [[u'/OK', u'/EI' ]]
    # markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    # bot.sendMessage(update.message.chat_id, reply_markup = markup, text="Oletko varma!")

def sos(bot, update):
    to_chat_id = tilajakamo_data['channel']['sos']
    global msg
    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää hälytys komennon perään!")
        return
    custom_keyboard = [[u'/OK', u'/EI' ]]
    markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    bot.sendMessage(update.message.chat_id, reply_markup = markup, text="Oletko varma!")

def confirm(bot, update):
    to_chat_id = tilajakamo_data['channel']['sos']
    global msg
    bot.sendMessage(to_chat_id, msg)
    bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="SOS lähetetty!")

def cancel(bot, update):
    bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Peruutettu!")

def huolto(bot, update):
    to_chat_id = tilajakamo_data['channel']['huolto']
    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu huoltotoiveisiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää ilmoitus komennon perään!")

def siivous(bot, update):
    to_chat_id = tilajakamo_data['channel']['siivous']
    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu siivousilmoituksiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää ilmoitus komennon perään!")

def news(bot, update):
    to_chat_id = tilajakamo_data['channel']['tiedote']
    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu tiedotteisiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää uutinen komennon perään!")


def talkoot(bot, update):
    to_chat_id = tilajakamo_data['channel']['talkoot']
    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu talkookutsuihin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää kutsu komennon perään!")

def tapahtuma(bot, update):
    to_chat_id = tilajakamo_data['channel']['tapahtumat']
    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu tapahtumiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää tapahtuma komennon perään!")

def ehdotus(bot, update):
    to_chat_id = tilajakamo_data['channel']['ehdotus']
    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu ehdotuksiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää ehdotus komennon perään!")

def netti(bot, update):
    to_chat_id = tilajakamo_data['channel']['netti']
    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu nettivalituksiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää valitus komennon perään!")

def paatos(bot, update):
    to_chat_id = tilajakamo_data['channel']['kirjaus']
    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu hallituksen päätöksiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää päätös komennon perään!")

def omv(bot, update):
    to_chat_id = tilajakamo_data['channel']['omv']
    try:
        validmsg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split('/',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu osta-myy-vaihda kanavalle!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää ilmoitus komennon perään!")


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text=tilajakamo_data['apua'])

def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def inlinequery(bot, update):
    if update.inline_query is not None and update.inline_query.query:
        query = update.inline_query.query
        results = list()

        results.append(InlineQueryResultArticle(
                id=hex(getrandbits(64))[2:],
                title="Caps",
                message_text=query.upper()))

        results.append(InlineQueryResultArticle(
                id=hex(getrandbits(64))[2:],
                title="Bold",
                message_text="*%s*" % escape_markdown(query),
                parse_mode=ParseMode.MARKDOWN))

        results.append(InlineQueryResultArticle(
                id=hex(getrandbits(64))[2:],
                title="Italic",
                message_text="_%s_" % escape_markdown(query),
                parse_mode=ParseMode.MARKDOWN))

        bot.answerInlineQuery(update.inline_query.id, results=results)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    TOKEN = tilajakamo_data['token']
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("okei", okei)
    dp.addTelegramCommandHandler("apua", help)
    dp.addTelegramCommandHandler("jaa", share)
    dp.addTelegramCommandHandler("kuka", share)
    dp.addTelegramCommandHandler("huone", share)
    dp.addTelegramCommandHandler("testi", test)
    dp.addTelegramCommandHandler("liity", join)
    dp.addTelegramCommandHandler("huolto", huolto)
    dp.addTelegramCommandHandler("siivous", siivous)
    dp.addTelegramCommandHandler("netti", netti)
    dp.addTelegramCommandHandler("kirjaus", paatos)
    dp.addTelegramCommandHandler("talkoot", talkoot)
    dp.addTelegramCommandHandler("tapahtuma", tapahtuma)
    dp.addTelegramCommandHandler("ehdotus", ehdotus)
    dp.addTelegramCommandHandler("sos", sos)
    dp.addTelegramCommandHandler("SOS", sos)
    dp.addTelegramCommandHandler('OK', confirm)
    dp.addTelegramCommandHandler('EI', cancel)
    dp.addTelegramCommandHandler('ostan', omv)
    dp.addTelegramCommandHandler('myyn', omv)
    dp.addTelegramCommandHandler('vaihdan', omv)
    dp.addTelegramCommandHandler('tiedote', news)
        

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramInlineHandler(inlinequery)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
