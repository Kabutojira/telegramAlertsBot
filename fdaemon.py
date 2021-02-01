#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

import logging
import sys
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import time
import datetime
from datetime import date
import yfinance as yf
import pandas as pd
from talib.abstract import *


def get_changes(ticker,smatimeperiod=5):
    t = yf.Ticker(ticker)
    history = t.history(period="1d",interval="1m")
    close_prices = pd.DataFrame(history, columns=['Close'])
    sma = SMA(close_prices.values[:,0], timeperiod=smatimeperiod)
    sma = sma.tolist()
    changes = {}
    for minutes in [10,15,30,60]:
        if len(sma) > minutes+1:
            changes[str(minutes)] = ((sma[-1] - sma[-(minutes+1)]) / sma[-(minutes+1)] ) * 100
    print(changes)
    return changes
               
def check_price(context):
    job = context.job
    changes = get_changes('GME')
    for time,change in changes.items():
        if float(change) > 20:
            msg = time + " minutes change is " + str(round(change)) + "%\n"
            for i in range(0,round(change/20)):
                msg = msg + "🚀"
            context.bot.send_message(job.context, text = msg)
        if float(change) < -20:
            msg = time + " minutes change is " + str(round(change)) + "%\n"
            for i in range(0,round(-change/20)):
                msg = msg + "📉"
            context.bot.send_message(job.context, text = msg)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("💎🤲🚀🚀🚀")
    for job in context.job_queue.get_jobs_by_name(str(update.message.chat_id)):
        job.schedule_removal()
    context.job_queue.run_repeating(callback=check_price, interval=300, context=update.message.chat_id, name=str(update.message.chat_id))

def halt(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("👋 Bye!")
    os.system("ps aux | grep fdaemon.py | grep -v grep | awk '{print $2}' | xargs kill -SIGABRT")

def main():
    if not os.environ.get('TOKEN') and len(sys.argv) < 2:
        print('missing token')
        sys.exit(1)
    elif os.environ.get('TOKEN'): 
        updater = Updater(os.environ.get('TOKEN'), use_context=True)
    else:
        updater = Updater(sys.argv[1], use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("exit", halt))
    dispatcher.add_handler(CommandHandler("quit", halt))
    dispatcher.add_handler(CommandHandler("restart", halt))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print (e)
            sys.exit(0)
