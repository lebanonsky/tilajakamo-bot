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
import requests
import re
import pytz
from datetime import datetime

from django.utils import feedgenerator
#from feedgen.feed import FeedGenerator
from lxml import objectify
import lxml.etree as et


# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

tilajakamo_data = json.load(open('./tilajakamo.json'))

rooms = []

tilajakamo_base = "https://tilajakamo.fi/api/v1/pages"

def rest_update(bot, update):
    
    del rooms[:]

    rest_data = "%s/?type=home.RoomPage&limit=100" %(tilajakamo_base)

    try:
        json_data = requests.get(rest_data, verify=False).json()
    except:
        json_data = ''
    #tilajakamo_rest = json.load(rest_data.json())

    for page in json_data['pages']:
        room = requests.get(page['meta']['detail_url'], verify=False).json()
        rooms.append(room)

    logger.info(rooms)

    bot.sendMessage(update.message.chat_id, text='...ok')

    return rooms


def auto_update(bot):

    del rooms[:]

    rest_data = "%s/?type=home.RoomPage&limit=100" %(tilajakamo_base)


    json_data = requests.get(rest_data, verify=False).json()

    #tilajakamo_rest = json.load(rest_data.json())

    for page in json_data['pages']:
        room = requests.get(page['meta']['detail_url'], verify=False).json()
        rooms.append(room)

        #logger.info(room)

    return rooms

msg = ''
key = ''

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

def who(bot, update):
    try:
        key = update.message.text.split()[1].lower()
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text="Okei, lisää nimi komennon perään!")
        return

    msg=""

    h = 0

    for room in rooms:
        if room['member'] != None:
            if room['member']['title'].lower().startswith(key) or room['member']['first_name'].lower().startswith(key) or room['member']['last_name'].lower().startswith(key) or room['member']['telegram'].lower().startswith(key) or room['title'].startswith(key):
                intro = re.sub('<[^<]+?>', '', room['member']['intro'])
                msg = msg + '%s %s @%s #%s \n"%s"\n\n' %(room['member']['first_name'],room['member']['last_name'],room['member']['telegram'], room['title'],intro )    
                h+=1
              
    if h == 0:
        msg = "Ei ole!"

    bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text = msg )


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

def news_feed(bot,update):
    try:
        entry = update.message.text.split(' ',1)[1]
        logger.warn(update.update_id)
    except:
        pass

    feed = feedgenerator.Rss201rev2Feed(
         title = "Tilajakamo",
         link = "http://139.162.147.227/news.rss",
         description = "Osuuskunta Lapinlahden Tilajakamo tiedottaa",
         language="fi",
    )
    
    feed.add_item(
        title = "%s (%s)"%(entry, datetime.today().strftime('%d. %m. %Y') ),
        link = "#",
        description = "%s (%s)"%(entry, datetime.today().strftime('%d. %m. %Y') )
    )

    try:    
        with open('/var/www/html/news.rss','r') as fd:
            root = objectify.fromstring(fd.read())

        i = 0
        for item in root['channel']['item']:
            logger.warn(item.title)
            if i < 10:
                feed.add_item(title=item.title,
                    link=item.link,
                    description=item.description)
                i = i + 1            
    except:
        pass

    with open('/var/www/html/news.rss', 'w') as fp:
        feed.write(fp, 'utf-8')

def event_feed(bot,update):
    try:
        entry = update.message.text.split(' ',1)[1]
    except:
        pass

    feed = feedgenerator.Rss201rev2Feed(
         title = "Tilajakamo",
         link = "http://139.162.147.227/events.rss",
         description = "Osuuskunta Lapinlahden Tilajakamon tapahtumat",
         language="fi",
    )
    
    feed.add_item(
        title = u"%s (%s)"%(entry, datetime.today().strftime('%d. %m. %Y') ),
        link = "#",
        description = u"%s (%s)"%(entry, datetime.today().strftime('%d. %m. %Y') )
    )
    
    try:
        with open('/var/www/html/events.rss','r') as fd:
            root = objectify.fromstring(fd.read())

        i = 0
        for item in root['channel']['item']:
            if i < 10:
                feed.add_item(title=item.title,
                    link=item.link,
                    description=item.description)
                i = i + 1            
    except:
        pass

    with open('/var/www/html/events.rss', 'w') as fp:
        feed.write(fp, 'utf-8')

def remove_feed(bot,update):


    try:
        entry = update.message.text.split(' ',1)[1]
    except:
        pass
    
    # logger.warn('entry...%s',type(entry))

    with open('/var/www/html/news.rss','r') as fd:
        rss = objectify.fromstring(fd.read())    
        # logger.warn(rss['channel'])

        for item in rss['channel']['item']:
            title = unicode(item.title[0])
            # logger.warn('find...%s %s'%(entry, title.find(entry)))
            if title.find(entry) > -1:

                rss['channel'].remove(item)
                bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text = "Okei, poistettu feedistä")
    
    feed = et.tostring(rss)
    with open('/var/www/html/news.rss', 'w') as fp:
        fp.write(feed)         

    # try:
    #     with open('/var/www/html/news.rss','r') as fd:
    #         root = objectify.fromstring(fd.read())

    #     for item in root['channel']['item']:
    #         if entry[:9] in item.title[:9]:
    #             item.getparent().remove(item)
    #             bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text = "Okei, poistettu feedistä")
    #             with open('/var/www/html/news.rss', 'w') as fp:
    #                 fp.write(et.tostring(fd), 'utf-8')         
    # except:
    #     pass


def test(bot, update):
    to_chat_id = tilajakamo_data['channel']['testi']
    #news_feed(bot, update)
    # chat = bot.getUpdates()[-1].message.chat_id

    global msg
    try:
        msg = "%s %s: %s" %(update.message.from_user.first_name, update.message.from_user.last_name, update.message.text.split(' ',1)[1]) 
        bot.sendMessage(to_chat_id, msg)
    except:
        bot.sendMessage(update.message.chat_id, reply_to_message_id = update.message.message_id, text = "Okei, lisää juttu komennon perään!")
        return
    # custom_keyboard = [[u'/OK', u'/EI' ]]
    # markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    # bot.sendMessage(update.message.chat_id, reply_markup = markup, text="Oletko varma!")

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
    news_feed(bot, update)

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
    event_feed(bot, update)
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
    
    jq = updater.job_queue
    jq.put(auto_update, 3600, next_t=21600)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("okei", okei)
    dp.addTelegramCommandHandler("apua", help)
    dp.addTelegramCommandHandler("jaa", share)
    dp.addTelegramCommandHandler("kuka", who)
    dp.addTelegramCommandHandler("huone", who)
    dp.addTelegramCommandHandler("testi", test)
    dp.addTelegramCommandHandler("liity", join)
    dp.addTelegramCommandHandler("huolto", huolto)
    dp.addTelegramCommandHandler("siivous", siivous)
    dp.addTelegramCommandHandler("netti", netti)
    dp.addTelegramCommandHandler("kirjaus", paatos)
    dp.addTelegramCommandHandler("p", paatos)
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
    dp.addTelegramCommandHandler('who', who)
    dp.addTelegramCommandHandler('update', rest_update)
    dp.addTelegramCommandHandler('feed', news_feed)
    dp.addTelegramCommandHandler('poista', remove_feed)
    
    

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramInlineHandler(inlinequery)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()
    
    # Alternatively, run with webhook:
    #updater.bot.setWebhook(webhook_url='http://44807aa7.ngrok.com/%s/webhook' % TOKEN)
    #update_queue = updater.start_webhook('0.0.0.0', 8443)

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
