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

from telegram import Updater, Update, InlineQueryResultArticle, ParseMode
import logging
import json

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

tilajakamo_data = json.load(open('./tilajakamo.json'))

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text=tilajakamo_data['apua'])

def okei(bot, update):
    bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text=tilajakamo_data['okei!'])

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
        list = "Tapahtumat %s\n Talkoot %s\nSaneeraus %s" %(tilajakamo_data['tapahtumakanava'],tilajakamo_data['talkookanava'],tilajakamo_data['saneerauskanava'])
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text=list)

def test(bot, update):
    to_chat_id = tilajakamo_data['testi']
    try:
        msg = update.message.text.split(' ',1)[1]
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu testiin!")
        bot.sendMessage(to_chat_id, msg)
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text = "Okei, lisää juttu komennon perään!")
        
def huolto(bot, update):
    to_chat_id = tilajakamo_data['huolto']
    try:
        msg = update.message.text.split(' ',1)[1]
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu huoltotoiveisiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää juttu komennon perään!")

def siivous(bot, update):
    to_chat_id = tilajakamo_data['siivous']
    try:
        msg = update.message.text.split(' ',1)[1]
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu siivousilmoituksiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää juttu komennon perään!")

def talkoot(bot, update):
    to_chat_id = tilajakamo_data['talkoot']
    try:
        msg = update.message.text.split(' ',1)[1]
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu talkookutsuihin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää juttu komennon perään!")

def tapahtuma(bot, update):
    to_chat_id = tilajakamo_data['tapahtumat']
    try:
        msg = update.message.text.split(' ',1)[1]
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu tapahtumiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää juttu komennon perään!")

def ehdotus(bot, update):
    to_chat_id = tilajakamo_data['ehdotus']
    try:
        msg = update.message.text.split(' ',1)[1]
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu ehdotuksiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää juttu komennon perään!")

def sos(bot, update):
    to_chat_id = tilajakamo_data['sos']
    try:
        msg = update.message.text.split(' ',1)[1]
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu HÄLYTYKSIIN!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää juttu komennon perään!")

def netti(bot, update):
    to_chat_id = tilajakamo_data['netti']
    try:
        msg = update.message.text.split(' ',1)[1]
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu nettivalituksiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää juttu komennon perään!")

def paatos(bot, update):
    to_chat_id = tilajakamo_data['kirjaus']
    try:
        msg = update.message.text.split(' ',1)[1]
        bot.sendMessage(to_chat_id, msg)
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Tallennettu hallituksen päätöksiin!")
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää juttu komennon perään!")

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
